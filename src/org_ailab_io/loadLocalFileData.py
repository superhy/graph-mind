# -*- coding: UTF-8 -*-

'''
Created on 2015年10月25日

@author: hylovedd
'''

import os


def checkFile(file):
    if os.path.exists(file) == False:
        return u'none'
    elif os.path.isfile(file):
        return u'file'
    else:
        return u'other'

if __name__ == '__main__':
    pass