# -*- coding: UTF-8 -*-

'''
Created on 2015年10月25日

@author: hylovedd
'''
from numpy import *

def file2matrix(filePath):
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

if __name__ == '__main__':
    pass