# -*- coding: UTF-8 -*-

class Model():
    def __init__(self, method):
        self.method = method

    def preprocess(self):
        print("class ", Model.__name__)

    def print(self):
        print("parent ", self.method)

class RL(Model):
    def __init__(self, method, name):
        Model.__init__(self, method)
        self.name = name

    def preprocess(self):
        print("class ", RL.__name__)
        print("class ", self.name)
        print("method ", self.method)

if __name__ == '__main__':
    rl = RL("Q-learning", 'RL')
    rl.preprocess()
    rl.print()