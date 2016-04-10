# -*- coding: UTF-8 -*-

'''
Created on 2016年4月11日

@author: hylovedd
'''

from org_ailab_data.graph.neoDataGraphOpt import neoDataGraphOpt
from org_ailab_seg.word2vec.wordVecOpt import wordVecOpt


class wordSemanticsGraph():
    
    def createBasicNounNodes(self, wvOptObj, wordList):
        nounNodes = []
        for word in wordList:
            wordStr = word.split(u'/')[0]
            wordPos = word.split(u'/')[1]
            node = wvOptObj.createNodeWithProperty('noun', wordStr, {u'pos' : wordPos})
            nounNodes.append(node)
        return nounNodes
    
    def buildBasicSemGraph(self, w2vModelPath, wordList, topN=20):
        graphDBBeanObj = neoDataGraphOpt()
        wvOptObj = wordVecOpt(w2vModelPath)                    
    
if __name__ == '__main__':
    pass