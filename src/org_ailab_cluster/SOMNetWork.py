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
                    learning_rate=ET(-5e-4, 1, 0.01),
                    noise_variance=z)

    kw = kwargs()
    m = kohonen.Map(kohonen.Parameters(**kw))
    print("neuron1: \n" + str(m.neuron(0)))
    print("neuron2: \n" + str(m.neuron(1)))
    print('----------------------------------------')
    m.learn((80, 90, 90))
    m.learn((100, 90, 90))
    m.learn((80, 90, 80))
    m.learn((71, 90, 103))
    m.learn((82, 93, 90))
    m.learn((101, 95, 90))
    m.learn((83, 90, 85))
    m.learn((74, 92, 99))
    m.learn((85, 91, 90))
    m.learn((98, 98, 90))
    m.learn((81, 95, 88))
    m.learn((77, 96, 100))
    m.learn((3, 3, 2))
    m.learn((3, 4, 3))
#     m.learn((4, 5, 3))
#     m.learn((5, 5, 4))
#     m.learn((3, 5, 2))
#     m.learn((3, 3, 3))
#     m.learn((3, 5, 3))
#     m.learn((5, 5, 3))
#     m.learn((3, 3, 4))
#     m.learn((3, 4, 5))
#     m.learn((4, 5, 2))
#     m.learn((5, 2, 3))

    print('----------------------------------------')
    print("neuron1: \n" + str(m.neuron(0)))
    print("neuron2: \n" + str(m.neuron(1)))
    print('----------------------------------------')
    print(m.winner((3, 3, 2)))
    print(m.winner((5, 5, 3)))
    print(m.winner((80, 90, 90)))
    print(m.winner((80, 90, 80)))
    print(m.winner((71, 90, 103)))
    print(m.winner((5, 2, 3)))
    print(str(m.distances((3, 3, 2))) + ' /' + str(m.weights(m.distances((3, 3, 2)))))
    print(str(m.distances((5, 5, 3))) + ' /' + str(m.weights(m.distances((5, 5, 3)))))
    print(str(m.distances((90, 90, 80))) + ' /' + str(m.weights(m.distances((90, 90, 80)))))
    print(str(m.distances((70, 90, 80))) + ' /' + str(m.weights(m.distances((70, 90, 80)))))
    print(str(m.distances((71, 90, 103))) + ' /' + str(m.weights(m.distances((71, 90, 103)))))
    print(str(m.distances((5, 2, 3))) + ' /' + str(m.weights(m.distances((5, 2, 3)))))
    print('----------------------------------------')
    print("neuron1: \n" + str(m.neuron(0)))
    print("neuron2: \n" + str(m.neuron(1)))
