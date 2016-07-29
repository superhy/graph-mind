# -*- coding: UTF-8 -*-

'''
Created on 2016年7月26日

@author: hylovedd
'''
from org_ailab_seg.word2vec.wordVecOpt import wordVecOpt
from org_ailab_tools.cache import ROOT_PATH


def prodFieldW2VModel(modelStoragePath, corpusFilePath, dimension_size=100):
    wordVecOptObj = wordVecOpt(modelStoragePath, size=dimension_size)
    model = wordVecOptObj.initTrainWord2VecModel(corpusFilePath)
    
    return model

# need not
def loadW2VModelFromDisk(modelStoragePath):
    wordVecOptObj = wordVecOpt(modelStoragePath)
    model = wordVecOptObj.loadModelfromFile(modelStoragePath)
    
    return model

def freqDataSetFromW2V(modelStoragePath, entities, scanTopN):
    '''
    entity must look like 'XXXX/?'
    entity in entities list must be unique
    '''
    wordVecOptObj = wordVecOpt(modelStoragePath)
    
    entFreqSetDic = {}
    for entity in entities:
        entMSimList = wordVecOptObj.queryMsimilarWVfromFile(entity, topN = scanTopN)
        
        freqTuple = (entity, )
        freqProbScoreSum = 0.0
        for msEnt in entFreqSetDic:
            if msEnt[0] in entities:
                freqTuple += (msEnt[0], )
                freqProbScoreSum += msEnt[1]
        if freqProbScoreSum > 0.0:
            freqProbScoreAvg = freqProbScoreSum / (len(freqTuple) - 1)
            entFreqSetDic[freqTuple] = freqProbScoreAvg
    
    return entFreqSetDic

def loadEntitiesFromDict(dictPath):
    fw = open(dictPath, 'r')
    entities = []
    entities.extend(line[:line.find('\n')].replace(' ', '/') for line in fw) # clean the newline character
    
    return entities

if __name__ == '__main__':
    modelStoragePath = ROOT_PATH.root_win64 + u'word2vec\\shicaiword2vecModel.vector'
    corpusFilePath = ROOT_PATH.root_win64 + u'med_seg\\食材百科\\'
    
    w2vModel = prodFieldW2VModel(modelStoragePath, corpusFilePath, dimension_size=150)

#     w2vModel = loadW2VModelFromDisk(modelStoragePath)
    
    wordVecOptObj = wordVecOpt(modelStoragePath)
    print(u'train time: ' + str(w2vModel.total_train_time))
    print(u'model dimensionality size: ' + str(w2vModel.vector_size))
    print(u'process corpus num : ' + str(w2vModel.corpus_count))
    wordStr = u'阿胶/n'
    print(u'Train model and word vec object: ' + wordStr)
    queryList = wordVecOptObj.queryMostSimilarWordVec(w2vModel, wordStr, topN=20)
    for e in queryList:
        print e[0], e[1]
        
    print(u'word in vector space:----------------------------------------------------')
    vector = wordVecOptObj.getWordVec(w2vModel, wordStr)
    print(vector)