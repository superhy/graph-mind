# -*- coding: UTF-8 -*-

'''
Created on 2016年7月29日

@author: hylovedd
'''
from org_ailab_cluster.association.apriori import aprioriAss
from org_ailab_kg import freqAssGraphSupOpt
from org_ailab_tools.cache import ROOT_PATH


def testLoadEntitiesFromDict():
    dict_path = ROOT_PATH.seg_dictwin64 + u'jieba_shicai.txt'
    
    entities = freqAssGraphSupOpt.loadEntitiesFromDict(dict_path)
    
    for entity in entities:
        print(entity)
        
def testFreqDataSetFromW2V():
    dict_path = ROOT_PATH.seg_dictwin64 + u'jieba_shicai.txt'
    entities = freqAssGraphSupOpt.loadEntitiesFromDict(dict_path)
    
    modelStoragePath = ROOT_PATH.root_win64 + u'word2vec\\shicaiword2vecModel.vector'
    entFreqSetDic = freqAssGraphSupOpt.freqDataSetFromW2V(modelStoragePath, entities, scanTopN=5)
    
    for key in entFreqSetDic:
        print(str(key) + ' ' + str(entFreqSetDic[key]))

def testAprioriAssFromEntities():
    dict_path = ROOT_PATH.seg_dictwin64 + u'jieba_shicai.txt'
    entities = freqAssGraphSupOpt.loadEntitiesFromDict(dict_path)
    
    modelStoragePath = ROOT_PATH.root_win64 + u'word2vec\\shicaiword2vecModel.vector'
    entFreqSetDic = freqAssGraphSupOpt.freqDataSetFromW2V(modelStoragePath, entities, scanTopN=10)
    
    rulesCachePath = ROOT_PATH.root_win64 + 'model_cache\\shicai_freqrules.txt=w+'
    assRules = freqAssGraphSupOpt.aprioriAssFromEntities(entFreqSetDic, MinSupport=0.01, MinConf=0.6, rulesStorePath=rulesCachePath)
    for rules in assRules:
        print(rules[0] + ' -> ' + rules[1] + ': ' + str(rules[2]))
    
def testRelationBtwEntities():
    entity1 = u'泡椒凤爪/n'
    entity2 = u'肝癌/n'
    
    modelStoragePath = ROOT_PATH.root_win64 + u'word2vec\\zongheword2vecModel.vector'
    relationWordTuples = freqAssGraphSupOpt.relationBtwEntities(modelStoragePath, entity1, entity2, 100, pureFilterTopN=200)
    relationWordTuples2 = freqAssGraphSupOpt.relationBtwEntities(modelStoragePath, entity1, entity2, 100, pureFilterTopN=0)
    
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
    
