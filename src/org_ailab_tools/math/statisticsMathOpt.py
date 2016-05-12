# -*- coding: UTF-8 -*-
'''
Created on 2016年5月12日

@author: superhy
'''

import math

import numpy


def shannonEnt(probList, datum):
    '''
    
    '''
    
    probs = numpy.array(probList)
    baseNum = numpy.min(probList)
    norms = probs - baseNum + 0.1
    return sum([abs(norms[datum] / p * math.log(norms[datum] / p)) for p in norms ])

if __name__ == '__main__':
#     p = numpy.max(x)
#     print(p)
#     s = [round(p, 6)] * 3
#     print s
#     a = numpy.array(s) - numpy.array(x)
#     print a[2]
    x1 = [9.20595052, 1.48028894]
    x2 = [130.90174515, 138.72282131]
    
    print(numpy.array(x1) + 0.1)
    print(numpy.array(x2) + [0.1] * len(x2))
    
    min_x1 = x1.index(numpy.min(x1))
    min_x2 = x2.index(numpy.min(x2))
    print((min_x1, min_x2))
    ent1 = shannonEnt(x1, min_x1)
    ent2 = shannonEnt(x2, min_x2)
    
    print(ent1)
    print(ent2)
