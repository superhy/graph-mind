# -*- coding: UTF-8 -*-

'''
Created on 2016年3月17日

@author: superhy
'''

import os
import warnings

from Cython.Build.Cythonize import multiprocessing
from gensim.models.word2vec import Word2Vec, LineSentence

from org_ailab_io import localFileOptUnit
from org_ailab_seg.advanceSegOpt import advanceSegOpt
from win32con import SLE_ERROR


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
    
    def loadSetencesFromFiles(self, files):
        '''
        load all sentences list from files
        '''
        sentences = []
        for file in files:
            sentences.extend(LineSentence(file))
        return sentences
    
    def initTrainWord2VecModel(self, corpusFilePath, safe_model=False):
        '''
        init and train a new w2v model
        (corpusFilePath can be a path of corpus file or directory or a file directly, in some time it can be sentences directly
        about soft_model:
            if safe_model is true, the process of training uses update way to refresh model,
        and this can keep the usage of os's memory safe but slowly.
            and if safe_model is false, the process of training uses the way that load all
        corpus lines into a sentences list and train them one time.)
        '''
        advanceSegOpt().reLoadEncoding()
        
        fileType = localFileOptUnit.checkFileState(corpusFilePath)
        if fileType == u'error':
            warnings.warn('load file error!')
            return None
        else:
            model = None
            if fileType == u'opened':
                print('training model from singleFile!')
                model = Word2Vec(LineSentence(corpusFilePath), size=self._size, window=self._window, min_count=self._minCount, workers=self._workers)
            elif fileType == u'file':
                corpusFile = open(corpusFilePath, u'r')
                print('training model from singleFile!')
                model = Word2Vec(LineSentence(corpusFile), size=self._size, window=self._window, min_count=self._minCount, workers=self._workers)
            elif fileType == u'directory':
                corpusFiles = localFileOptUnit.listAllFileInDirectory(corpusFilePath)
                print('training model from listFiles of directory!')
                if safe_model == True:
                    model = Word2Vec(LineSentence(corpusFiles[0]), size=self._size, window=self._window, min_count=self._minCount, workers=self._workers)
                    for file in corpusFiles[1:len(corpusFiles)]:
                        model = self.updateW2VModelUnit(model, file)
                else:
                    sentences = self.loadSetencesFromFiles(corpusFiles)
                    model = Word2Vec(sentences, size=self._size, window=self._window, min_count=self._minCount, workers=self._workers)
            elif fileType == u'other':
                # TODO add sentences list directly
                pass
                
            model.save(self.modelPath)
            model.init_sims()
            print('producing word2vec model ... ok!')
            return model
        
    def updateW2VModelUnit(self, model, corpusSingleFilePath):
        '''
        (only can be a singleFile)
        '''
        fileType = localFileOptUnit.checkFileState(corpusSingleFilePath)
        if fileType == u'directory':
            warnings.warn('can not deal a directory!')
            return model
        
        if fileType == u'opened':
            trainedWordCount = model.train(LineSentence(corpusSingleFilePath))
            print('update model, update words num is: ' + trainedWordCount)
        elif fileType == u'file':
            corpusSingleFile = open(corpusSingleFilePath, u'r')
            trainedWordCount = model.train(LineSentence(corpusSingleFile))
            print('update model, update words num is: ' + trainedWordCount)
        else:
            # TODO add sentences list directly (same as last function)
            pass
        return model
    
    def updateWord2VecModel(self, modelFilePath=None, corpusFilePath):
        '''
        update w2v model from disk
        (about corpusFilePath and safe_model is same as function initTrainWord2VecModel
        default set safe_model == True)
        '''
        advanceSegOpt().reLoadEncoding()
        
        fileType = localFileOptUnit.checkFileState(corpusFilePath)
        if fileType == u'error':
            warnings.warn('load file error!')
            return None
        else:
            if modelFilePath == None:
                modelFilePath = self.modelPath
            model = self.loadModelfromFile(modelFilePath)
            # TODO add safe_model == False
            if fileType == u'file' or u'opened':
                model = self.updateW2VModelUnit(model, corpusFilePath)
            elif fileType == u'directory':
                corpusFiles = localFileOptUnit.listAllFileInDirectory(corpusFilePath)
                for file in corpusFiles:
                    model = self.updateW2VModelUnit(model, file)
        return model
    
    def finishTrainModel(self, modelFilePath=None):
        '''
        warning: after this, the model is read-only (can't be update)
        '''
        if modelFilePath == None:
            modelFilePath = self.modelPath
        model = self.loadModelfromFile(modelFilePath)
        model.init_sims(replace=True)
    
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
        
        if modelFilePath == None:
            modelFilePath = self.modelPath
        model = self.loadModelfromFile(modelFilePath)
        return self.culSimBtwWordVecs(model, wordStr1, wordStr2)
    
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
    
    def queryMSVwithPosNegFromFile(self, posWordStrList, negWordStrList, modelFilePath=None):
        '''
        (with sub function queryMSimilarVecswithPosNeg)
        '''
        advanceSegOpt.reLoadEncoding()
        
        if modelFilePath == None:
            modelFilePath = self.modelPath
        model = self.loadModelfromFile(modelFilePath)
        return self.queryMSimilarVecswithPosNeg(model, posWordStrList, negWordStrList)
    
if __name__ == '__main__':
    pass
