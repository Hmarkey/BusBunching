# coding=utf-8
"""
Reinforcement learning bus bunching:
    debug switches and debug information
"""

import time
import os
import traceback

from sqlalchemy import true

class Debug():
    def __init__(self):
        self.debug_bus  = False
        self.debug_stop = False
        self.debug_env  = False
        self.debug_all  = False
        self.debug_passenger = False

    '''
    打开debug开关
    '''
    def debug_on(self, debug_str):
        if(debug_str == "bus"):
            self.debug_bus = True
        elif(debug_str == "stop"):
            self.debug_stop = True
        elif(debug_str == "env"):
            self.debug_env = True
        elif(debug_str == "passenger"):
            self.debug_passenger = True
        elif(debug_str == "all"):
            self.debug_all = True
        else:
            assert(0)

    '''
    关闭debug开关
    '''
    def debug_off(self, debug_str):
        if(debug_str == "bus"):
            self.debug_bus = False
        elif(debug_str == "stop"):
            self.debug_stop = False
        elif(debug_str == "env"):
            self.debug_env = False
        elif(debug_str == "passenger"):
            self.debug_passenger = False
        elif(debug_str == "all"):
            self.debug_all = False
            self.debug_bus = False
            self.debug_stop = False
            self.debug_env = False
            self.debug_passenger = False
        else:
            assert(0)

    '''
    显示debug开关信息
    '''
    def debug_show(self):
        pass

    '''
    判断type类型的日志是否要进行打印
    '''
    def debug_status(self, type):
        if(self.debug_all == True):
            return True
        if(self.debug_bus and type == "bus"):
            return True
        if(self.debug_stop and type == "stop"):
            return True
        if(self.debug_env and type == "env"):
            return True
        if(self.debug_passenger and type == "passenger"):
            return True
        return False
        
    '''
    打印日志信息
    type：日志类型：{"BUS", "STOP", "ENV", "PASSENGER"}
    content: 日志内容
    *args：可变参数
    '''
    def Log(self, type, content, *args):
        res = "%-10s| "%type
        # 记录时间
        cur_time = time.strftime("%H:%M:%S", time.localtime(time.time()))
        res = res + cur_time + " | "
        # 记录调用信息:调用文件名和行数
        trace = traceback.extract_stack()
        res = res + trace[-3][0] + " | " + str(trace[-3][1]) + " | "
        # 记录日志内容
        res = res + content + "\n"

        return res

    '''
    打印日志信息到终端
    '''
    def Log_Vty(self, type, content, *args):
        if self.debug_status(type) == False:
            return
        res = self.Log(type, content, *args)
        print(res)
        pass

    '''
    打印日志信息到文件

    '''
    def Log_File(self, type, content, *args):
        # 如果开关没打开，直接返回
        if self.debug_status(type) == False:
            return
        # 获取当前日期作为文件名
        cur_date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        res = self.Log(type, content, *args)
        # 获取当前目录组合文件路径
        basepath = os.path.abspath('..')
        filepath = basepath + "/log/"+ cur_date + ".txt"
        with open(filepath, "a+", encoding="utf-8") as f:
            f.write(res)

if __name__ == '__main__':
    Test = Debug()
    Test.debug_on("bus")
    Test.debug_on("all")
    Test.Log_Vty("bus", "this is test {}".format(10))
    Test.Log_File("passenger", "this is test {}".format(10))

