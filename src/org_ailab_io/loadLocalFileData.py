# -*- coding: UTF-8 -*-

'''
Created on 2015年10月25日

@author: hylovedd
'''

import os
import types


def checkFileState(file):
    '''
    (file can be a file path or other object)
    '''
    fileObjectType = type(file)
    if fileObjectType is types.StringType:
        if os.path.isdir(file):
            return u'directory'
        elif os.path.isfile(file):
            return u'file'
        else:
            return u'error'
    else:
        return u'other'

if __name__ == '__main__':
    model = None
    model = 'ok'
    print(type(model) == types.StringType or types.BooleanType)