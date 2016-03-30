# -*- coding: UTF-8 -*-

'''
Created on 2016年3月30日

@author: hylovedd
'''

_nounPosTags = []
_not_nounPosTags = []

class wordTypeFilter:
    
    def findNounWord(self, segParaList, nounPosTags=_nounPosTags):
        '''
        找出分词结果形成的词库中所有的名词性词汇（准备作为实体，图中的节点）
        传入所有的分词结果，以列表数组的方式传入
        返回的是一个数组，数组中是过滤得到的名词
        每个过滤结果的形式为：词/词性
        '''
        nounWordsWithPos = []
        for para in segParaList:
            paraPos = para.split(u'/')[1]
            # 是名词 且不是：动名词，形名词，未知词
            if len(nounPosTags) == 0 or nounPosTags == None:
                if (paraPos.find('n') != -1) and (not (paraPos.find('an') != -1 or paraPos.find('vn') != -1 or paraPos.find('un') != -1)):
                    nounWordsWithPos.append(para)
            else:
                if paraPos in nounPosTags:
                    nounWordsWithPos.append(para)
                
        return nounWordsWithPos
    
    def filterNotNounWordDic(self, similarPairList, not_nounPosTags=_not_nounPosTags):
        '''
        找出词向量关联映射对中所有的非名词性词汇（准备作为修饰性关系词，图中的边元素）
        传入词向量关联映射对，以二维列表数组的方式传入
        返回的同样是字典数组，数组中是过滤得到的 修饰词:概率 映射对
        修饰词的形式是 词/词性 组合
        '''
        adjWordsProbMap = {}
        for pair in similarPairList:
            word = pair[0]
            prob = pair[1]
            wordPos = word.split(u'/')[1]
            if len(not_nounPosTags) == 0 or not_nounPosTags == True:
                if (wordPos.find('n') == -1) or (wordPos.find('an') != -1 or wordPos.find('vn') != -1 or wordPos.find('un') != -1):
                    adjWordsProbMap[word] = prob
            else:
                if wordPos in not_nounPosTags:
                    adjWordsProbMap[word] = prob
        
        return adjWordsProbMap

if __name__ == '__main__':
    word = u'韩寒/nr'
    pos = word.split(u'/')[1]
    
    print word
