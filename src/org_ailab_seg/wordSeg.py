# -*- coding: UTF-8 -*-

'''
Created on 2016年1月9日

@author: hylovedd
'''
import jieba
from jieba import posseg

class wordSeg:
    def __init__(self, segMode, paraList):
        self.segMode = segMode
        self.paraList = paraList
        
    def singleSegEngine(self, segStr):
        wordGenList = []
        if self.segMode == 'a':
            wordGenList = jieba.cut(segStr, cut_all=True)
        elif self.segMode == 's':
            wordGenList = jieba.cut_for_search(segStr)
        else:
            wordGenList = jieba.cut(segStr, cut_all=False)
        
        wordStr = '_'.join(wordGenList)
        wordList = wordStr.split('_')
            
        return wordList
    
    def singlePosSegEngine(self, segStr):
        wordPosGenList = posseg.cut(segStr, HMM=True)
        
        wordPosList = []
        for wordPair in wordPosGenList:
            wordPosList.append(u'/'.join(wordPair))
        
        return wordPosList
    
    def serialSeger(self, posNeedFlag=False):
        segParaList = []
        if posNeedFlag == True:
            for para in self.paraList:
                segParaList.append(self.singlePosSegEngine(para))
        else:
            for para in self.paraList:
                segParaList.append(self.singleSegEngine(para))
        
        return segParaList

if __name__ == '__main__':
    mainObj = wordSeg('e', [])
    segRes = mainObj.singleSegEngine('我爱北京天安门')
    segRes2 = mainObj.singlePosSegEngine('我爱北京天安门')
        
    writenStr = ' '.join(segRes2)
    print writenStr
