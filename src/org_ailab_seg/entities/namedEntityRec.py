# -*- coding: UTF-8 -*-

'''
Created on 2016年6月5日

@author: hylovedd
'''

import re


class ner(object):
    def __init__(self, trainTextDir=None, NEWordToupleFilePath=None):
        self._trainTextDir = trainTextDir
        self._NEWordDicPath = NEWordToupleFilePath
    
    def taggingTrainText(self, trainSentenceList, NEWordToupleList):
        '''
        '''
        trainCorpusText = trainSentenceList[0]
        for i in range(1, len(trainSentenceList)):
            trainCorpusText += (u'-\-' + trainSentenceList[i])
        for neWordTouple in NEWordToupleList:
            if trainCorpusText.find(neWordTouple[0]) != -1:
                replaceEntity = u'<START:' + neWordTouple[1] + u'>' + neWordTouple[0] + u'<END>'
                trainCorpusText.replace(neWordTouple[0], replaceEntity)
                
        tagTrainSentenceList = trainCorpusText.split(u'-\-')
        print(u'---finish tagging name parts on text---')
        
        return tagTrainSentenceList
    
    def interceptEntityPart(self, sentence):
        parts = []
        rest_sentence = sentence
        while(True):
            if rest_sentence.find(u'<START') == -1:
                break
            # fetch the none part
            none_part = rest_sentence[ : rest_sentence.find(u'<START')]
            parts.append((u'none', none_part))
            # fetch the named part part
            entity_part = rest_sentence[rest_sentence.find(u'>') + 1 : rest_sentence.find(u'<END>')]
            entity_tag = rest_sentence[rest_sentence.find(u':') + 1 : rest_sentence.find(u'>')]
            parts.append((entity_tag, entity_part))
            rest_sentence = rest_sentence[rest_sentence.find(u'<END>') + 5 : ]
        # the last part
        if(len(rest_sentence)):
            parts.append((u'none', rest_sentence))
        
        return parts
    
    def transTagSentencesIntoRole(self, tagTrainSentenceList, preWinSize, latWinSize):
        '''
        '''
        for sentence in tagTrainSentenceList:
            if type(sentence).__name__ != "unicode":
                sentence = sentence.decode('utf-8')
            if sentence.find(u'<START') != -1:
                sentence_part = self.interceptEntityPart(sentence)
                for i in range(0, len(sentence_part)):
                    pass
                
if __name__ == '__main__':
    s = '习近平总书记表扬小明，小明硕士毕业于<START:pos>中国科学院计算所<END>，后在<START:pos>日本京都大学<END>深造'
#     s = '习近平总书记表扬小明，小明硕士毕业于中国科学院计算所，后在日本京都大学深造'
    s = s.decode('utf-8')
    p = s.find('<START')
    
    print(type('习近平').__name__)
    s1 = '习近平'
    s1 = s1.decode('utf-8')
    print(type(s1).__name__)
    print(len('习近平'.decode('utf-8')))
#     print(s[p - 1])
    
    parts = ner().interceptEntityPart(s)
    for part in parts:
        print(part[0] + u' ' + part[1])
