# -*- coding: UTF-8 -*-

'''
Created on 2016年3月17日

@author: superhy
'''

from org_ailab_seg.extraSegOpt import ExtraSegOpt
from org_ailab_seg.word2vec.wordVecOpt import WordVecOpt
from org_ailab_tools.cache import ROOT_PATH

def testTrainWord2VecModel():
    corpusFilePath = ROOT_PATH.root_win64 + 'weibo_seg\\segNLPCC2014.txt'
    modelPath = ROOT_PATH.root_win64 + 'word2vec\\NLPCC2014word2vecModel.vector'
    wordVecOptObj = WordVecOpt(modelPath)
    model = wordVecOptObj.initTrainWord2VecModel(corpusFilePath)
    print(u'process corpus num :' + str(model.corpus_count))
    wordStr = u'韩寒/nr'
    print(u'Train model and word vec object: ' + wordStr)
    queryList = wordVecOptObj.queryMostSimilarWordVec(model, wordStr)
    for e in queryList:
        print e[0], e[1]
    
def testQueryWordVec():
    modelPath = ROOT_PATH.root_win64 + 'word2vec\\NLPCC2014word2vecModel.vector'
    wordVecOptObj = WordVecOpt(modelPath)
    wordStr = u'韩寒/nr'
    print(u'Load model then word vec object: ' + wordStr)
    queryList = wordVecOptObj.queryMsimilarWVfromFile(wordStr)
    for e in queryList:
        print e[0], e[1]
        
    model = wordVecOptObj.loadModelfromFile(modelPath)
    print(u'\nmodel\'s corpus num:' + str(model.corpus_count))
    wordStr1 = u'韩寒/nr'
    wordStr2 = u'女人/n'  
    simRes = wordVecOptObj.culSimBtwWordVecs(model, wordStr1, wordStr2)
    print(u'\r\n' + wordStr1 + u' to ' + wordStr2 + u'\'similarity:')
    print(simRes)
    
    wordList1 = [u'韩寒/nr', u'可爱/v']
    wordList2 = []
    queryPNSimList = wordVecOptObj.queryMSimilarVecswithPosNeg(model, wordList1, wordList2, 30)
    print(u'\r\nPos: ' + u';'.join(wordList1) + u' Neg: ' + u';'.join(wordList2) + u'\'word vecs:')
    for e in queryPNSimList:
        # print type(e)
        print e[0], e[1]
    
if __name__ == '__main__':
#     testTrainWord2VecModel()
    testQueryWordVec()
