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
            wordVec = wvOptObj.getWordVecfromFile(word)
            wordMatrixDic[word] = wordVec
        wordClusters, wordClustResDic = cluster.clust(wordMatrixDic, canopy_t_ratio)
        #TODO
        
        lexGroupNodes = []

if __name__ == '__main__':
    pass
