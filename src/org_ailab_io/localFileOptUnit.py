# -*- coding: UTF-8 -*-

'''
Created on 2015年10月25日

@author: hylovedd
'''

import os
import types


def checkFileState(filePath):
    '''
    (filePath can be a file path or other object)
    '''
    fileObjectType = type(filePath)
    print(fileObjectType)
    
    if fileObjectType is types.FileType:
        return u'opened'
    elif fileObjectType is types.StringType or types.UnicodeType:
        if os.path.isdir(filePath):
            return u'directory'
        elif os.path.isfile(filePath):
            return u'file'
        else:
            return u'error'
    else:
        return u'other'

def listAllFileInDirectory(dirPath, io=u'r'):
    '''
    list all file in a directory from dir file
    '''
    loadedFiles = []
    files = os.listdir(dirPath)
    for file in files:
        print file
        loadedFiles.append(open(file, io))
    return loadedFiles

if __name__ == '__main__':
    files = listAllFileInDirectory(u'../org_ailab_io')
    for file in files[2:len(files)]:
        print(checkFileState(file))
    