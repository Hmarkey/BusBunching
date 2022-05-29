# coding=utf-8
import numpy as np
import pandas as pd
import math

debug_bus=False
#debug=True

class bus():
    '''
    假设：
    公交车容量无限
    乘客按泊松分布到达车站
    公交车在乘客上车后开始计算holding_time, hold_time期间不让乘客上车
    不考虑乘客的下车时间，永远认为乘客上车时间比下车时间大

    id:                bus id
    is_serving:        whehter bus is serving a stop 1:stop for service 0:on route -1:holding -2: not emit
    omega:             angle speed
    capacity:          bus capacity
    car_size:          car size for visualization
    track_radius:      radius of bus corridor
    color:             car color for visualization
    step:              simulation step increase with 1
    slack time:        time cost at each station
    emit_time:         time for departure
    is_emit:           emit flag
    serve_list:        record served  passgenger number for each stop of a bus through the simulation
    alight_list:       record numbers of passenger to alight in each stop in real time
    serve_level:       bus serve level
    dispatch_loc:      dispatch location
    loc:               bus current loc (reset when arriving at origin station in favor of visualization)
    travel_sum:        overall distance the bus has traveled
    arrival_schedule:  schedule arrval time on a stop
    arrival_bias:      bias between schedule arrival time and actual arrival time
    alight_rate:       alighting rate
    onboard_list:      record number of passenger on board boarding from each stop in real time
    slack_time:         slack time to force bus keep pace with the schedule <= hold time
    slack_time_sum:     sum of slack time
    hold_time:         holding time to force bus keep pace with the schedule
    hold_time_list:     sum of holding time
    trajectory:        record bus trajectory
    hold_stop:         record at which station the bus is holding
    state:             state observation from the perspective of bus
    action:            control for each stop
    reward:            minimize mean of headway and variance of headway
    is_close           the bus is closed or not. 0:open 1:close
    ass_dispatch_loc:  assist locate the bus in trajectory construction
    hold_action:       record the where and when the holding function
    is_serving_rl:     flag for RL train sample collect
    special_state:     0 for normal ,1 for catching its leading bus
    serve_stop:        record which stop the bus is serving
    trip_record        record travel point for each od-pair trip
    trip_cost        record travel cost for each od-pair trip
    '''
    def __init__(self, id, speed, process_rate, at_stop, pos, pass_num, action_num, start_stop, bus_nums, stop_nums, stop_pos):
        ### my code
        self.id =id
        self.speed = speed                  ## 公车的角速度
        self.at_stop = at_stop              ## 记录公车所在的公交站id，不在则为-1
        self.pos = pos                      ## 记录公车在环上的角度，以12点钟顺时针开始计算，单位为角度
        self.pass_num = pass_num            ## 当前车上乘客的总数量，后续考虑作为reward函数的权重,
        self.pass_up = [0 for i in range(stop_nums)]            ## 每一站上车人数量                            #DX??
        #self.pass_down = [0 for i in range(stop_nums)]          ## 每一站下车人数量
        self.cur_step = 0                   ## 公车的时间步数
        self.bus_num = bus_nums             # total bus number
        self.bus_stop_num = stop_nums       # total bus stop number
        self.start_stop = start_stop        ## 公交车起始车站
        self.hold_time = 0                  ## 本站做出的决策，等待多长时间
        self.toprocess_num = 0           ## 公车在本站处理乘客的数量
        self.hold_time_list=[]              ## 在每个站的hold_time
        self.is_feedback = False
        self.process_rate  =  process_rate
        self.stop_pos = stop_pos
        self.trajectory = []                ##公交车行驶轨迹


    def check_through_stop(self, stop_id, old_pos, new_pos):
        stop_pos = self.stop_pos[stop_id]
        if(new_pos<360):
            return (old_pos<stop_pos and stop_pos<=new_pos)
        else:
            if(stop_pos>old_pos):
                return True
            else:
                if(stop_pos+360<=new_pos):
                    return True
                else:
                    return False

    def step(self):
        ## 更新公交车位置
        if debug_bus:
            print("Bus ", self.id, "is at Bus Stop ",self.at_stop , "is feed back? ", self.is_feedback)  #
        if(self.at_stop == -1):
            old_pos = self.pos
            new_pos = self.pos + self.speed
            for stop_id in range(self.bus_stop_num):
                if(self.check_through_stop(stop_id, old_pos, new_pos)):
                    self.at_stop = stop_id
                    self.pos = self.stop_pos[stop_id]
                else:
                    self.pos = new_pos % 360
            #self.is_feedback = False  (DX不需要)
        else:
            if(self.toprocess_num>0):
                #self.pass_up[self.at_stop] += min(self.process_rate, self.toprocess_num)
                if (debug_bus):
                    print("Bus ", self.id,", Processing passenger, count:", self.toprocess_num)
                self.toprocess_num -= self.process_rate
                self.toprocess_num = max(0, self.toprocess_num)
            else:

                if(self.hold_time>0):
                    if (debug_bus):
                        print("Bus ", self.id,", Hoding time, time:", self.hold_time)
                    self.hold_time -= 1
                    self.hold_time = max(0, self.hold_time)
                else:
                    self.pos = (self.pos + self.speed) % 360
                    self.at_stop = -1
                    self.is_feedback = False
        if debug_bus:
            print("Bus ",self.id, "is at stop:", self.at_stop)
        self.record()                                                       # 记录位移
    """
    def forward_spacing(self, bus_id, bus_list):
        forward=0
        if bus_id==self.bus_num-1:
             delta_degree=bus_list[0].pos-bus_list[bus_id].pos
        else:
             delta_degree=bus_list[bus_id+1].pos-bus_list[bus_id].pos
        if abs(delta_degree)<180:
            forward=(abs(delta_degree))
        else:
            forward=(360-abs(delta_degree))
        return forward

    def backward_spacing(self, bus_id, bus_list):
        backward=0
        if bus_id==0:
             delta_degree=bus_list[bus_id].pos-bus_list[-1].pos
        else:
             delta_degree=bus_list[bus_id].pos-bus_list[bus_id-1].pos
        if abs(delta_degree)<180:
            backward=(abs(delta_degree))
        else:
            backward=(360-abs(delta_degree))
        return backward
    """


    def spacing(self, bus_id, bus_list):
        spacing=[0]*self.bus_num
        own_pos=bus_list[bus_id].pos
        for i in range(self.bus_num):
            his_pos = bus_list[i].pos
            if(abs(own_pos-his_pos) <= 180):
                spacing[i] = -(own_pos-his_pos)
            else:
                if(his_pos < own_pos):
                    spacing[i] = - (own_pos-his_pos-360)
                else:
                    spacing[i] = - (own_pos-his_pos+180)
        return spacing
    """
    def spacing(self, bus_id, bus_list):
        spacing=[0]*self.bus_num
        own_pos=bus_list[bus_id].pos
        for i in range(self.bus_num):
            his_pos = bus_list[i].pos
            spacing[i] = own_pos-his_pos
        return spacing
    """

    def compute_reward(self, i,bus_list):
        reward = 0
        #delta00= 360/len(bus_list)/3

        if i==self.bus_num-1:
            forward = self.spacing(i, bus_list)[0]# 返回此车前面 distance
        else:
            forward = self.spacing(i, bus_list)[i+1]
        if i==0:
            backward = self.spacing(i, bus_list)[-1]# 返回此车后面 distance
        else:
            backward = self.spacing(i, bus_list)[i-1]

        if abs(forward)<=5 or abs(backward)<=5:
            reward = -1
        """
        #elif (forward) == -(backward):
        if ((forward-backward)-360/len(bus_list)*2)== 0:
            reward = 20
        else:
        """
        reward = 2*math.exp(-(abs((forward-backward)-360/len(bus_list)*2)/100))
        #reward += math.exp(self.hold_time)
        #reward += math.exp(-next_state[-1])   #DX

        return reward


    def record(self):                                                      #定义记录位移的函数
        self.trajectory.append(self.pos)



