# -*- coding: UTF-8 -*-

'''
Created on 2016年3月17日

@author: superhy
'''

import multiprocessing
import os
import warnings

from gensim.models.word2vec import Word2Vec, LineSentence

from tools import localFileOptUnit
from tools.cache import ROOT_PATH
from word_seg.extraSegOpt import ExtraSegOpt


class WordVecOpt(object):
    def __init__(self, modelPath, size=100, window=5, minCount=1, workers=multiprocessing.cpu_count()):
        self.modelPath = modelPath
        self._size = size
        self._window = window
        self._minCount = minCount
        self._workers = workers
    
    def loadModelfromFile(self, modelFilePath):
        '''
        load model from disk which is already existed
        can continue training with the loaded model (need more test)
        '''
        return Word2Vec.load(modelFilePath)
    
    def initTrainWord2VecModel(self, corpusFilePath):
        '''
        init and train a new w2v model
        (corpusFilePath can be a path of corpus file or directory or a file directly, in some time it can be sentences directly
        about soft_model:
            if safe_model is true, the process of training uses update way to refresh model,
        and this can keep the usage of os's memory safe but slowly.
            and if safe_model is false, the process of training uses the way that load all
        corpus lines into a sentences list and train them one time.)
        '''
        ExtraSegOpt().reLoadEncoding()
        
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
                corpusFile.close()
            elif fileType == u'directory':
                corpusFiles = localFileOptUnit.listAllFilePathInDirectory(corpusFilePath)
                print('training model from listFiles of directory!')
                
                sentences = localFileOptUnit.loadSetencesFromFiles(corpusFiles)
                model = Word2Vec(sentences, size=self._size, window=self._window, min_count=self._minCount, workers=self._workers)
            elif fileType == u'other':
                # TODO add sentences list directly
                pass
                
            model.save(self.modelPath)
            model.init_sims()
            print('producing word2vec model ... ok!')
            return model
    
    # not suggest, only can update the model build by non-C tools    
    def updateW2VModelUnit(self, model, corpusSingleFilePath):
        '''
        (only can be a singleFile)
        '''
        fileType = localFileOptUnit.checkFileState(corpusSingleFilePath)
        if fileType == u'directory':
            warnings.warn('can not deal a directory!')
            return
        
        if fileType == u'opened':
            trainedWordCount = model.train(LineSentence(corpusSingleFilePath))
            print('update model, update words num is: ' + str(trainedWordCount))
        elif fileType == u'file':
            corpusSingleFile = open(corpusSingleFilePath, u'r')
            trainedWordCount = model.train(LineSentence(corpusSingleFile))
            corpusSingleFile.close()
            print('update model, update words num is: ' + str(trainedWordCount))
        else:
            # TODO add sentences list directly (same as last function)
            pass
    
    # not suggest, only can update the model build by non-C tools
    def updateWord2VecModel(self, corpusFilePath, modelFilePath=None):
        '''
        update w2v model from disk
        (about corpusFilePath and safe_model is same as function initTrainWord2VecModel
        default set safe_model == True)
        '''
        ExtraSegOpt().reLoadEncoding()
        
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
                self.updateW2VModelUnit(model, corpusFilePath)
            elif fileType == u'directory':
                corpusFiles = localFileOptUnit.listAllFilePathInDirectory(corpusFilePath)
                for file in corpusFiles:
                    self.updateW2VModelUnit(model, file)
    
    def finishTrainModel(self, modelFilePath=None):
        '''
        warning: after this, the model is read-only (can't be update)
        '''
        if modelFilePath == None:
            modelFilePath = self.modelPath
        model = self.loadModelfromFile(modelFilePath)
        model.init_sims(replace=True)
        
    def getWordVec(self, model, wordStr):
        '''
        get the word's vector as arrayList type from w2v model
        '''
        ExtraSegOpt().reLoadEncoding()
        
        return model[wordStr]
    
    def getWordVecfromFile(self, wordStr, modelFilePath=None):
        '''
        load model + get word's vector
        (with sub function getWordVec)
        '''
        
        if modelFilePath == None:
            modelFilePath = self.modelPath
        model = self.loadModelfromFile(modelFilePath)
        return self.getWordVec(model, wordStr)
    
    def queryMostSimilarWordVec(self, model, wordStr, topN=20):
        '''
        MSimilar words basic query function
        return 2-dim List [0] is word [1] is double-prob
        '''
        ExtraSegOpt().reLoadEncoding()
        
        similarPairList = model.most_similar(wordStr.decode('utf-8'), topn=topN)
        return similarPairList
    
    def queryMsimilarWVfromFile(self, wordStr, modelFilePath=None, topN=20):
        '''
        load model + query MsimilarWV for single word total function
        (with sub function queryMostSimilarWordVec)
        '''
        
        if modelFilePath == None:
            modelFilePath = self.modelPath
        model = self.loadModelfromFile(modelFilePath)
        return self.queryMostSimilarWordVec(model, wordStr, topN)
    
    def culSimBtwWordVecs(self, model, wordStr1, wordStr2):
        '''
        two words similar basic query function
        return double-prob
        '''
        ExtraSegOpt().reLoadEncoding()
        
        similarValue = model.similarity(wordStr1.decode('utf-8'), wordStr2.decode('utf-8'))
        return similarValue
    
    def culSimBtwWVfromFile(self, wordStr1, wordStr2, modelFilePath=None):
        '''
        (with sub function culSimBtwWordVecs)
        '''
        
        if modelFilePath == None:
            modelFilePath = self.modelPath
        model = self.loadModelfromFile(modelFilePath)
        return self.culSimBtwWordVecs(model, wordStr1, wordStr2)
    
    def queryMSimilarVecswithPosNeg(self, model, posWordStrList, negWordStrList, topN=20):
        '''
        pos-neg MSimilar words basic query function
        return 2-dim List [0] is word [1] is double-prob
        '''
        ExtraSegOpt().reLoadEncoding()
        
        posWordList = []
        negWordList = []
        for wordStr in posWordStrList:
            posWordList.append(wordStr.decode('utf-8'))
        for wordStr in negWordStrList:
            negWordList.append(wordStr.decode('utf-8'))
        pnSimilarPairList = model.most_similar(positive=posWordList, negative=negWordList, topn=topN)
        return pnSimilarPairList
    
    def queryMSVwithPosNegFromFile(self, posWordStrList, negWordStrList, modelFilePath=None, topN=20):
        '''
        (with sub function queryMSimilarVecswithPosNeg)
        '''
        
        if modelFilePath == None:
            modelFilePath = self.modelPath
        model = self.loadModelfromFile(modelFilePath)
        return self.queryMSimilarVecswithPosNeg(model, posWordStrList, negWordStrList, topN)
    
    def copeMSimilarVecsbtwWordLists(self, model, wordStrList1, wordStrList2, topN_rev=20, topN=20):
        '''
        range word vec res for two wordList from source to target
        use wordVector to express the relationship between src-wordList and tag-wordList
        first, use the tag-wordList as neg-wordList to get the rev-wordList,
        then use the scr-wordList and the rev-wordList as the new src-tag-wordList
        topN_rev is topN of rev-wordList and topN is the final topN of relationship vec
        '''
        ExtraSegOpt().reLoadEncoding()
        
        srcWordList = []
        tagWordList = []
        srcWordList.extend(wordStr.decode('utf-8') for wordStr in wordStrList1)
        tagWordList.extend(wordStr.decode('utf-8') for wordStr in wordStrList2)
        
        revSimilarPairList = self.queryMSimilarVecswithPosNeg(model, [], tagWordList, topN_rev)
        revWordList = []
        revWordList.extend(pair[0].decode('utf-8') for pair in revSimilarPairList)
        stSimilarPairList = self.queryMSimilarVecswithPosNeg(model, srcWordList, revWordList, topN)
        return stSimilarPairList
    
    def copeMSVbtwWordListsFromFile(self, wordStrList1, wordStrList2, modelFilePath = None, topN_rev=20, topN=20):
        '''
        load model + copeMSVs between wordLists
        (with sub function copeMSimilarVecsbtwWordLists)
        '''
        
        if modelFilePath == None:
            modelFilePath = self.modelPath
        model = self.loadModelfromFile(modelFilePath)
        return self.copeMSimilarVecsbtwWordLists(model, wordStrList1, wordStrList2, topN_rev, topN)
    
if __name__ == '__main__':
    pass