# -*- coding: UTF-8 -*-

'''
Created on 2016年7月21日

@author: hylovedd
'''
import platform

root_win64 = 'D:\\graph-mind-file\\'
root_macos = ''
root_linux = '/home/superhy/graph-mind-file/'

seg_dictwin64 = 'D:\\graph-mind-file\\seg_dict\\'

def auto_config_root():
    
    global root_linux
    global root_macos
    global root_win64
    
    if platform.system() == 'Windows':
        return root_win64;
    elif platform.system() == 'Linux':
        return root_linux;
    else:
        return ''