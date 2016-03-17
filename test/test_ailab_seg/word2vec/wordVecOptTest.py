# -*- coding: UTF-8 -*-

'''
Created on 2016年3月17日

@author: superhy
'''
from org_ailab_seg.word2vec.wordVecOpt import wordVecOpt


def testTrainWord2VecModel():
    filePath = u"../segNLPCC2014.txt"
    file = open(filePath, u'r')
    modelPath = u'NLPCC2014word2vecModel.txt'
    wordVecOptObj = wordVecOpt(filePath, modelPath)
    wordVecOptObj.trainWord2VecModel()
    
if __name__ == '__main__':
    testTrainWord2VecModel()