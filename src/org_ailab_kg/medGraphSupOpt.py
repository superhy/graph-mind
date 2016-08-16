# -*- coding: UTF-8 -*-

'''
Created on 2016年8月8日

@author: hylovedd
'''

from org_ailab_seg.word2vec.wordTypeFilter import wordTypeFilter
from org_ailab_seg.word2vec.wordVecOpt import wordVecOpt
from gensim.models.word2vec import Word2Vec


def prodFieldW2VModel(modelStoragePath, corpusFilePath, dimension_size=100):
    wordVecOptObj = wordVecOpt(modelStoragePath, size=dimension_size)
    model = wordVecOptObj.initTrainWord2VecModel(corpusFilePath)
    
    return model

def loadW2VModelFromDisk(modelStoragePath):
    wordVecOptObj = wordVecOpt(modelStoragePath)
    model = wordVecOptObj.loadModelfromFile(modelStoragePath)
    
    return wordVecOptObj, model

def loadEntitiesFromDict(dictPath):
    fr = open(dictPath, 'r')
    entities = []
    entities.extend(line[:line.find('\n')].replace(' ', '/').decode('utf-8') for line in fr)  # clean the newline character
    
    return entities

def seekSimWords(modelStoragePath, entities, pureCleanWords, scanRange):
    '''
    entities can be a single string or a list of strings,
    but they must in a list
    '''
    wordVecOptObj, model = loadW2VModelFromDisk(modelStoragePath)
    
    simTuples = []
    
    # clean the words not in the model's vocab
    posWords, negWords = [], []
    for e in entities:
        if e in model.vocab:
            posWords.append(e)
        else:
            print(u'entity word ' + e + u' not in vocab!')
    for e in pureCleanWords:
        if e in model.vocab:
            negWords.append(e)
        else:
            print(u'pure word ' + e + u' not in vocab!')
    
    if len(posWords) == 0:
        print('posWords can not be null!')
        return simTuples
    
    if len(posWords) == 1 and pureCleanWords == []:
        simTuples = wordVecOptObj.queryMostSimilarWordVec(model, posWords[0], scanRange)
    else:
        simTuples = wordVecOptObj.queryMSimilarVecswithPosNeg(model, posWords, negWords, scanRange)
        
    return simTuples

def findLinkedWords(modelStoragePath, entityStr, domainEntities, scanRange):
    simTuples = seekSimWords(modelStoragePath, [entityStr], [], scanRange)
    if len(simTuples) == 0: # cut short save time
        return simTuples
    
    simTuples = wordTypeFilter().ditInOutWordFilter(simTuples, domainEntities, 'in')
    
    return simTuples

def findCrossLinkedWords(modelStoragePath, entityStr, srcEntities, tagEntities, scanRanges):
    '''
    scanRanges contains three parameters: 1.pureScanRange, 2.midScanRange, 3.tagScanRange
    '''
    pureScanRange, midScanRange, tagScanRange = scanRanges[0], scanRanges[1], scanRanges[2]
    
    # get the source scan tuples result, to pure the mid scan result
#     pureTuples = findLinkedWords(modelStoragePath, entityStr, srcEntities, pureScanRange)
    sourceTuples = seekSimWords(modelStoragePath, entities=[entityStr], pureCleanWords=[], scanRange=pureScanRange)
    if len(sourceTuples) == 0: # cut short save time
        return sourceTuples
    
    supTuples = wordTypeFilter().ditInOutWordFilter(sourceTuples, srcEntities, 'out')
    cleanTuples = wordTypeFilter().ditInOutWordFilter(sourceTuples, srcEntities, 'in')
    pureSupWords = [entityStr]
    pureSupWords.extend(e[0] for e in supTuples)
    pureCleanWords = []
    pureCleanWords.extend(e[0] for e in cleanTuples)
    # get the mid scan tuples result, to link the tag scan result
    # need to test use sup tuples into positive word list
    midTuples = seekSimWords(modelStoragePath, entities=pureSupWords, pureCleanWords=pureCleanWords, scanRange=midScanRange)
#     midTuples = seekSimWords(modelStoragePath, [entityStr], pureCleanWords=pureCleanWords, scanRange=midScanRange)
    if len(midTuples) == 0 : # cut short save time
        return midTuples
    
    mid_tagTuples = wordTypeFilter().ditInOutWordFilter(midTuples, tagEntities, 'in')
    midWords = []
    midWords.extend(e[0] for e in midTuples)
    # get the tag scan tuples from mid words
    # TODO need test add pure words again or not
    tagTuples = seekSimWords(modelStoragePath, entities=midWords, pureCleanWords=[], scanRange=tagScanRange)
#     tagTuples = seekSimWords(modelStoragePath, midWords, pureCleanWords=pureCleanWords, scanRange=tagScanRange)
    if len(tagTuples) == 0: # cut short save time
        return tagTuples
    
    tagTuples = wordTypeFilter().ditInOutWordFilter(tagTuples, tagEntities, 'in')
    tagTuples.extend(mid_tagTuples)
    
    return tagTuples

def repInDomainLinks(modelStoragePath, sEntityStr, tEntityStr, domainEntities, repRange):
    '''
    '''
    wordVecOptObj, model = loadW2VModelFromDisk(modelStoragePath)
    
    linkTuples = wordVecOptObj.queryMSimilarVecswithPosNeg(model, [sEntityStr, tEntityStr], [], repRange)
    linkTuples = wordTypeFilter().ditInOutWordFilter(linkTuples, domainEntities, 'out')
    
    return linkTuples

def repCrossDomainLinks(modelStoragePath, sEntityStr, tEntityStr, srcEntities, tagEntities, repRange):
    '''
    '''
    outEntities = srcEntities + tagEntities
    linkTuples = repInDomainLinks(modelStoragePath, sEntityStr, tEntityStr, outEntities, repRange)
    
    return linkTuples

def collectInDomainLinks(modelStoragePath, domainEntities, scanRange, repRange, fileWriteInfo=u''):
    '''
    collect the links in one domain 
    which contain all src, tag entities and relations between them
    only give the src entities and need to find all linked entities
    in domain from them, then give the relations from src entities
    to all entities it links
    such as we own n domain entities and each entity has about m
    relations, so we get n*m relations and each relation be represented
    by p represent words with their probability value
    '''
    inDomainlinksDic = {}
    for entityStr in domainEntities:
        simTuples = findLinkedWords(modelStoragePath, entityStr, domainEntities, scanRange)
        if len(simTuples) > 0:
            for tuple in simTuples:
                tEntityStr = tuple[0]
                linkKey = entityStr + '-->' + tEntityStr
                linkTuples = repInDomainLinks(modelStoragePath, entityStr, tEntityStr, domainEntities, repRange)
                
                if len(linkTuples) > 0:  # and (not inDomainlinksDic.has_key(linkKey))
                    inDomainlinksDic[linkKey] = linkTuples
                    if fileWriteInfo.find(u'=') != -1:
                        writeLinkIntoFile(linkKey, linkTuples, fileWriteInfo)
                    print('representing in domain links: ' + linkKey)
    
    return inDomainlinksDic
    
def collectCrossDomainLinks(modelStoragePath, srcEntities, tagEntities, scanRanges, repRange, fileWriteInfo=u''):
    '''
    collect the links cross two domains
    same as the function 'collectInDomainLinks'
    if we own n srcEntities and each entity has m linked entities
    in tag domain, so we can get n * m relations, each relations
    with p represent words and its probability value 
    '''
    crossDomainLinksDic = {}
    for entityStr in srcEntities:
        simTuples = findCrossLinkedWords(modelStoragePath, entityStr, srcEntities, tagEntities, scanRanges)
        if len(simTuples) > 0:
            for tuple in simTuples:
                tEntityStr = tuple[0]
                linkKey = entityStr + '-->' + tEntityStr
                linkTuples = repCrossDomainLinks(modelStoragePath, entityStr, tEntityStr, srcEntities, tagEntities, repRange)
                
                if len(linkTuples) > 0:  # and (not crossDomainLinksDic.has_key(linkKey))
                    crossDomainLinksDic[linkKey] = linkTuples
                    if fileWriteInfo.find(u'=') != -1:
                        writeLinkIntoFile(linkKey, linkTuples, fileWriteInfo)
                    print('representing cross domain links: ' + linkKey)
                    
    return crossDomainLinksDic
    
####################################################################

def writeLinkIntoFile(linkKey, linkTuples, fileWriteInfo):
    '''
    'fileWriteInfo' is path + write type, divided by '='
    '''
    linkInfoStr = u''
    linkInfoStr += (linkKey + '{')
        
    repValueStrList = []
    for tuple in linkTuples:
        repValueStr = tuple[0] + ':' + str(tuple[1])
        repValueStrList.append(repValueStr)
    linkInfoStr += (','.join(repValueStrList))
    linkInfoStr += '}\n'
    
    fw = open(fileWriteInfo.split(u'=')[0], fileWriteInfo.split(u'=')[1])
    fw.write(linkInfoStr)
    fw.close()

def writeAllLinksIntoFile(linksDic, writeFilePath, writeType='w'):
    '''
    '''
    linksInfoList = []
    for key in linksDic.keys():
        linkInfoStr = u''
        linkInfoStr += (key + '{')
        
        repVauleTuples = linksDic[key]
        repValueStrList = []
        for tuple in repVauleTuples:
            repValueStr = tuple[0] + ':' + str(tuple[1])
            repValueStrList.append(repValueStr)
        linkInfoStr += (','.join(repValueStrList))
        linkInfoStr += '}'
        
        linksInfoList.append(linkInfoStr)
    
    fw = open(writeFilePath, writeType)
    fw.write('\n'.join(linksInfoList))
    fw.close()

if __name__ == '__main__':
    pass
