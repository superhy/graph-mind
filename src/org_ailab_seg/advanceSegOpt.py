# -*- coding: UTF-8 -*-

'''
Created on 2016年1月9日

@author: superhy
'''

class advanceSegOpt:
    
    def conutAvgWordsNum(self, segParaList):
        paraNum = len(segParaList)
        allWordsNum = 0
        for segPara in segParaList:
            segStr = '/'.join(segPara)
            segWords = segStr.split('/')
            allWordsNum += len(segWords)
            
        avgWordsNum = allWordsNum * 1.0 /paraNum
        
        return avgWordsNum

if __name__ == '__main__':
    pass