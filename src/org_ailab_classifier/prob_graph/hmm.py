# -*- coding: UTF-8 -*-

'''
Created on 2016年6月2日

@author: hylovedd
'''
from numpy import multiply, argmax

class HiddenMarkov(object):
    def __init__(self, startP, transP, emitP):
        self._startP = startP
        self._transP = transP
        self._emitP = emitP
        
    def viterbi(self, obs, hiddens):
        '''
        input the obvious states sequence and the possible hidden states dictionary list
        return the forest result(a dictionary list)
        the dictionary's key is the most likely hidden state and the value is the probability
        '''
        V = [{}]  # 路径概率表 V[时间][隐状态] = 概率
        for y in hiddens:  # 初始时间点
            V[0][y] = self._startP[y] * self._emitP[y][obs[0]]
        for t in xrange(1, len(obs)):
            V.append({})
            for y in hiddens:
                # 概率 隐状态 = 前状态是y0的概率 * y0转移到y的概率 * y表现为当前状态的概率
                V[t][y] = max([(V[t - 1][y0] * self._transP[y0][y] * self._emitP[y][obs[t]]) for y0 in hiddens])
                
        result = []
        for vector in V:
            temp = {}
            temp[vector.keys() [argmax(vector.values())]] = max(vector.values())
            result.append(temp)
        
        return result

if __name__ == '__main__':
    pass
