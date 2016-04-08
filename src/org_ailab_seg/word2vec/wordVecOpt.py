# -*- coding: UTF-8 -*-

'''
Created on 2016年3月17日

@author: superhy
'''

import os
import warnings

from Cython.Build.Cythonize import multiprocessing
from gensim.models.word2vec import Word2Vec, LineSentence

from org_ailab_io import loadLocalFileData
from org_ailab_seg.advanceSegOpt import advanceSegOpt


class wordVecOpt:
    def __init__(self, modelPath, _size=100, _window=5, _minCount=1, _workers=multiprocessing.cpu_count()):
        self.modelPath = modelPath
        self._size = _size
        self._window = _window
        self._minCount = _minCount
        self._workers = _workers
    
    def loadModelfromFile(self, modelFilePath):
        '''
        load model from disk which is already existed
        can continue training with the loaded model (need more test)
        '''
        return Word2Vec.load(modelFilePath)
    
    def initTrainWord2VecModel(self, corpusFile, safe_model=False):
        '''
        init and train a new w2v model
        (corpusFile can be a path of corpus file or directory)
        about lazy_model:
            if safe_model is true, the process of training uses update way to refresh model,
        and this can keep the usage of os's memory safe but slowly.
            and if safe_model is false, the process of training uses the way that load all
        corpus lines into a sentences list and train them one time.
        '''
        advanceSegOpt().reLoadEncoding()
        
        fileType = loadLocalFileData.checkFileState(corpusFile)
        if fileType == u'error':
            warnings.warn('load file error!')
            return None
        else:
            model = None
            if fileType == u'file':
                model = Word2Vec(LineSentence(corpusFile), size=self._size, window=self._window, min_count=self._minCount, workers=self._workers)
            elif fileType == u'directory':
                if safe_model == True:
                    pass
                else:
                    pass
            elif fileType == u'other':
                #TODO is sentences list directly (same to next function)
                pass
                
            model.save(self.modelPath)
            model.init_sims(replace=True)
            print('producing word2vec model ... ok!')
            return model
        
    def updateW2VModelUnit(self, model, corpusSingleFile):
        '''
        only can be a singleFile
        '''
        trainedWordCount = model.train(LineSentence(corpusSingleFile))
        print('update model, update words num is: ' + trainedWordCount)
        return model
    
    def updateWord2VecModel(self, modelFilePath=None, corpusFile, safe_model=False):
        pass
    
    def queryMostSimilarWordVec(self, model, wordStr):
        '''
        MSimilar words basic query function
        return 2-dim List [0] is word [1] is double-prob
        '''
        similarPairList = model.most_similar(wordStr.decode('utf-8'))
        return similarPairList
    
    def queryMsimilarWVfromFile(self, wordStr, modelFilePath=None):
        '''
        load model + query MsimilarWV for single word total function
        (with sub function queryMostSimilarWordVec)
        '''
        advanceSegOpt().reLoadEncoding()
        
        if modelFilePath == None:
            modelFilePath = self.modelPath
        model = self.loadModelfromFile(modelFilePath)
        return self.queryMostSimilarWordVec(model, wordStr)
    
    def culSimBtwWordVecs(self, model, wordStr1, wordStr2):
        '''
        two words similar basic query function
        return double-prob
        '''
        similarValue = model.similarity(wordStr1.decode('utf-8'), wordStr2.decode('utf-8'))
        return similarValue
    
    def culSimBtwWVfromFile(self, wordStr1, wordStr2, modelFilePath=None):
        '''
        (with sub function culSimBtwWordVecs)
        '''
        advanceSegOpt.reLoadEncoding()
        
    
    def queryMSimilarVecswithPosNeg(self, model, posWordStrList, negWordStrList):
        '''
        pos-neg MSimilar words basic query function
        return 2-dim List [0] is word [1] is double-prob
        '''
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
