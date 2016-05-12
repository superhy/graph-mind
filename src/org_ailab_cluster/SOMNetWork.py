# -*- coding: UTF-8 -*-
'''
Created on 2016年5月9日

@author: superhy
'''

from kohonen import kohonen


class KohonenSOM(object):
    def __init__(self, dimension, shape=None, rate=-5e-4, initial=1, final=0.1, noise_variance=0.05):
        self._dimension = dimension
        self._shape = shape
        self._rate = rate
        self._initial = initial
        self._final = final
        self._noise_variance = noise_variance
        
        self.prodMapModel()
        
    def prodMapModel(self):
        ET = kohonen.ExponentialTimeseries

        def kwargs(shape=self._shape, z=self._noise_variance):
            return dict(dimension=self._dimension,
                        shape=shape,
                        learning_rate=ET(self._rate, self._initial, self._final),
                        noise_variance=z)
        kw = kwargs()
        
        self._model = kohonen.Map(kohonen.Parameters(**kw))
        return self._model
    
    def resetModel(self):
        self._model.reset()
        
    def clust(self, matrixDic):
        '''
        input matrix dic: key is id of feature element(id); value is vector of feature element(vec)
        '''
        
        # train the cluster model
        for key in matrixDic:
            self._model.learn(matrixDic[key])
        
        def neuFlatShapMap(neuId, shape):
            return (neuId / shape[0], neuId % shape[0])
        

if __name__ == '__main__':
    '''
    some basic test
    '''
    
    som = KohonenSOM(3, (2, 2))
    m = som.prodMapModel()
    print('----------------------------------------')
    m.learn([80, 90, 90])
    m.learn([100, 90, 90])
    m.learn([80, 90, 80])
    m.learn([70, 90, 100])
    m.learn([80, 90, 90])
    m.learn([100, 90, 90])
    m.learn([80, 90, 80])
    m.learn([70, 90, 100])
    m.learn([80, 90, 90])
    m.learn([100, 90, 90])
    m.learn([80, 90, 80])
    m.learn([70, 90, 100])
    m.learn([3, 3, 2])
    m.learn([3, 4, 3])
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
    
    print(m.winner([4, 4, 4]))
    print(m.winner([5, 5, 2]))
    print(m.winner([90, 90, 80]))
    print(m.winner([70, 90, 80]))
    print(m.winner([5, 5, 3]))
    print(m.distances([4, 4, 4]))
    print(m.distances([5, 5, 2]))
    print(m.distances([90, 90, 80]))
    print(m.distances([70, 90, 80]))
    print(m.distances([5, 5, 3]))
    print('----------------------------------------')
    print(m.distances([5, 5, 3])[0][0])
    print(m.weights(m.distances([5, 5, 3])))
    print('----------------------------------------')
    print(m.neuron(0))
    print(m.neuron(1))
#     print(m.neuron(2)[0])