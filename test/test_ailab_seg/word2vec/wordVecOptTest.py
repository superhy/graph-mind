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
    wordStr = u'韩寒/nr'
    print(u'Train model and word vec object: ' + wordStr)
    queryList = wordVecOptObj.queryMostSimilarWordVec(model, wordStr)
    for e in queryList:
        print e[0], e[1]
    
def testQueryWordVec():
    modelPath = u'NLPCC2014word2vecModel.vector'
    wordVecOptObj = wordVecOpt(modelPath)
    wordStr = u'韩寒/nr'
    print(u'Load model then word vec object: ' + wordStr)
    queryList = wordVecOptObj.queryMsimilarWVfromFile(wordStr)
    for e in queryList:
        print e[0], e[1]
        
    model = wordVecOptObj.loadModelfromFile(modelPath)
    wordStr1 = u'韩寒/nr'
    wordStr2 = u'女人/n'  
    simRes = wordVecOptObj.culSimBtwWordVecs(model, wordStr1, wordStr2)
    print(u'\r\n' + wordStr1 + u' to ' + wordStr2 + u'\' similarity:')
    print(simRes)
    
    queryNSimList = wordVecOptObj.queryNSimBtwWordVecs(model, wordStr1, wordStr2)
    print(queryNSimList)
    
if __name__ == '__main__':
    #testTrainWord2VecModel()
    testQueryWordVec()