# -*- coding: UTF-8 -*-
'''
Created on 2016年4月20日

@author: superhy
'''
from orgword_segtraSegOpt import ExtraSegOpt
from orgtoolsche import ROOT_PATH


def countWordPos():
    ExtraSegOpt().reLoadEncoding()
    
    segFile = open(ROOT_PATH.root_win64 + 'weibo_seg\\segNLPCC2014.txt', 'r')
    segLines = segFile.readlines()
    dic = {}
    for line in segLines:
        words = line.split(' ')
        for word in words:
            if word.find('/') != -1:
                word_str = word.split('/')[0]
                seg = word.split('/')[1]
                if dic.has_key(seg) and len(dic[seg]) < 5:
                    dic[seg].append(word_str)
                elif not dic.has_key(seg):
                    dic[seg] = [word_str]
#                 else:
#                     print(seg + ": "),
#                     for s in dic[seg]:
#                         print(s.encode('utf-8') + ';'),
#                     print('')
    segFile.close()
    
    for key in dic:
        if key.startswith('x'):
            print(key + ": "),
            for s in dic[key]:
                print(s.encode('utf-8') + ';'),
            print('')
    
#     posListFileStr = ''
#     fileWriteObj = open(u'NLPCC2014WordPosList.txt', 'w')
#     for key in dic:
#         posListFileStr += (key + ': [')
#         for w in dic[key]:
#             posListFileStr += (w + ';')
#         posListFileStr += ']\n'
#     fileWriteObj.write(posListFileStr)
#     fileWriteObj.close()

if __name__ == '__main__':
    countWordPos()
