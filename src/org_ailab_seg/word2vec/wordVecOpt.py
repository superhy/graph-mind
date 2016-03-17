'''
Created on 2016年3月17日

@author: superhy
'''

from Cython.Build.Cythonize import multiprocessing
from gensim.models.word2vec import Word2Vec, LineSentence
from org_ailab_load import loadLocalFileData
import warnings


class wordVecOpt:
    def __init__(self, corpusPathDir, modelPath):
        self.corpusPathDir = corpusPathDir
        self.modelPath = modelPath
        
    def trainWord2VecModel(self, _size=100, _window=5, _minCount=5, _workers=multiprocessing.cpu_count()):
        fileType = loadLocalFileData.checkFile(self.corpusPathDir)
        if fileType == u'null' or fileType == u'error':
            warnings.warn('load file error!')
            pass
        else:
            if fileType == u'file':
                model = Word2Vec(LineSentence(self.corpusPathDir), size=_size, window=_window, min_count=_minCount, workers=_workers)
                model.save(self.modelPath)
            elif fileType == u'dir':
                pass

if __name__ == '__main__':
    pass