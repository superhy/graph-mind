# -*- coding: UTF-8 -*-

'''
Created on 2016年3月30日

@author: hylovedd
'''

class wordTypeFilter:
    
    def findNounWord(self, segParaList):
        nounWordsWithPos = []
        for para in segParaList:
            paraPos = para.split(u'/')[1]
            # 是名词 且不是：动名词，形名词，未知词
            if (paraPos.find('n')) and (not (paraPos.find('an') or paraPos.find('vn') or paraPos.find('un'))):
                nounWordsWithPos.append(para)
                
        return nounWordsWithPos
    
    def filterNotNounWordDic(self, similarPairList):
        pass

if __name__ == '__main__':
    pass