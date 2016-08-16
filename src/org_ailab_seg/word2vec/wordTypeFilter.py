# -*- coding: UTF-8 -*-

'''
Created on 2016年3月30日

@author: hylovedd
'''

from gensim.models.word2vec import LineSentence

from org_ailab_tools.cache import WORD_POS
from test_ailab_seg.segSentiWbTest import segSentiWbTest


_entityPosTags = WORD_POS.noun
_qualifyPosTags = WORD_POS.place + WORD_POS.verb + WORD_POS.adj + WORD_POS.dist + WORD_POS.adv

class wordTypeFilter(object):
    
    def entityWordFilter(self, wordProbPairList, entityPosTags=_entityPosTags, scanRange=None):
        '''
        (using Chinese notes)
        找出分词结果形成的词库中所有的名词性词汇（准备作为实体，图中的节点）
        传入所有的分词结果以及生成概率对，以列表数组的方式传入
        返回的是一个数组，数组中是过滤得到的名词
        每个过滤结果的形式为：词/词性
        '''
        entityWordPairs = []
        for wordPair in wordProbPairList:
            word = wordPair[0]
            wordPos = word.split(u'/')[1]
                
            hitFlag = False
            for tagPos in entityPosTags:
                if wordPos.startswith(tagPos):
                    hitFlag = True
                    break
            if hitFlag == True:
                entityWordPairs.append(wordPair)
            
            if scanRange != None and len(entityWordPairs) >= scanRange:
                break
            
        return entityWordPairs
    
    def qualifyWordFilter(self, wordProbPairList, qualifyPosTags=_qualifyPosTags):
        '''
        (using Chinese notes)
        找出词向量关联映射对中所有的非名词性词汇（准备作为修饰性关系词，图中的边元素）
        传入词向量关联映射对，以二维列表数组的方式传入
        返回的同样是字典数组，数组中是过滤得到的 修饰词:概率 映射对
        修饰词的形式是 词/词性 组合
        '''
        qualifyWordPairs = []
        for wordPair in wordProbPairList:
            word = wordPair[0]
            wordPos = word.split(u'/')[1]
            
            hitFlag = False
            for tagPos in qualifyPosTags:
                if wordPos.startswith(tagPos):
                    hitFlag = True
                    break
            if hitFlag ==True:
                qualifyWordPairs.append(wordPair)
        
        return qualifyWordPairs
    
    def diyWordFilter(self, wordProbPairList, filterPosTags):
        '''
        (using Chinese notes)
        自定义词过滤器，自我传入想保留的词性标签
        '''
        filterWordPairs = []
        for wordPair in wordProbPairList:
            word = wordPair[0]
            wordPos = word.split(u'/')[1]
            
            hitFlag = False
            for tagPos in filterPosTags:
                if wordPos.startswith(tagPos):
                    hitFlag = True
                    break
            if hitFlag ==True:
                filterWordPairs.append(wordPair)
        
        return filterWordPairs
    
    def ditInOutWordFilter(self, wordProbPairList, inOutEntities, filterType):
        '''
        get the word in or out entity dit from wordPairList
        filterType is the string of 'in' or 'out'
        '''
        
        filtWordPairs = []
        if filterType == 'in':
            for wordPair in wordProbPairList:
                word = wordPair[0]
                if word in inOutEntities:
                    filtWordPairs.append(wordPair)
        elif filterType == 'out':
            for wordPair in wordProbPairList:
                word = wordPair[0]
                if word not in inOutEntities:
                    filtWordPairs.append(wordPair)
            
        return filtWordPairs
    
    def collectAllWordsFromSegSentences(self, segSetences):
        allWordList = []
        for sentence in segSetences:
            for word in sentence:
                if not (word in allWordList):
                    allWordList.append(word)
        return allWordList
    
    def collectAllWordsFromSegFile(self, segFilePath):
        segFile = open(segFilePath, u'r')
        segSetences = LineSentence(segFile)
        return self.collectAllWordsFromSegSentences(segSetences)

if __name__ == '__main__':
    word = u'韩寒/nr'
    wordPos = word.split(u'/')[1]
    
    print wordPos.startswith(u'n')
    print _qualifyPosTags
