# -*- coding: UTF-8 -*-

'''
Created on 2016年7月29日

@author: hylovedd
'''
from org_ailab_tools.cache import ROOT_PATH
from org_ailab_kg import freqAssGraphSupOpt


def testLoadEntitiesFromDict():
    dict_path = ROOT_PATH.seg_dictwin64 + u'jieba_shicai.txt'
    
    entities = freqAssGraphSupOpt.loadEntitiesFromDict(dict_path)
    
    for entity in entities:
        print(entity)

if __name__ == '__main__':
    testLoadEntitiesFromDict()