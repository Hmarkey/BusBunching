# coding=utf-8
"""
Reinforcement learning bus bunching:
    debug switches and debug information
"""

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
        pass

    '''
    关闭debug开关
    '''
    def debug_off(self, debug_str):
        pass

    '''
    显示debug开关信息
    '''
    def debug_show(self):
        pass

    '''
    打印日志信息
    type：日志类型：{"BUS", "STOP", "ENV"}
    content: 日志内容
    *args：可变参数
    '''
    def Log(self, type, content, *args):
        pass

    '''
    打印日志信息到终端
    '''
    def Log_vty(self, type, content, *args):
        pass

    '''
    打印日志信息到文件
    '''
    def Log_File(self, type, content, file_path, *args):
        pass
