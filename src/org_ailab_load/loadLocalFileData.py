# -*- coding: UTF-8 -*-

'''
Created on 2015年10月25日

@author: hylovedd
'''

from numpy import zeros
import os


# ML book test
def filedata2matrix(filePath):
    fr = open(filePath)
    numberOfLines = len(fr.readlines())
    returnMat = zeros((numberOfLines, 3))
    classLabelVector = []
    fr = open(filePath)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index, :] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat, classLabelVector

def checkFile(filePath):
    if os.path.exists(filePath) == False:
        return u'null'
    elif os.path.isdir(filePath):
        return u'dir'
    elif os.path.isfile(filePath):
        return u'file'
    else:
        return u'error'

if __name__ == '__main__':
    pass