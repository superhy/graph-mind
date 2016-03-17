# -*- coding: UTF-8 -*-

'''
Created on 2016年3月17日

@author: superhy
'''
from org_ailab_seg.word2vec.wordVecOpt import wordVecOpt
from org_ailab_seg.advanceSegOpt import advanceSegOpt


def testTrainWord2VecModel():
    corpusFilePath = u"../segNLPCC2014.txt"
    corpusFile = open(corpusFilePath, u'r')
    modelPath = u'NLPCC2014word2vecModel.vector'
    wordVecOptObj = wordVecOpt(modelPath)
    model = wordVecOptObj.trainWord2VecModel(corpusFilePath)
    wordStr = u'调戏/v'
    print(u'word vec object: ' + wordStr)
    queryList = wordVecOptObj.queryMostSimilarWordVec(model, wordStr)
    for e in queryList:
        print e[0], e[1]
    
def testQueryWordVec():
    advanceSegOptObj = advanceSegOpt()
    advanceSegOptObj.reLoadEncoding()
    filePath = u"../segNLPCC2014.txt"
    file = open(filePath, u'r')
    modelPath = u'NLPCC2014word2vecModel.vector'
    wordVecOptObj = wordVecOpt(filePath, modelPath)
    wordStr = u'调戏'
    wordVecOptObj.queryMsimilarWVfromFile(modelPath, wordStr)
    
if __name__ == '__main__':
    testTrainWord2VecModel()
    #testQueryWordVec()