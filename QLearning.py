# -*- coding: UTF-8 -*-

"""
This part of code is the Q learning brain, which is a brain of the agent.
All decisions are made in here.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""

from Model import Model
import numpy as np
import pandas as pd
import copy


class QLearning:
    def __init__(self, common, actions, learning_rate=0.1, reward_decay=0.8, e_greedy=0.9):
        Model.__init__(self, 'QLearning', common)
        self.actions = actions  # a string list 
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

        self.reward_train_list = []

    def choose_action(self, observation):
        self.check_state_exist(observation)
        # action selection
        if np.random.uniform() < self.epsilon:
            # choose best action
            state_action = self.q_table.loc[observation, :]
            # some actions may have the same value, randomly choose on in these actions
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        else:
            # choose random action
            action = np.random.choice(self.actions)
        return action

    def learn(self, s, a, r, s_):
        self.check_state_exist(s)
        self.check_state_exist(s_)          
        q_predict = self.q_table.loc[s, a]
        if s_ != 'terminal':
            q_target = r + self.gamma * self.q_table.loc[s_, :].max()  # next state is not terminal
        else:
            q_target = r  # next state is terminal
        self.q_table.loc[s, a] += self.lr * (q_target - q_predict)  # update

    def test_choose_action(self, observation):
        if observation not in self.q_table.index:
            return 0
        # action selection
        state_action = self.q_table.loc[observation, :]
        # some actions may have the same value, randomly choose on in these actions
        action = np.random.choice(state_action[state_action == np.max(state_action)].index)

        return action

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table
            self.q_table = self.q_table.append(
                pd.Series(
                    [-100]*len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )

    def preprocess(self):
        pass

    def postprocess(self):
        pass

    def train(self):
        #def train(count, env, RL,reward_train,reward_train_list):
        ## 全局参数
        max_timestep = self.env.max_timestep


        for episode in range(self.episode):
            print("######### Q-Learning Train Episode ", episode, " #########")
            # initial observation       [d1,d2,d3,pos,num]
            cnt=0
            reward_train=0

            observation = self.env.reset(max_timestep)  ## 随着时间步变化的State，不一定有效
            valid_observation = "start"                 ## 记录有效的State
            action = [0]*self.env.bus_num

            while  self.env.is_end() == False:
                if(self.env.need_feedback()):           ## 此时到达了下一个车站，需要反馈，即获得reward，更新Q值表
                    cnt+=1
                    # RL take action and get next observation and reward
                    reward = self.env.compute_reward()
                    reward_train += reward
                    if(cnt>1):
                        self.learn(str(valid_observation), str(action), reward, str(observation))
                    
                    # 此时需要做出决定，即等待多长时间
                    if(self.env.need_decision()):                       
                        valid_observation = copy.deepcopy(observation)
                        # return a string, need convert list
                        action_str = self.choose_action(str(valid_observation))       
                        action_num = self.action_str2num(action_str)
                        self.env.notify_bus_process(action_num)
                
                observation = self.env.step()
                if observation == 'terminal':
                    break
            self.reward_train_list.append(reward_train)
    

    def test(self):
        pass

    def action_str2num(self, action_str):
        temp = action_str[1:-1]
        action = temp.split(',')
        assert len(action)==self.env.bus_num
        for i in range(len(action)):
            action[i] = float(action[i])
        return action