# -*- coding: UTF-8 -*-

'''
Created on 2016年7月29日

@author: hylovedd
'''
from org_ailab_cluster.association.apriori import aprioriAss
from org_ailab_kg import freqAssGraphSupOpt
from org_ailab_tools.cache import ROOT_PATH
from org_ailab_seg.word2vec.wordVecOpt import WordVecOpt

def testLoadEntitiesFromDict():
    dict_path = ROOT_PATH.seg_dictwin64 + u'jieba_shicai.txt'
    
    entities = freqAssGraphSupOpt.loadEntitiesFromDict(dict_path)
    
    for entity in entities:
        print(entity)
        
def testFreqDataSetFromW2V():
    dict_path = ROOT_PATH.seg_dictwin64 + u'jieba_shicai.txt'
    entities = freqAssGraphSupOpt.loadEntitiesFromDict(dict_path)
    
    modelStoragePath = ROOT_PATH.root_win64 + u'word2vec\\zongheword2vecModel.vector'
    entFreqSetDic = freqAssGraphSupOpt.freqDataSetFromW2V(modelStoragePath, entities, scanTopN=5)
    
    for key in entFreqSetDic:
        print(str(key) + ' ' + str(entFreqSetDic[key]))

def testAprioriAssFromEntities():
    dict_path = ROOT_PATH.seg_dictwin64 + u'jieba_shicai2.txt'
    entities = freqAssGraphSupOpt.loadEntitiesFromDict(dict_path)
    
    modelStoragePath = ROOT_PATH.root_win64 + u'word2vec\\zongheword2vecModel.vector'
    entFreqSetDic = freqAssGraphSupOpt.freqDataSetFromW2V(modelStoragePath, entities, scanTopN=10)
    
    rulesCachePath = ROOT_PATH.root_win64 + 'model_cache\\shicai_freqrules.txt=w'
    assRules = freqAssGraphSupOpt.aprioriAssFromEntities(entFreqSetDic, MinSupport=0.005, MinConf=0.4, rulesStorePath=rulesCachePath)
    for rules in assRules:
        print(rules[0] + ' -> ' + rules[1] + ': ' + str(rules[2]))
    
def testRelationBtwEntities():
    entity1 = u'红枣/n'
    entity2 = u'雪梨/n'
    
    modelStoragePath = ROOT_PATH.root_win64 + u'word2vec\\zongheword2vecModel.vector'
    
    sim = WordVecOpt(modelStoragePath).culSimBtwWVfromFile(entity1, entity2, modelStoragePath)
    print(sim)
    
    relationWordTuples = freqAssGraphSupOpt.relationBtwEntities(modelStoragePath, entity1, entity2, 500, pureFilterTopN=2)
    relationWordTuples2 = freqAssGraphSupOpt.relationBtwEntities(modelStoragePath, entity1, entity2, 50, pureFilterTopN=0)
    
    for relation in relationWordTuples:
        print relation[0], relation[1]
    print('-----------------------------------')
    for relation in relationWordTuples2:
        print relation[0], relation[1]
    
if __name__ == '__main__':
#     testLoadEntitiesFromDict()
#     testFreqDataSetFromW2V()
#     testAprioriAssFromEntities()
    testRelationBtwEntities()
    
