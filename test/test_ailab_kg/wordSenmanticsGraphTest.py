# -*- coding: UTF-8 -*-

'''
Created on 2016年4月12日

@author: hylovedd
'''

from org_ailab_kg.wordSemanticsGraph import wordSemanticsGraph
from org_ailab_seg.word2vec.wordTypeFilter import wordTypeFilter
from org_ailab_seg.word2vec.wordVecOpt import wordVecOpt


def createTestW2VModel():
    segFilePath = u'segNLPCC2014Lite.txt'
    w2vModelPath = u'NLPCC2014Liteword2vecModel.vector'
    
    wordVecOptObj = wordVecOpt(w2vModelPath)
    model = wordVecOptObj.initTrainWord2VecModel(segFilePath)
    print(u'process corpus num :' + str(model.corpus_count))

def testBuildBasicSemGraph():
    segFilePath = u'segNLPCC2014Lite.txt'
    w2vModelPath = u'NLPCC2014Liteword2vecModel.vector'
    
    allWordList = wordTypeFilter().collectAllWordsFromSegFile(segFilePath)
    wordSemanticsGraph().buildBasicSemGraph(w2vModelPath, allWordList, 20)

if __name__ == '__main__':
    #createTestW2VModel()
    testBuildBasicSemGraph()