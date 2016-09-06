# -*- coding: UTF-8 -*-

'''
Created on 2016年4月11日

@author: hylovedd
'''

from org_ailab_data.graph.neoDataGraphOpt import NeoDataGraphOpt
from org_ailab_seg.word2vec.wordTypeFilter import WordTypeFilter
from org_ailab_seg.word2vec.wordVecOpt import WordVecOpt

class BasicSemanticsGraph(object):
    '''
    TODO
    设置基类，继承，统一管理共享参数，如：是否直接传入实体词列表等等
    '''
    
    def createBasicEmtityNodes(self, neoOptObj, wordList):
        # transform wordList into wordPairs
        wordPairs = []
        for word in wordList:
            wordPair = [word, 0.0]
            wordPairs.append(wordPair)
        entityWordPairs = WordTypeFilter().enWordTypeFilter(wordPairs)
        
        nounNodes = []
        for wordPair in entityWordPairs:
            word = wordPair[0]
            wordStr = word.split(u'/')[0]
            wordPos = word.split(u'/')[1]
            if wordStr != u'':
                node = neoOptObj.createNodeWithProperty('noun', wordStr, {u'pos' : wordPos})
                nounNodes.append(node)
                print(u'create node [' + word + u']!')
        return nounNodes
    
    def createBasicRelasBtwNodes(self, wvOptObj, neoOptObj, nounNode1, nounNode2, topN, edgeThreshold):
        nodeWord1 = nounNode1[u'name'] + u'/' + nounNode1[u'pos']
        nodeWord2 = nounNode2[u'name'] + u'/' + nounNode2[u'pos']
        posWordList = [nodeWord1, nodeWord2]
        negWordList = []
        
        relatQueryRes = wvOptObj.queryMSVwithPosNegFromFile(posWordList, negWordList, topN=topN)
        adjWordProbList = WordTypeFilter().quWordTypeFilterr(relatQueryRes)
        relatLabel = u'semantic'
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
            relationShip = neoOptObj.createRelationshipWithProperty(relatLabel, nounNode1, nounNode2, relatLabelDic)
        else:
            relationShip = neoOptObj.unionSubGraphs([nounNode1, nounNode2])
        # print(relatLabelDic)
        print(relationShip)
        # print(u'create relationship from [' + nodeWord1 + u'] to [' + nodeWord2 + u']!')
        return relationShip
    
    def unionSemRelatSubGraph(self, neoOptObj, relationShips):
        return neoOptObj.unionSubGraphs(relationShips)
    
    def constructSemGraphOnNeo(self, neoOptObj, subGraph):
        neoOptObj.constructSubGraphInDB(subGraph)
    
    def buildBasicSemGraph(self, w2vModelPath, allWordList, topN=20, edgeThreshold=0.2, unionRange=60):
        graphOptObj = NeoDataGraphOpt()
        w2vOptObj = WordVecOpt(w2vModelPath)     
        print('ready to build semantic graph!')
        
        nounNodes = self.createBasicEmtityNodes(graphOptObj, allWordList)
        cacheRelationShips = []
        unionCache = 0
        graphRelatSize = 0;
        for i in range(0, len(nounNodes)):
            for j in range(0, len(nounNodes)):
                if i != j:
                    adjRelationShip = self.createBasicRelasBtwNodes(w2vOptObj, graphOptObj, nounNodes[i], nounNodes[j], topN, edgeThreshold)
                    if unionCache < unionRange:
                        cacheRelationShips.append(adjRelationShip)
                        print('add relat to cache pool.')
                        unionCache += 1
                    else:
                        semSubGraph = self.unionSemRelatSubGraph(graphOptObj, cacheRelationShips)
                        self.constructSemGraphOnNeo(graphOptObj, semSubGraph)
                        print('construct subgraph cache range: ' + str(unionRange) + '!')
                        graphRelatSize += unionCache
                        unionCache = 0
                        cacheRelationShips = []
        if unionCache > 0:
            semSubGraph = self.unionSemRelatSubGraph(graphOptObj, cacheRelationShips)
            self.constructSemGraphOnNeo(graphOptObj, semSubGraph)
            print('construct surplus subgraph size: ' + str(unionCache) + '!')
            graphRelatSize += unionCache
        print('construct semgraph on neo size: ' + str(graphRelatSize) + '!')
    
if __name__ == '__main__':
    pass
#     path = os.getcwd()
#     print(path)
#     print(path.rindex('ailab-mltk-py'))
    
