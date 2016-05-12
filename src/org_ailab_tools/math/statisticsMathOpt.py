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
    norm = probs - round(baseNum, 6) + 0.01
    return sum([abs(norm[datum] / p * math.log(norm[datum] / p)) for p in probs ])

if __name__ == '__main__':
#     p = numpy.max(x)
#     print(p)
#     s = [round(p, 6)] * 3
#     print s
#     a = numpy.array(s) - numpy.array(x)
#     print a[2]
    x1 = [6.23744053, 6.35333023, 1.33800801, 6.33826086]
    x2 = [137.31098967, 137.26085068, 144.53581023, 137.20453991]
    
    print(numpy.array(x1) + 0.1)
    print(numpy.array(x2) + [0.1] * len(x2))
    
    min_x1 = numpy.where(numpy.min(x1))
    min_x2 = numpy.where(numpy.min(x2))
    ent1 = shannonEnt(x1, min_x1)
    ent2 = shannonEnt(x2, min_x2)
    
    print(ent1)
    print(ent2)
