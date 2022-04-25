# coding=utf-8
import numpy as np


debug_stop=False
#debug=True

class bus_stop():
    '''
    id:               bus stop id
    arr_dis:          arrival distribution 0 for possion 1 for uniform
    schedule_hw:      set schedule arrival interval
    actual_bus_arr:   actual bus arrival time list
    bus_arr_interval: actual bus arrival interval list
    arr_rate:         arrival rate
    board_rate:       boarding rate
    tor_cap:          passenger tolerance on the maixmum loading number on bus
    wait_num:         number of passenger waiting on the bus stop
    corr_radius:      radius of bus corridor
    loc:              location of bus stop in angle
    scale:            scale factor in favor of visualization
    wait_time_sum:    total waiting time
    wait_num_sep:     accumulated waiting number between two consecutive arrival of buses
    '''
    def __init__(self, id, bus_stop_num, pos,bus_nums,arr_rate, process_rate, wait_num,wait_accumulate=[0]): # arr_dis : arrive distribution. 0 for uniform, 1 for possion
        ### my code
        self.id = id
        self.bus_stop_num=bus_stop_num
        self.pos = pos
        self.wait_num = wait_num
        self.is_served = 0                                  ## 标志当前是否被服务
        self.actual_bus_arr=[0 for i in range(bus_nums)]    ## 标志，当前是否有公车在该站
        self.arr_rate =  arr_rate                        #min(abs(np.random.normal(loc=1/2/30,scale=0.1)),2/60 )# person / s
        self.process_rate = process_rate
        self.wait_accumulate = wait_accumulate
        self.arrival=0
        self.arrival_list = [0]
        self.wait_accumulate_list = [0]


        '''
        ### paper's code
        self.id = id
        self.arr_dis = arr_dis
        self.schedule_hw = H # scheduled bus arrival headway
        self.actual_bus_arr=[]
        self.bus_arr_interval = []
        self.arr_rate =  arr_rate#min(abs(np.random.normal(loc=1/2/30,scale=0.1)),2/60 )# person / s
        # print(self.arr_rate)
        self.tor_cap = 120 # bus capacity
        self.board_rate = board_rate  # person / s
        self.wait_num = wait_num # 1 pixel for 10 person
        self.corr_radius = radius
        self.loc = alpha # determine stop location
        self.stop_x = self.corr_radius*np.cos(alpha)
        self.stop_y = self.corr_radius*np.sin(alpha)
        self.scale = 1. # scale waitline for visualization
        self.is_served = 0
        self.wait_time_sum = 0
        self.wait_num_sep = 0
        self.wait_num_all=0
        '''
    def step(self):
        ## 主要更新乘客数量(隐含多辆车到达，处理乘客上车时间不变)
        if debug_stop:
            print("Stop: ",self.id ," is served? ",self.is_served )
            #print("    Bus Stop: ",self.id ," Wait Number: ",self.wait_num )
        if(self.is_served==0):
            self.arrival=np.random.poisson(self.arr_rate, 1)[0]
            self.wait_num += self.arrival
        else:
            self.wait_num -= self.process_rate
            self.wait_num = max(self.wait_num, 0.)
        self.is_served=0
        self.arrival_list.append(self.arrival)
        self.wait_accumulate_list.append(self.wait_num)



