# -*- coding: UTF-8 -*-

'''
Created on 2016年1月9日

@author: hylovedd
'''

from jieba import posseg
import jieba
import jieba.analyse


class wordSeg(object):
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
    
    segRes = mainObj.singleSegEngine('习近平总书记表扬小明，小明硕士毕业于中国科学院计算所，后在日本京都大学深造')
#     segRes2 = mainObj.singlePosSegEngine('习近平总书记在北京市朝阳区表扬小明，小明硕士毕业于中国科学院计算所，后在日本京都大学深造') 
    segRes2 = mainObj.singlePosSegEngine('我最近参加了高校主办的北清大数据联合会中文的一系列活动')
    
    print(' '.join(segRes2))
    
    for word in segRes2:
        print(word)
        
#     for segPair in segRes2:
#         if segPair.split('/')[1].startswith('nr'):
#             print('person: ' + segPair.split(u'/')[0])
#         elif segPair.split('/')[1].startswith('ns'):
#             print('position: ' + segPair.split(u'/')[0])
#         elif segPair.split('/')[1].startswith('nt'):
#             print('organization: ' + segPair.split(u'/')[0])
    