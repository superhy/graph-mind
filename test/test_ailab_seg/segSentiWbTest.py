# -*- coding: UTF-8 -*-

'''
Created on 2016年1月9日

@author: hylovedd
'''
from bs4 import BeautifulSoup
from org_ailab_seg.wordSeg import wordSeg

class segSentiWbTest:
    def __init__(self, filePath):
        self.filePath = filePath
    
    def fetchParaText(self):
        fileObj = open(self.filePath)
        paraTextList = []
        try:
            fileAllText = fileObj.read()
            
            soup = BeautifulSoup(fileAllText)
            soupEles = soup.find_all('review')
            for ele in soupEles:
                paraTextList.append(ele.get_text().encode('utf-8'))
        finally:
            fileObj.close()
            
        return paraTextList
    
    def segParaText(self, segMode):
        paraTextList = self.fetchParaText()
        testSeger = wordSeg(segMode, paraTextList)
        
        segParaList = testSeger.serialSeger()
        
        return segParaList

if __name__ == '__main__':
    filePath = u'sample.positive.txt'
    segObj = segSentiWbTest(filePath)
