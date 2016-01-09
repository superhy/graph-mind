# -*- coding: UTF-8 -*-

'''
Created on 2016年1月9日

@author: hylovedd
'''
import jieba

class wordSeg:
    def __init__(self, segMode, paraList):
        self.segMode = segMode
        self.paraList = paraList
        
    def singleSegEngine(self, segStr):
        wordList = []
        if self.segMode == 'a':
            wordList = jieba.cut(segStr, cut_all = True)
        elif self.segMode == 's':
            wordList = jieba.cut_for_search(segStr)
        else:
            wordList = jieba.cut(segStr, cut_all = False)
            
        return wordList
    
    def serialSeger(self):
        segParaList = []
        for para in self.paraList:
            segParaList.append(self.singleSegEngine(para))
        
        return segParaList

if __name__ == '__main__':
    mainObj = wordSeg('e', [])
    segRes = mainObj.singleSegEngine('我爱北京天安门')
        
    for word in segRes:
        print word