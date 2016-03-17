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


class wordVecOpt:
    def __init__(self, corpusFile, modelPath):
        self.corpusFile = corpusFile
        self.modelPath = modelPath
        
    def trainWord2VecModel(self, _size=100, _window=5, _minCount=5, _workers=multiprocessing.cpu_count()):
        fileType = loadLocalFileData.checkFile(self.corpusFile)
        print(fileType)
        if fileType == u'null' or fileType == u'error':
            warnings.warn('load file error!')
        else:
            model = Word2Vec(LineSentence(self.corpusFile), size=_size, window=_window, min_count=_minCount, workers=_workers)
            model.save(self.modelPath)
            model.init_sims(replace=True)
            return model
if __name__ == '__main__':
    pass