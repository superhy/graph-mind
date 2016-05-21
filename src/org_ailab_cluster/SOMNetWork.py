# -*- coding: UTF-8 -*-
'''
Created on 2016年5月9日

@author: superhy
'''

from kohonen import kohonen
import numpy

from org_ailab_tools.math import statisticsMathOpt
from org_ailab_cluster.canopyAidCluster import canopyAidCluster


class KohonenSOM(object):
    def __init__(self, dimension, shape=None, rate=-5e-4, initial=1, final=0.1, noise_variance=0.05):
        self._dimension = dimension
        self._shape = shape
        self._rate = rate
        self._initial = initial
        self._final = final
        self._noise_variance = noise_variance
        
    def prodMapModel(self, matrixDic, canopy_t_ratio):
        ET = kohonen.ExponentialTimeseries
        
        if self._shape == None:
            N, clusters = canopyAidCluster().aidClust(matrixDic, canopy_t_ratio)
            
            print('canopy aid-clust res:')
            print('N: ' + str(N))
            print('clusters:')
            for cluster in clusters:
                print(cluster)
                
            f = int(numpy.sqrt(N))
            while(N % f != 0):
                f -= 1
            self._shape = (N / f, f)

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
        
    def clust(self, matrixDic, canopy_t_ratio = 2):
        '''
        input matrix dic: key is id of feature element(id); value is vector of feature element(vec)
        '''
        
        self.prodMapModel(matrixDic, canopy_t_ratio)
        
        # train the cluster model
        for key in matrixDic:
            self._model.learn(matrixDic[key])
        
#         def neuFlatShapMap(neuId, shape):
#             return neuId / shape[0], neuId % shape[0]

        def matIntoList(mat):
            disList = []
            for i in range(self._shape[0]):
                for j in range(self._shape[1]):
                    disList.append(d[i][j])
            return disList
        
        clustResDic = {}
        clusters = [[] for i in range(self._shape[0] * self._shape[1])]
        for key in matrixDic:
            w = self._model.winner(matrixDic[key])
            d = self._model.distances(matrixDic[key])
            
            dList = matIntoList(d)
            dAve = numpy.average(dList)
            weight = dAve - dList[w]
            ent = statisticsMathOpt.shannonEnt(dList, w)
            #
            clustResDic[key] = (w, weight, ent)
            #
            clusters[w].append((key, w, weight, ent))
        
        return clusters, clustResDic

if __name__ == '__main__':
    '''
    some basic test
    '''
    
    som = KohonenSOM(3)
    print('called res:')
    matrixDic = {0 : [80, 90, 90],
                 1 : [100, 90, 90],
                 2 : [80, 90, 80],
                 4 : [70, 90, 100],
                 5 : [80, 90, 90],
                 6 : [100, 90, 90],
                 7 : [80, 90, 80],
                 8 : [70, 90, 100],
                 9 : [80, 90, 90],
                 10 : [100, 90, 90],
                 11 : [80, 90, 80],
                 12 : [70, 90, 100],
                 13 : [3, 3, 2],
                 14 : [3, 4, 3]}
    clusters, clustResDic = som.clust(matrixDic)
    print(som._shape)
    print(clustResDic)
    for cluster in clusters:
        print(cluster)
    print('----------------------------------------')
    m = som.prodMapModel(matrixDic, 2)
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
    print(m.winner([3, 3, 2]))
    print(m.winner([80, 90, 80]))
    print(m.winner([70, 90, 80]))
    print(m.winner([5, 5, 3]))
    print(m.distances([4, 4, 4]))
    print(m.distances([3, 3, 2]))
    print(m.distances([80, 90, 80]))
    print(m.distances([70, 90, 80]))
    print(m.distances([5, 5, 3]))
    print('----------------------------------------')
    print(m.distances([5, 5, 3])[0][0])
    print(m.weights(m.distances([5, 5, 3])))
    print('----------------------------------------')
    print(m.neuron(0))
    print(m.neuron(1))
#     print(m.neuron(2)[0])
