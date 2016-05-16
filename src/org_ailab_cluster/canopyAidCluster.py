# -*- coding: UTF-8 -*-
'''
Created on 2016年5月13日

@author: superhy
'''
from org_ailab_tools.math import statisticsMathOpt

class canopyAidCluster(object):
    def __init__(self, T1=None, T2=None):
        self._T1 = T1
        self._T2 = T2
        
    def aidClust(self, matrixDic, T_RATIO=2):
        '''
        
        '''
        if self._T2 == None:
            self._T2 = self.cntAvgThreshold(matrixDic, T_RATIO)
        
        points = []
        clusters = []
        for key in matrixDic:
            points.append((key, matrixDic[key]))
        
        while(len(points) != 0):
            cluster = []
            basePoint = points.pop()
            cluster.append(basePoint)
            for p in points:
                dis = statisticsMathOpt.euclideanMetric(basePoint[1], p[1])
                if dis < self._T2:
                    cluster.append(p)
                    points.remove(p)
            clusters.append(cluster)
            
        return len(clusters), clusters
    
    def cntAvgThreshold(self, matrixDic, T_RATIO):
        '''
        
        '''
        disSum = 0.0;
        for key in matrixDic:
            disSum += sum(0.0 if key == k else statisticsMathOpt.euclideanMetric(matrixDic[key], matrixDic[k]) for k in matrixDic)
        pNum = len(matrixDic) * (len(matrixDic) + 1) / 2
        return disSum / pNum / T_RATIO

if __name__ == '__main__':
    p = []
    p.append((1, [9, 9, 9]))
    print(p)
    s = p.pop()
    print(len(p))
