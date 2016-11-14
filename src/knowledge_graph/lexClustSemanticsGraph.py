# -*- coding: UTF-8 -*-
'''
Created on 2016年5月16日

@author: superhy
'''

import numpy

from orgclustertworks.SOMNetWork import KohonenSOM
from orgdatastoreaph.neoDataGraphOpt import NeoDataGraphOpt
from orgword_segrd2vec.wordTypeFilter import WordTypeFilter
from orgword_segrd2vec.wordVecOpt import WordVecOpt

class LexClustSemanticsGraph(object):
    '''
    TODO
    设置基类，继承，统一管理共享参数，如：是否直接传入实体词列表等等
    '''
    
    def createLexClustEmtityNodes(self, neoOptObj, wvOptObj, wordList, vec_z_ratio, canopy_t_ratio, cluster=None):
        '''
        '''
        if cluster == None:
            cluster = KohonenSOM(wvOptObj._size)
        
        wordPairs = []
        for word in wordList:
            wordPair = [word, 0.0]
            wordPairs.append(wordPair)
        entityWordPairs = WordTypeFilter().enWordTypeFilter(wordPairs)
        
        # run the word cluster
        wordMatrixDic = {}
        for wordPair in entityWordPairs:
            word = wordPair[0]
            if word.split(u'/')[0] != u'':
                wordVec = wvOptObj.getWordVecfromFile(word)
                wordVec = numpy.array(wordVec) * vec_z_ratio
                wordMatrixDic[word] = wordVec
                print(u'get word vec: ' + word + u'(' + str(wordVec) + u')')
        wordClusters, wordClustResDic = cluster.clust(wordMatrixDic, canopy_t_ratio)
        print(u'finish word clust!')
        
        lexGroupNodes = []
        print('cluster num:' + str(len(wordClusters)))
        for wordCluster in wordClusters:
            if len(wordCluster) != 0:
                lex_groupStr = ''
#                 groupAttrDic = {}
                avgEnt = 0.0
                maxLexStr = wordCluster[0][0]
                maxLexWeight = wordCluster[0][2]
                for wordUnit in wordCluster:
                    word = wordUnit[0]
                    wordWeight = wordUnit[2]
                    avgEnt += wordUnit[3]
                    if wordWeight > maxLexWeight:
                        maxLexStr = word
                        maxLexWeight = wordWeight
#                     groupAttrDic[word] = wordWeight
                    lex_groupStr += (word + ':' + str(wordWeight) + ';')
                avgEnt /= (len(wordCluster))
#                 groupAttrDic[u'avgEnt'] = avgEnt
#                 groupAttrDic[u'groupCnt'] = lex_groupStr
                nameWordStr = maxLexStr + '...'
                node = neoOptObj.createNodeWithProperty('lex-group', nameWordStr, {u'groupCnt' : lex_groupStr, u'avgEnt' : avgEnt})
                lexGroupNodes.append(node)
                print(u'create group node [' + lex_groupStr + u']!')
        return lexGroupNodes
    
    def createLexGroupRelasBtwNodes(self, wvOptObj, neoOptObj, lexNode1, lexNode2, topN_rev, topN, edgeThreshold):
        '''
        '''
        nodeWordList1 = []
        nodeWordList2 = []
        for wordPair in lexNode1[u'groupCnt'].split(u';'):
            if wordPair != u'':
                nodeWordList1.append(wordPair.split(u':')[0])
        for wordPair in lexNode2[u'groupCnt'].split(u';'):
            if wordPair != u'':
                nodeWordList2.append(wordPair.split(u':')[0])
        
        print(str(nodeWordList1) + ' ' + str(nodeWordList2))
        
        relatCopeRes = wvOptObj.copeMSVbtwWordListsFromFile(nodeWordList1, nodeWordList2, topN_rev=topN_rev, topN=topN)
        adjWordProbList = WordTypeFilter().quWordTypeFilterr(relatCopeRes)
        relatLabel = u'lex-semantic'
        relatLabelDic = {}
        maxRelatProb = 0.0
        for adjWord in adjWordProbList:
            wordStr = adjWord[0].split(u'/')[0]
            wordPos = adjWord[0].split(u'/')[1]
            wordProb = adjWord[1]
            if wordProb >= edgeThreshold and wordStr != u'':
                relatLabelDic[wordStr] = (str(wordProb) + u'--' + wordPos)
                if wordProb > maxRelatProb:
                    relatLabel = wordStr
                    maxRelatProb = wordProb
        
        if maxRelatProb > 0.0:
            relationShip = neoOptObj.createRelationshipWithProperty(relatLabel, lexNode1, lexNode2, relatLabelDic)
        else:
            relationShip = neoOptObj.unionSubGraphs([lexNode1, lexNode2])
        print(relationShip)
        
        return relationShip
    
    def unionSemRelatSubGraph(self, neoOptObj, relationShips):
        return neoOptObj.unionSubGraphs(relationShips)
    
    def constructSemGraphOnNeo(self, neoOptObj, subGraph):
        neoOptObj.constructSubGraphInDB(subGraph)
    
    def buildLexGroupSemGraph(self, w2vModelPath, allWordList, lex_cluster=None, vec_z_ratio=100, canopy_t_ratio=3, topN_rev=20, topN=20, edgeThreshold=0.2, unionRange=60):
        graphOptObj = NeoDataGraphOpt()
        w2vOptObj = WordVecOpt(w2vModelPath)    
        print('ready to build lex-group semantic graph!')
        
        lexGroupNodes = self.createLexClustEmtityNodes(graphOptObj, w2vOptObj, allWordList, cluster=lex_cluster, vec_z_ratio=vec_z_ratio, canopy_t_ratio=canopy_t_ratio)
        cacheRelationShips = []
        unionCache = 0
        graphRelatSize = 0
        for i in range(0, len(lexGroupNodes)):
            for j in range(0, len(lexGroupNodes)):
                if i != j:
                    adjRelationShip = self.createLexGroupRelasBtwNodes(w2vOptObj, graphOptObj, lexGroupNodes[i], lexGroupNodes[j], topN_rev, topN, edgeThreshold)
                    if unionCache < unionRange:
                        cacheRelationShips.append(adjRelationShip)
                        print('add lex-group relat to cache pool.')
                        unionCache += 1
                    else:
                        lexSemSubGraph = self.unionSemRelatSubGraph(graphOptObj, cacheRelationShips)
                        self.constructSemGraphOnNeo(graphOptObj, lexSemSubGraph)
                        print('construct lex-graph subgraph cache range: ' + str(unionRange) + '!')
                        graphRelatSize += unionCache
                        unionCache = 0
                        cacheRelationShips = []
        if unionCache > 0:
            lexSemSubGraph = self.unionSemRelatSubGraph(graphOptObj, cacheRelationShips)
            self.constructSemGraphOnNeo(graphOptObj, lexSemSubGraph)
            print('construct lex-graph subgraph cache range: ' + str(unionRange) + '!')
            graphRelatSize += unionCache
        print('construct lex-graph semgraph on neo size: ' + str(graphRelatSize) + '!')

if __name__ == '__main__':
    str = 'aaa;bbb;ccc;ddd;eee;'
    for s in str.split(u';'):
        if s != u'':
            print(s)
    
    p = [('a', 1), ('b', 2), ('c', 3), ('d', 4), ('e', 5)]
    n = []
    n.extend(e[0].decode('utf-8') for e in p)
    print(n)
    