# -*- coding: UTF-8 -*-

'''
Created on 2015年10月25日

@author: hylovedd
'''

import os
import types

from gensim.models.word2vec import LineSentence
from jieba import posseg

from org_ailab_seg.extraSegOpt import ExtraSegOpt
from org_ailab_tools.cache import ROOT_PATH


def checkFileState(filePath):
    '''
    (filePath can be a file path or other object)
    '''
    fileObjectType = type(filePath)
#     print(u'filePath object type is ' + str(fileObjectType))
    
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

def listAllFilePathInDirectory(dirPath):
    '''
    list all file_path in a directory from dir folder
    '''
    ExtraSegOpt().reLoadEncoding()
    
    loadedFilesPath = []
    files = os.listdir(dirPath)
    # TODO need improve code to one line
    for file in files:
        filePath = dirPath + file
#         print(filePath)
        
        loadedFilesPath.append(filePath)

    return loadedFilesPath

def loadSetencesFromFiles(filePaths):
    '''
    load all sentences list from filePaths
    '''
    sentences = []
    for filePath in filePaths:
        sentences.extend(LineSentence(filePath))
    return sentences

def folderFilesNameEntities(corpusDirPath, userDictPath=None, dictRewrite=False):
    '''
    get entities from folder files' names
    write these entities into user_dict for jieba analyser(chose)
    '''
    ExtraSegOpt().reLoadEncoding()
    
    entities = []
    files = os.listdir(corpusDirPath)
    for file in files:
        fileName = file[:file.find(u'(seg)')]
        extra = u''
        if fileName.find(u'（') != -1 and fileName.find(u'）') != -1:
            extra = fileName[fileName.find(u'（') + 1:fileName.find(u'）')]
        if fileName.find(u'(') != -1 and fileName.find(u')') != -1:
            extra = fileName[fileName.find(u'(') + 1:fileName.find(u')')]
        if len(extra) != 0:
            if fileName.find(extra) - 1 == 0:
                fileName = fileName[fileName.find(extra) + len(extra) + 1:]
            else:
                fileName = fileName[:fileName.find(extra) - 1]
        if fileName not in entities:      
            entities.append(fileName)
            
    # write user's word directory
    if userDictPath != None:
        entitiesFwStr = ''
        for i in range(len(entities)):
            entitiesFwStr += (entities[i] + u' n')
            if not i == len(entities) - 1:
                entitiesFwStr += u'\n'
        
        mode = 'w' if dictRewrite == False else 'w+'
        fw = open(userDictPath, mode)
        fw.write(entitiesFwStr)
        fw.close()
    
    return entities
            
if __name__ == '__main__':
#     files = listAllFilePathInDirectory(u'../org_ailab_tools')
#     for file in files[2:len(files)]:
#         print(checkFileState(file))
    
    entities = folderFilesNameEntities(ROOT_PATH.root_win64 + u'med_seg\\食材百科', ROOT_PATH.seg_dictwin64 + u'jieba_shicai.txt')  # Chinese character need unicode
    for entity in entities:
        print(entity)
