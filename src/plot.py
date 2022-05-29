# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 14:35:21 2022

@author: Apple
"""

import matplotlib.pyplot as plt
import numpy as np
import numpy as np

#from scipy.interpolate import spline
#from sklearn.gaussian_process import GaussianProcess
#plt.style.use('seaborn-whitegrid')


def plot_trajactory(method,bus_nums,bus_list):
    plt.figure(figsize=(20,10))
    for j in range(bus_nums):
        plt.plot(bus_list[j].trajectory,label='Bus '+ str(j))
    plt.legend()
    if method == "Q-Learning":
        plt.title('Bus Trajactory with Q-Learning Method.')
    if method == "No_control":
        plt.title('Bus Trajactory without control.')
    plt.savefig(method + "trajactory.png")

def plot_arrival(method,bus_stop_num,bus_stop_list):
    plt.figure(figsize=(20,10))
    for j in range(bus_stop_num):
        plt.subplot(bus_stop_num,1,j)
        plt.plot(bus_stop_list[j].arrival_list,label='Bus Stop '+ str(j))
    plt.legend()
    if method == "Q-Learning":
        plt.title('Arrival passenger at Bus Stop with Q-Learning Method.')
    if method == "No_control":
        plt.title('Arrival passenger at Bus Stop without control.')
    plt.savefig(method + "arrival.png")

def plot_spacing(method,bus_nums,bus_list,RL,max_timestep):
    plt.figure(figsize=(20,10))
    spacing= [[] for i in range(bus_nums)]
    for j in range(bus_nums):
        for k in range(max_timestep):
            if j==bus_nums-1:
                 delta_degree=bus_list[0].trajectory[k]-bus_list[j].trajectory[k]
            else:
                 delta_degree=bus_list[j+1].trajectory[k]-bus_list[j].trajectory[k]
            if abs(delta_degree)<180:
                spacing[j].append(abs(delta_degree))
            else:
                spacing[j].append(360-abs(delta_degree))
    for j in range(bus_nums):
        if j==bus_nums-1:
            plt.plot(spacing[j],label='Spacing of Bus '+ str(j)+' and Bus 0')
        else:
            plt.plot(spacing[j],label='Spacing of Bus '+ str(j)+' and Bus '+ str(j+1))
    plt.legend()
    if method == "Q-Learning":
        plt.title('Bus Spacing with Q-Learning Method.')
    if method == "No_control":
        plt.title('Bus Spacing without control.')
    plt.savefig(method + "spacing.png")

def print_Q_Table(method,bus_nums,RL):
    if method == "Q-Learning":                                                  #####    DX
        for i in range(bus_nums):
            #print("Bus ",i, "'s trajactory is ", env.bus_list[i].trajectory)
            print("Bus ",i, "'s Q Table is ", RL[i].q_table)


def plot_accu (method,bus_stop_num,bus_stop_list):
    plt.figure(figsize=(20,10))
    for j in range(bus_stop_num):
        plt.subplot(bus_stop_num,1,j+1)
        plt.plot(bus_stop_list[j].wait_accumulate_list ,label='Bus Stop'+ str(j))
        plt.legend()
    plt.tight_layout()
    if method == "Q-Learning":
        plt.title(' Accumulation of passengers at Bus Stop with Q-Learning Method.')
    if method == "No_control":
        plt.title('Bus Stop Accumulation without control.')
    plt.savefig(method + "arrival.png")

def plot_reward (method, reward_list):
    plt.figure(figsize=(20,10))
    x=list(range(len(reward_list)))
    #xnew = np.linspace(min(x),max(x),len(reward_list)*1000)
    #reward_smooth = spline(x,reward_list,xnew)
    plt.plot(x ,reward_list,'gray')
    plt.plot(x, reward_list, 'ob')
    #plt.scatter(list(range(len(reward_list))),reward_list)
    plt.xlabel('Episode')
    plt.ylabel('reward')
    if method == "Q-Learning":
        plt.title(' Reward with Q-Learning Method.')
    if method == "No_control":
        plt.title(' Reward without control.')
    plt.savefig(method + "reward0.png")


def sav(listtosave):
    list_log = [listtosave]
    file= open('log.txt', 'w')
    for fp in list_log:
        file.write(str(fp))
        file.write('\n')
    file.close()
    """
    numpy_array=np.array(listtosave)
    np.save('log.npy',numpy_array )
    """

def polyfit_reward(method, reward_list):
    x=np.array(range(len(reward_list)))
    y=reward_list

    coefficients = np.polyfit(x, y, 2)
    c = coefficients[0] * x *x  + coefficients[1]*x + coefficients[2]
    #plt.figure(figsize=(20,10))
    plt.plot(x, y, 'ob')
    #plt.plot(x, c,'r')
    #dy=0.05
    #plt.errorbar(x, c, yerr=dy, fmt='.k')

    """
    #计算高斯过程拟合结果
    gp = GaussianProcess(corr='cubic', theta0=1e-2, thetaL=1e-4, thetaU=1E-1,
                         random_start=100)
    gp.fit(x[:, np.newaxis], y)

    xfit = np.linspace(0, len(reward_list), 1000)
    yfit, MSE   = gp.predict(xfit[:, np.newaxis], eval_MSE=True)
    dyfit = 2 * np.sqrt(MSE)    #s*sigma~95%的置信区间
    plt.fill_between(xfit, yfit - dyfit, yfit+dyfit, color='gray', alpha=0.2)
    """

    """
    #log
    log_x = np.log(range(len(reward_list)))
    log_y = np.log(reward_list)
    coefficients = np.polyfit(log_x, y, 1)
    print(coefficients)
    c = coefficients[0] * log_x + coefficients[1]
    plt.plot(log_x, y, "o")
    plt.plot(log_x, c)
    """