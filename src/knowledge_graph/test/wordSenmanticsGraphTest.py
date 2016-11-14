# -*- coding: UTF-8 -*-

'''
Created on 2016年4月12日

@author: hylovedd
'''

import numpy

from orgknowledge_graphsicSemanticsGraph import BasicSemanticsGraph
from orgword_segrd2vec.wordTypeFilter import WordTypeFilter
from orgword_segrd2vec.wordVecOpt import WordVecOpt
from orgknowledge_graphxClustSemanticsGraph import LexClustSemanticsGraph
from orgtoolsche import ROOT_PATH


def createTestW2VModel():
    segFilePath = ROOT_PATH.root_win64 + 'weibo_seg\\segNLPCC2014Lite.txt'
    w2vModelPath = ROOT_PATH.root_win64 + 'model\\word2vec\\NLPCC2014Liteword2vecModel.vector'
    
    wordVecOptObj = WordVecOpt(w2vModelPath)
    model = wordVecOptObj.initTrainWord2VecModel(segFilePath)
    print(u'process corpus num :' + str(model.corpus_count))

def testBuildBasicSemGraph():
    segFilePath = ROOT_PATH.root_win64 + 'weibo_seg\\segNLPCC2014Lite.txt'
    w2vModelPath = ROOT_PATH.root_win64 + 'model\\word2vec\\NLPCC2014Liteword2vecModel.vector'
    
    allWordList = WordTypeFilter().collectAllWordsFromSegFile(segFilePath)
    BasicSemanticsGraph().buildBasicSemGraph(w2vModelPath, allWordList, 20, 0.2)
    
def testBuildLexGroupSemGraph():
    segFilePath = ROOT_PATH.root_win64 + 'weibo_seg\\segNLPCC2014Lite.txt'
    w2vModelPath = ROOT_PATH.root_win64 + 'model\\word2vec\\NLPCC2014Liteword2vecModel.vector'
    
    allWordList = WordTypeFilter().collectAllWordsFromSegFile(segFilePath)
    LexClustSemanticsGraph().buildLexGroupSemGraph(w2vModelPath, allWordList, vec_z_ratio=1000, canopy_t_ratio=2.05, topN_rev=20, topN=20, edgeThreshold=0.2)
    
if __name__ == '__main__':
#     createTestW2VModel()
#     testBuildBasicSemGraph()
#     vec = worWordVecOptNLPCC2014Liteword2vecModel.vector').getWordVecfromFile(u'欢迎/v')
#     print(numpy.array(vec) * 10000)
#     print(len(vec))
    testBuildLexGroupSemGraph()
