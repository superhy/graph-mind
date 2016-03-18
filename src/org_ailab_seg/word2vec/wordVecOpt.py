# -*- coding: UTF-8 -*-

'''
Created on 2016年3月17日

@author: superhy
'''

import os
import warnings

from Cython.Build.Cythonize import multiprocessing
from gensim.models.word2vec import Word2Vec, LineSentence

from org_ailab_load import loadLocalFileData
from org_ailab_seg.advanceSegOpt import advanceSegOpt


class wordVecOpt:
    def __init__(self, modelPath, _size=100, _window=5, _minCount=1, _workers=multiprocessing.cpu_count()):
        self.modelPath = modelPath
        self._size = _size
        self._window = _window
        self._minCount = _minCount
        self._workers = _workers
    
    def loadModelfromFile(self, modelFilePath):
        return Word2Vec.load(modelFilePath)
    
    def trainWord2VecModel(self, corpusFile):
        advanceSegOpt().reLoadEncoding()
        fileType = loadLocalFileData.checkFile(corpusFile)
        if fileType == u'null' or fileType == u'error':
            warnings.warn('load file error!')
        else:
            model = Word2Vec(LineSentence(corpusFile), size=self._size, window=self._window, min_count=self._minCount, workers=self._workers)
            model.save(self.modelPath)
            model.init_sims(replace=True)
            print('producing word2vec model ... ok')
            return model
    
    def queryMostSimilarWordVec(self, model, wordStr):
        similarPairList = model.most_similar(wordStr.decode('utf-8'))
        return similarPairList
    
    def queryMsimilarWVfromFile(self, wordStr, modelFilePath=None):
        advanceSegOpt().reLoadEncoding()
        if modelFilePath == None:
            modelFilePath = self.modelPath
        model = self.loadModelfromFile(modelFilePath)
        return self.queryMostSimilarWordVec(model, wordStr)
    
    def culSimBtwWordVecs(self, model, wordStr1, wordStr2):
        similarValue = model.similarity(wordStr1.decode('utf-8'), wordStr2.decode('utf-8'))
        return similarValue
    
    def queryMSimilarVecswithPosNeg(self, model, posWordStrList, negWordStrList):
        posWordList = []
        negWordList = []
        for wordStr in posWordStrList:
            posWordList.append(wordStr.decode('utf-8'))
        for wordStr in negWordStrList:
            negWordList.append(wordStr.decode('utf-8'))
        pnSimilarPairList = model.most_similar(positive=posWordList, negative=negWordList)
        return pnSimilarPairList
    
if __name__ == '__main__':
    pass