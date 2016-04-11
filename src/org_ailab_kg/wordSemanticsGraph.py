# -*- coding: UTF-8 -*-

'''
Created on 2016年4月11日

@author: hylovedd
'''

import os

from blaze.expr.core import path

from org_ailab_data.graph.neoDataGraphOpt import neoDataGraphOpt
from org_ailab_seg.word2vec.wordTypeFilter import wordTypeFilter
from org_ailab_seg.word2vec.wordVecOpt import wordVecOpt


class wordSemanticsGraph():
    
    def createBasicNounNodes(self, neoOptObj, wordList):
        nounWordList = wordTypeFilter().findNounWord(wordList)
        
        nounNodes = []
        for word in nounWordList:
            wordStr = word.split(u'/')[0]
            wordPos = word.split(u'/')[1]
            if wordStr != u'':
                node = neoOptObj.createNodeWithProperty('noun', wordStr, {u'pos' : wordPos})
                nounNodes.append(node)
                print(u'create node [' + word + u']!')
        return nounNodes
    
    def createBasicRelasBtwNounNodes(self, wvOptObj, neoOptObj, nounNode1, nounNode2, topN):
        nodeWord1 = nounNode1[u'name'] + u'/' + nounNode1[u'pos']
        nodeWord2 = nounNode2[u'name'] + u'/' + nounNode2[u'pos']
        posWordList = [nodeWord1, nodeWord2]
        negWordList = []
        
        relatQueryRes = wvOptObj.queryMSVwithPosNegFromFile(posWordList, negWordList, topN=topN)
        adjWordProbList = wordTypeFilter().filterNotNounWordDic(relatQueryRes)
        relatLabel = u'semantic'
        for i in range(0, len(adjWordProbList)):
            if adjWordProbList[i][0].split(u'/')[0] != u'':
                relatLabel = adjWordProbList[i][0].split(u'/')[0]
                break
        relatLabelDic = {}
        for adjWord in adjWordProbList:
            wordStr = adjWord[0].split(u'/')[0]
            wordPos = adjWord[0].split(u'/')[1]
            wordProb = adjWord[1]
            if wordStr != u'':
                relatLabelDic[wordStr] = (str(wordProb) + u'--' + wordPos)
            
        relationShip = neoOptObj.createRelationshipWithProperty(relatLabel, nounNode1, nounNode2, relatLabelDic)
        print(relatLabelDic)
        print(relationShip)
        # print(u'create relationship from [' + nodeWord1 + u'] to [' + nodeWord2 + u']!')
        return relationShip
    
    def unionSemRelatSubGraph(self, neoOptObj, relationShips):
        return neoOptObj.unionSubGraphs(relationShips)
    
    def constructSemGraphOnNeo(self, neoOptObj, subGraph):
        neoOptObj.constructSubGraphInDB(subGraph)
    
    def buildBasicSemGraph(self, w2vModelPath, allWordList, topN=20):
        graphOptObj = neoDataGraphOpt()
        wvOptObj = wordVecOpt(w2vModelPath)
        
        print('ready to build semantic graph!')
        
        nounNodes = self.createBasicNounNodes(graphOptObj, allWordList)
        allRelationShips = []
        for i in range(0, len(nounNodes)):
            for j in range(0, len(nounNodes)):
                if i != j:
                    adjRelationShip = self.createBasicRelasBtwNounNodes(wvOptObj, graphOptObj, nounNodes[i], nounNodes[j], topN)
                    allRelationShips.append(adjRelationShip)
        semSubGraph = self.unionSemRelatSubGraph(graphOptObj, allRelationShips)
        self.constructSemGraphOnNeo(graphOptObj, semSubGraph)
        print('construct semgraph on neo!')
    
if __name__ == '__main__':
    pass
#     path = os.getcwd()
#     print(path)
#     print(path.rindex('ailab-mltk-py'))
    
