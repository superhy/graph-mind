# -*- coding: UTF-8 -*-

'''
Created on 2016年8月8日

@author: hylovedd
'''
from org_ailab_kg import medGraphSupOpt
from org_ailab_seg.word2vec.wordTypeFilter import WordTypeFilter
from org_ailab_tools.cache import ROOT_PATH


def testCrossLinkedWordsPrecess():
    dict_path = ROOT_PATH.seg_dictwin64 + u'jieba_shicai.txt'
    sourceEntities = medGraphSupOpt.loadEntitiesFromDict(dict_path)
    
    modelStoragePath = ROOT_PATH.root_win64 + u'model\\word2vec\\zongheword2vecModel.vector'
    
    entityStr = u'党参/n'
    # get the source scan tuples result, to pure the mid scan result
#     pureTuples = findLinkedWords(modelStoragePath, entityStr, sourceEntities, pureScanRange)
    sourceTuples = medGraphSupOpt.seekSimWords(modelStoragePath, entities=[entityStr], pureCleanWords=[], scanRange=10)
    supTuples = WordTypeFilter().ditInOutWordFilter(sourceTuples, sourceEntities, 'out')
    cleanTuples = WordTypeFilter().ditInOutWordFilter(sourceTuples, sourceEntities, 'in')
    pureSupWords = [entityStr]
    pureSupWords.extend(e[0] for e in supTuples)
    pureCleanWords = []
    pureCleanWords.extend(e[0] for e in cleanTuples)
    # get the mid scan tuples result, to link the tag scan result
    # need to test use sup tuples into positive word list
    midTuples = medGraphSupOpt.seekSimWords(modelStoragePath, entities=pureSupWords, pureCleanWords=pureCleanWords, scanRange=20)
#     midTuples = seekSimWords(modelStoragePath, [entityStr], pureCleanWords=pureCleanWords, scanRange=midScanRange)
    for e in midTuples:
        print(e[0] + ': ' + str(e[1]))
    print('--------------------------------------')

def testFindLinkedWords():
    dict_path = ROOT_PATH.seg_dictwin64 + u'jieba_yixuebaike.txt'
    domainEntities = medGraphSupOpt.loadEntitiesFromDict(dict_path)
    
    modelStoragePath = ROOT_PATH.root_win64 + u'model\\word2vec\\zongheword2vecModel.vector'
    
    entityStr = u'肺炎/n'
    simTuples = medGraphSupOpt.findLinkedWords(modelStoragePath, entityStr, domainEntities, scanRange=10)
    for e in simTuples:
        print(e[0] + ': ' + str(e[1]))
    print('--------------------------------------')
        
def testFindCrossLinkedWords():
    shicai_dict_path = ROOT_PATH.seg_dictwin64 + u'jieba_shicai.txt'
    yixuebaike_dict_path = ROOT_PATH.seg_dictwin64 + u'jieba_yixuebaike.txt'
    shicai_Entities = medGraphSupOpt.loadEntitiesFromDict(shicai_dict_path)
    yixuebaike_Entities = medGraphSupOpt.loadEntitiesFromDict(yixuebaike_dict_path)
    
    modelStoragePath = ROOT_PATH.root_win64 + u'model\\word2vec\\zongheword2vecModel.vector'
    
    shicaiEntityStr = u'莲子/n'
    tagTuples = medGraphSupOpt.findCrossLinkedWords(modelStoragePath, shicaiEntityStr, shicai_Entities, yixuebaike_Entities, [10, 50, 500])
    print('source: ' + shicaiEntityStr)
    print('linked to: ')
    for e in tagTuples:
        print(e[0] + ': ' + str(e[1]))
        
def testCollectInDomainLinks():
    shicai_dict_path = ROOT_PATH.seg_dictwin64 + u'jieba_shicai.txt'
    yixuebaike_dict_path = ROOT_PATH.seg_dictwin64 + u'jieba_yixuebaike.txt'
    shicai_Entities = medGraphSupOpt.loadEntitiesFromDict(shicai_dict_path)
    yixuebaike_Entities = medGraphSupOpt.loadEntitiesFromDict(yixuebaike_dict_path)
    
    modelStoragePath = ROOT_PATH.root_win64 + u'model\\word2vec\\zongheword2vecModel.vector'
    
    linkWriteFileInfo = ROOT_PATH.root_win64 + u'model_cache\\yixuebaike_links.txt=a'
    
    inDomainLinksDic = medGraphSupOpt.collectInDomainLinks(modelStoragePath, yixuebaike_Entities, 10, 20, linkWriteFileInfo)
    print('dic size: ' + str(len(inDomainLinksDic.keys())))
    
#     medGraphSupOpt.writeAllLinksIntoFile(inDomainLinksDic, linkWriteFileInfo)

def testCollectCrossDomainLinks():
    shicai_dict_path = ROOT_PATH.seg_dictwin64 + u'jieba_shicai_cta.txt'
    yixuebaike_dict_path = ROOT_PATH.seg_dictwin64 + u'jieba_yixuebaike.txt'
    shicai_Entities = medGraphSupOpt.loadEntitiesFromDict(shicai_dict_path)
    yixuebaike_Entities = medGraphSupOpt.loadEntitiesFromDict(yixuebaike_dict_path)
    
    modelStoragePath = ROOT_PATH.root_win64 + u'model\\word2vec\\zongheword2vecModel.vector'
    
    linkWriteFileInfo = ROOT_PATH.root_win64 + u'model_cache\\shicai2bingzheng_links.txt=a'
    
    crossDomainLinkDic = medGraphSupOpt.collectCrossDomainLinks(modelStoragePath, shicai_Entities, yixuebaike_Entities, [5, 20, 300], 20, linkWriteFileInfo)
    print('dic size: ' + str(len(crossDomainLinkDic.keys())))
    
if __name__ == '__main__':
#     testCrossLinkedWordsPrecess()
#     testFindLinkedWords()
#     testFindCrossLinkedWords()
    
    testCollectInDomainLinks()
#     testCollectCrossDomainLinks()
