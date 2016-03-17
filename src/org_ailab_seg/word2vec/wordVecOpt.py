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
        wordSimilarList = model.most_similar(wordStr.decode('utf-8'))
        return wordSimilarList
    
    def queryMsimilarWVfromFile(self, modelFilePath, wordStr):
        advanceSegOpt().reLoadEncoding()
        model = Word2Vec.load(modelFilePath)
        return self.queryMostSimilarWordVec(model, wordStr)
    
if __name__ == '__main__':
    pass