# coding=utf-8
"""
Reinforcement learning bus bunching.

Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].
"""

from Env import Env
from RL import QLearning
import random
import copy
import math
import matplotlib.pyplot as plt
from plot import plot_trajactory,plot_spacing,plot_reward,sav,plot_arrival,polyfit_reward, plot_accu
import numpy as np
import pandas as pd
#import dill                            #pip install dill --user
#filename = 'runsave.pkl'
#dill.dump_session(filename)
# and to load the session again:dill.load_session(filename)


#random.seed(0)
debug=False
debug_env= False
debug_bus = False
debug_stop= False
#debug=True


def action_str2num(action_str):
    pass


def train(count, env, RL,reward_train,reward_train_list):

    for episode in range(count):
        print("######### Train Episode ", episode, " #########")
        # initial observation       [d1,d2,d3,pos,num]
        cnt=0
        reward_train=0
        observation = env.reset(max_timestep)                   ## 随着时间步变化的State，不一定有效
        valid_observation = "start"             ## 记录有效的State
        if debug_env:
            print("Valid:   ", valid_observation)
        action = [0]*env.bus_num

        while  env.is_end() == False:
            if debug_env:
                print("Time Step: ", env.current_time)


            if(env.need_feedback()):          ## 此时到达了下一个车站，需要反馈，即获得reward，更新Q值表
                cnt+=1
                # RL take action and get next observation and reward
                reward = env.compute_reward()
                if i==0:
                    reward_train = reward_train + reward
                    # print("bus 0, action ", action[i], ", reward ", reward)
                #reward = env.bus_list[i].get_reward(observation[i])
                # RL learn from this transition
                if(debug_env):
                    print(str(valid_observation[i]))
                #if(valid_observation[i])
                if(cnt>1):
                    RL[i].learn(str(valid_observation), str(action), reward, str(observation))
                
                if(env.need_decision()):       ## 此时需要做出决定，即等待多长时间
                    valid_observation = copy.deepcopy(observation)
                    action_str = RL.choose_action(str(valid_observation))       ## return a string, need convert list
                    action_num = action_str2num(action_str)
                    env.notify_bus_process(action_num)
            
            observation = env.step()
            if observation == 'terminal':
                break
        reward_train_list.append(reward_train)



    for i in range(len(RL)):
        Q_trained.append(RL[i].q_table)
        (RL[i].q_table).to_csv(str(i)+".csv")
        if(debug):
            print("Q_table:", RL[i].q_table)
    print(Q_trained)


def test(count, env, RL,reward_test,reward_test_list):
    for episode in range(count):
        reward_test=0
        print("######### Test Episode ", episode, " #########")
        observation = env.reset(test_timestep)                   ## 随着时间步变化的State，不一定有效
        valid_observation = env.reset(test_timestep)         ## 记录有效的State
        action = [0]*env.bus_num
        while  env.is_end() == False:
            for i in range(len(RL)):
                if(env.need_feedback(i)):          ## 此时到达了下一个车站，需要反馈，即获得reward，更新Q值表
                    reward = env.bus_list[i].compute_reward(i,env.bus_list)
                    reward_test = reward_test + reward
                    if(env.need_decision(i)):       ## 此时需要做出决定，即等待多长时间
                        valid_observation[i] = copy.deepcopy(observation[i])
                        action[i] = RL[i].test_choose_action(str(valid_observation[i]))
                        env.notify_bus_process(i, action[i])
            observation = env.step()
        reward_test_list.append(reward_test)



def no_control(count, env):
    action = [0]*env.bus_num
    for episode in range(count):
        while  env.is_end() == False:
            #print("Time Step: ", env.current_time)
            for i in range(env.bus_num):
                env.notify_bus_process(i, action[i])
            env.step()


def originate_action_list(bus_num, action_num):
    action_list = []
    for i in range(action_num):
        for j in range(action_num):
            for k in range(action_num):
                action_list.append([i,j,k])

    return action_list


if  __name__ == "__main__":
    # env bus stop parameter:
    r = 5   # radius of the ring
    bus_stop_num = 5
    bus_stop_id = list(range(bus_stop_num))
    stop_pos= [i*360/bus_stop_num for i in range(bus_stop_num)]
    board_rate = 10
    arrive_rate = 1.2   #lambda of possion
    init_person = 2   #at bus stop
    # bus parameter:
    bus_num = 3
    init_delta = 360/bus_num
    init_pos = [i*init_delta-math.ceil(init_delta/3) for i in range(1,bus_num+1)]   ##DX 不在公交站的初始化
    init_atstop = [-1]*bus_num
    # init_pos = random.sample(bus_stop_id, bus_num)   #DX不应该是random
    class_num = 5 #bus_stop_num     # class of delta degree
    bus_speed = 8
    # control parameter:
    method = "Q-Learning"  #"No_control"   #"Q-Learning"
    episode = 100                  ## 训练的次数
    test_episode = 1                   ## 训练的次数
    state_dim = bus_num    ##
    action_dim = 5
    action_list = originate_action_list(bus_num, action_num)
    Q_action = list(i*10 for i in range(1,action_dim+1))  # [10, 20, 30]
    max_timestep = 500                 ## 训练时间
    test_timestep = 500
    RL = [0]*bus_num    #Q learning 的 对象，每个公交车
    Q_trained=[]   #Q learning 的 poilcy

    # reward
    reward_train=0
    reward_train_list=[]
    reward_test=0
    reward_test_list=[]
    # 对象
    '''
    Env __init__
    (self, method, speed, state_dim, action_dim, bus_num, bus_stop_num, stop_pos, r, max_timestep, init_pos, init_atstop, init_person, class_num, board_rate, arrive_rate):
    '''
    env = Env(method, bus_speed, state_dim, action_dim, bus_num, bus_stop_num,
            stop_pos, r, max_timestep, init_pos, init_atstop, init_person,class_num,
            board_rate, arrive_rate )
    if method == "Q-Learning":

        RL = QLearning(actions=action_list) # [0 1 2]
        train(episode, env, RL,reward_train,reward_train_list)
        sav(Q_trained)
        plot_reward(method, reward_train_list)
        #polyfit_reward(method, reward_train_list)
        plt.title("Learning Process")




    env1 = Env(method, bus_speed, state_dim, action_dim, bus_num, bus_stop_num,
    stop_pos, r, max_timestep, init_pos, init_atstop, init_person,class_num,
    board_rate, arrive_rate )
    test(test_episode, env1,RL,reward_test,reward_test_list)
    plot_trajactory(method,bus_num,env1.bus_list)
    plot_spacing(method,bus_num,env1.bus_list,RL,max_timestep)
    plot_accu(method,bus_stop_num,env.bus_stop_list)
        #plot_reward(method, reward_test_list)
    env2 = Env(method, bus_speed, state_dim, action_dim, bus_num, bus_stop_num,
    stop_pos, r, max_timestep, init_pos, init_atstop, init_person,class_num,
    board_rate, arrive_rate )
    #if method == "No_control" :
    method2 = "No_control"
    no_control(1, env2)
    plot_trajactory(method2,bus_num,env2.bus_list)
    plot_spacing(method2,bus_num,env2.bus_list,RL,max_timestep)
    plot_accu(method2,bus_stop_num,env.bus_stop_list)

#plot_arrival(method, bus_stop_num, env.bus_stop_list)
    #plot_arrival(method,bus_stop_num,env.bus_stop_list)

#   Toload the parameter:    Qrecord=pd.read_csv(str(0)+".csv")


