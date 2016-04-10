# -*- coding: UTF-8 -*-

'''
Created on 2016年1月9日

@author: superhy
'''

from nltk.util import pr


class extraSegOpt:
    
    def reLoadEncoding(self):
        # 重新载入字符集
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')
    
    def conutAvgWordsNum(self, segParaList):
        paraNum = len(segParaList)
        allWordsNum = 0
        
        for segPara in segParaList:
            allWordsNum += len(segPara)
            
        avgWordsNum = allWordsNum * 1.0 / paraNum
        
        return avgWordsNum
    
    def writeIntoFile(self, filePath, segParaList):
        self.reLoadEncoding()
        # 以覆盖写入方式打开文件
        fileObj = file(filePath, 'w')
        writenStr = ''
        for segPara in segParaList:
            segStr = ''
            for segWord in segPara:
                segStr += (u' ' + segWord)
            print segStr
            writenStr += (segStr + u'\r\n')
        fileObj.write(writenStr)
        fileObj.close()

if __name__ == '__main__':
    pass
