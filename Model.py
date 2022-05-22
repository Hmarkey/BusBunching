# -*- coding: UTF-8 -*-

class Model():
    def __init__(self, method, common):
        self.method = method
        self.env = common['Env']
        self.episode = common['episode']
        self.train_data = common['train_data']
        self.test_data = common['test_data']

    '''
    对输入的预处理
    '''
    def preprocess(self):
        pass

    '''
    对输出的预处理
    '''
    def postprocess(self):
        pass

    '''
    方法的训练过程
    '''
    def train(self):
        pass

    '''
    方法的测试过程
    '''
    def test(self):
        pass

    '''
    显示参数
    '''
    def showparams(self):
        pass
