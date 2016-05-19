# -*- coding: UTF-8 -*-
'''
Created on 2016年5月16日

@author: superhy
'''

from org_ailab_cluster.SOMNetWork import KohonenSOM
from org_ailab_seg.word2vec.wordTypeFilter import wordTypeFilter


class lexClustSemanticsGraph(object):
    
    def createLexClustEmtityNodes(self, neoOptObj, wvOptObj, wordList, cluster=None, canopy_t_ratio=3):
        '''
        '''
        if cluster == None:
            cluster = KohonenSOM(wvOptObj._size)
        
        wordPairs = []
        for word in wordList:
            wordPair = [word, 0.0]
            wordPairs.append(wordPair)
        entityWordPairs = wordTypeFilter().entityWordFilter(wordPairs)
        
        # run the word cluster
        wordMatrixDic = {}
        for wordPair in entityWordPairs:
            word = wordPair[0]
            if word.split(u'/')[0] != u'':
                wordVec = wvOptObj.getWordVecfromFile(word)
                wordMatrixDic[word] = wordVec
                print(u'get word vec: ' + word + u'(' + str(wordVec) + u')')
        wordClusters, wordClustResDic = cluster.clust(wordMatrixDic, canopy_t_ratio)
        print(u'finish word clust!')
        
        lexGroupNodes = []
        for wordCluster in wordClusters:
            if len(wordCluster) != 0:
                lex_groupStr = ''
                avgEnt = 0.0
                for wordUnit in wordCluster:
                    word = wordUnit[0]
                    wordWeight = wordUnit[2]
                    avgEnt += wordUnit[3]
                    lex_groupStr += (word + ':' + str(wordWeight) + ';')
                avgEnt /= (len(wordCluster))
                node = neoOptObj.createNodeWithProperty('lex-group', lex_groupStr, {u'avgEnt' : avgEnt})
                lexGroupNodes.append(node)
                print(u'create group node [' + lex_groupStr + u']!')
        return lexGroupNodes
    
    def createLexGroupRelasBtwNodes(self, wvOptObj, neoOptObj, lexNode1, lexNode2, topN_rev, topN, edgeThreshold):
        nodeWordList1 = []
        nodeWordList2 = []
        for wordPair in lexNode1[u'name'].split(u';'):
            if wordPair != u'':
                nodeWordList1.append(wordPair.split(u':')[0])
        for wordPair in lexNode2[u'name'].split(u':'):
            if wordPair != u'':
                nodeWordList2.append(wordPair.split(u':')[0])
        
        
#         revMSimilarVecList = wvOptObj.queryMSVwithPosNegFromFile([], nodeWordList2, topN=topN_rev)
        

if __name__ == '__main__':
    str = 'aaa;bbb;ccc;ddd;eee;'
    for s in str.split(u';'):
        if s != u'':
            print(s)
    
    p = [('a', 1), ('b', 2), ('c', 3), ('d', 4), ('e', 5)]
    n = []
    n.extend(e[0] for e in p)
    print(n)
    