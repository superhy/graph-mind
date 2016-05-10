# -*- coding: UTF-8 -*-
'''
Created on 2016年5月9日

@author: superhy
'''

from kohonen import kohonen


class KohonenSOM(object):
    def __init__(self):
        self.lratemax = 0.8  # max learning rate
        self.lratemin = 0.05  # min learning rate
        self.rmax = 5.0

if __name__ == '__main__':
    ET = kohonen.ExponentialTimeseries
    
    '''
    
    ''' 
    def kwargs(shape=(2, 1), z=0.2):
        return dict(dimension=3,
                    shape=shape,
                    learning_rate=ET(-5e-4, 1, 0.1),
                    noise_variance=z)

    kw = kwargs()
    m = kohonen.Map(kohonen.Parameters(**kw))
    m.learn((80, 90, 90))
    m.learn((100, 90, 90))
    m.learn((80, 90, 80))
    m.learn((70, 90, 100))
    m.learn((80, 90, 90))
    m.learn((100, 90, 90))
    m.learn((80, 90, 80))
    m.learn((70, 90, 100))
    m.learn((80, 90, 90))
    m.learn((100, 90, 90))
    m.learn((80, 90, 80))
    m.learn((70, 90, 100))
    m.learn((3, 3, 2))
#     m.learn((3, 4, 3))
#     m.learn((4, 5, 3))
#     m.learn((5, 5, 3))
#     m.learn((3, 3, 2))
#     m.learn((3, 4, 3))
#     m.learn((4, 5, 3))
#     m.learn((5, 5, 3))
#     m.learn((3, 3, 2))
#     m.learn((3, 4, 3))
#     m.learn((4, 5, 3))
#     m.learn((5, 5, 3))
    
    print(m.winner((4, 4, 4)))
    print(m.winner((5, 5, 2)))
    print(m.winner((90, 90, 80)))
    print(m.winner((70, 90, 80)))
    print(m.winner((5, 5, 3)))
    print(m.distances((4, 4, 4)))
    print(m.distances((5, 5, 2)))
    print(m.distances((90, 90, 80)))
    print(m.distances((70, 90, 80)))
    print(m.distances((5, 5, 3)))
    print('----------------------------------------')
    print(m.neuron(0))
#     print(m.neuron(1))
