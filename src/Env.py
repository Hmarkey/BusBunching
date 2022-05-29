# coding=utf-8
import numpy as np
import math
from BUS import bus
from BUS_STOP import bus_stop

debug_env=False
debug_bus=False
debug_stop=False
#debug=True
class Env():
    '''
    state_dim :        dimension of state space
    action_dim:        dimension of action space
    bus_num:           number of bus
    bus_stop_num:      number of bus stop
    r:                 radius of bus corridor
    emit_time_list:    schedule of bus departure
    bus_dep_list:      bus departure location list
    bus_stop_loc_list: bus stop location list
    arrival_schedule:  schedule arrival time of next stop for a bus. Rolling update
    update_step:       simulation update step, update_step=0.01 indiactes simulation run every 0.01 second
    sim_horizon:       length of simulation /seconds
                       Noted: 1 second sim_horizon = 1/update_step seconds in reality
    cooridor_radius:   the radius of the bus corridor
    check_step :       check system state every 3 second(5 min in real world),includng service level of bus
    arrival_bias:      bias between actural arrival and arrival schedule for each bus on every stip

    '''

    def __init__(self, method, speed, state_dim, action_dim, bus_num, bus_stop_num, stop_pos , r, max_timestep, init_pos, init_atstop, init_wait_person, class_num, board_rate, arrive_rate):
        ### my code
        self.method = method                        ## 采用的方法
        self.speed = speed
        self.state_dim = state_dim                  ## 每辆车的state的维度
        self.action_dim = action_dim
        self.bus_stop_num = bus_stop_num
        self.bus_num = bus_num
        self.board_rate = board_rate                ## 乘客上车速度
        self.arrive_rate = arrive_rate              ## 乘客到达速度
        self.r = r                    ## 轨道半径
        self.max_timestep = max_timestep            ## 公车系统运行的最大时间步数
        self.init_pos = init_pos                    ## 各个公车初始位置
        self.init_atstop = init_atstop              ## 各个公车是否在站
        self.init_wait_person = init_wait_person         ## 各个车站等待乘客人数的初始化
        self.stop_pos = stop_pos      ## 公交站位置
        self.class_num = class_num                  ## 将车辆之间的角度差进行分类（即离散化）的类别数量，
        self.bus_list = []
        self.bus_stop_list = []
        self.current_time = 0                       ## 当前的时间步
        self.init_state = []

        '''
        bus __init__
        (self, id, speed, process_rate, at_stop, pos, pass_num, action_num, start_stop, bus_nums, stop_nums, stop_pos):

        stop __init__
        (self, id, pos,bus_nums,arr_rate, process_rate, wait_num,wait_accumulate=[0])
        '''
        if debug_stop:
            print("Initial Waiting passenger:", self.init_wait_person)
        for i in range(bus_num):
            b = bus(i, speed, board_rate, init_atstop[i], init_pos[i], 0, action_dim, init_atstop[i], bus_num, self.bus_stop_num, self.stop_pos)
            self.bus_list.append(b)

        for i in range(bus_stop_num):
            bs = bus_stop(i, bus_stop_num, i*360/bus_stop_num, bus_num, arrive_rate, board_rate, init_wait_person)
            self.bus_stop_list.append(bs)

        for bus_id in range(self.bus_num):
            self.init_state.append(self.get_observation(bus_id))

        if debug_env:
            print("Envionment is initialized successfully.")

    '''
    随时间步更新主函数：走一个step，系统应该做出的变化
    返回step后系统的状态
    '''
    def step(self):
        self.current_time += 1
        if (debug_env):
            print('################# Step: %d' % self.current_time," #################")
        state_space = [0]*self.bus_num

        for i in range(self.bus_num):
            self.bus_list[i].step()
        for i in range(self.bus_stop_num):
            self.bus_stop_list[i].step()
            if debug_stop:
                print("BUS Stop", i ,"IS SERVED?",self.bus_stop_list[i].is_served)

        ## 根据step后公车的状态更新车站的状态，主要是is_serverd和actual_bus_arr
        """ ## 先把车站的参数全部重置为0//DXstep函数中已有此功能
        for i in range(self.bus_stop_num):
            self.bus_stop_list[i].is_served = 0
            self.bus_stop_list[i].actual_bus_arr = [0]*self.bus_num
        """
        for i in range(self.bus_num):                           ## 根据公车状态更新公交站
            if(self.bus_list[i].at_stop != -1):
                stop_id = self.bus_list[i].at_stop
                self.bus_stop_list[stop_id].is_served = 1
                self.bus_stop_list[stop_id].actual_bus_arr[i] = 1   ## DX其实这里应该不是很对
                state_space[i] = self.get_observation(i)

        return state_space



    def get_observation(self, base_degree, base_pax):
        for i in range(self.bus_num):
            if(ifbb_occurs(i, 2)):
                return 'terminal'

        observation = [0] * (self.bus_num+self.bus_stop_num) 

        for i in range(self.bus_num):
            observation[i] = self.bus_list[i].pos // base_degree

        for j in range(self.bus_num, len(observation)):
            observation[j] = match.ceil(self.bus_stop_list[j-self.bus_num].wait_num / base_pax)

        if debug_bus:
            print("Bus ", bus_id, "'s observation is ",observation)
        return observation

    '''
    判断是否结束系统运行
    '''
    def is_end(self):
        if(self.current_time > self.max_timestep):
            return True
        else:
            return False
    '''
    判断当前bus_id是否需要做出hold time的决策
    判断条件为：如果公车在公交车站，并且还没有做出过决策（hold_time==0），那么就需要
    '''
    def need_decision(self, bus_id):
        if(self.bus_list[bus_id].at_stop != -1 and self.bus_list[bus_id].is_feedback == False):
            return True
        else:
            return False


    '''
    判断当前bus_id是否需要需要更新Q值表，即需要反馈上次决策的reward
    判断条件为
    实际上没做决策意味着刚到达公交车站
    '''
    def need_feedback(self, bus_id):
        if(self.current_time == 0):     ## 刚开始，不需要反馈
            return False

        if(self.bus_list[bus_id].at_stop != -1 and self.bus_list[bus_id].is_feedback == False):   ###
            return True
        return False

    '''
    通知bus_id的公交车开始处理
    '''
    def notify_bus_process(self, bus_id, wait_step):

        serverd_stop = self.bus_list[bus_id].at_stop
        self.bus_list[bus_id].hold_time = wait_step *1
        self.bus_list[bus_id].toprocess_num = self.bus_stop_list[serverd_stop].wait_num
        self.bus_list[bus_id].is_feedback = True  #DX 这里应该初始化为T吗？True
        print("currrent: ", self.current_time, "bus ", bus_id, ", at stop ", serverd_stop, ", toprocess_num: ", self.bus_list[bus_id].toprocess_num)
        if debug_bus:
            print("Bus ", bus_id, "'is feed back? ", self.bus_list[bus_id].is_feedback)

    '''
    重置系统，只有在被训练时才会被调用 (公交、车站的重置，并记录初始state)
    '''
    def reset(self,max_timestep):
        self.current_time = 0
        self.bus_list = []
        self.bus_stop_list = []
        self.max_timestep = max_timestep
        if debug_stop:
            print("Initial Waiting passenger:", self.init_wait_person)
        for i in range(self.bus_num):
            b = bus(i, self.speed, self.board_rate,
                self.init_atstop[i],self.init_pos[i],
                0, self.action_dim, self.init_atstop[i] ,self.bus_num, self.bus_stop_num,self.stop_pos)
            self.bus_list.append(b)

        for i in range(self.bus_stop_num):
            bs = bus_stop(i, self.bus_stop_num, i*360/self.bus_stop_num, self.bus_num, self.arrive_rate,
                self.board_rate, self.init_wait_person)
            self.bus_stop_list.append(bs)
            if debug_stop:
                print("BUS stop", i, "Initial Waiting passenger:", self.bus_stop_list[i].wait_num)

        
        init_state = get_observation()

        return init_state


    def ifbb_occurs(self, bus_id, delta0):
        count_delta=0

        for i in range(self.bus_num):
            if(i == bus_id):
                continue
            if abs(self.bus_list[i].pos - self.bus_list[bus_id].pos) <= delta0:
                count_delta = 1
                if count_delta>=1:
                    return True
        return False








