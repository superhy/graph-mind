# -*- coding: UTF-8 -*-

'''
Created on 2016年1月9日

@author: hylovedd
'''

class segSentiWbTest:
    def __init__(self, filePath):
        self.filePath = filePath
    
    def fetchParaText(self):
        fileObj = open(self.filePath)
        paraTextList = []
        try:
            fileAllText = fileObj.read()
        finally:
            fileObj.close()

if __name__ == '__main__':
    pass