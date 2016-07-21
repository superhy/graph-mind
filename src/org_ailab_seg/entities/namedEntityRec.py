# -*- coding: UTF-8 -*-

'''
Created on 2016年6月5日

@author: hylovedd
'''

from org_ailab_seg.wordSeg import wordSeg
from org_ailab_seg.entities import nerStatisticalOpt
from org_ailab_classifier.prob_graph.hmm import hiddenMarkov
from json.encoder import JSONEncoder
from json.decoder import JSONDecoder

class tagPOSSeqModel(object):
    def __init__(self, tagStartP, tagPOSEmitP, tagHiddens, tag2tagTransP):
        self._tagStartP = tagStartP
        self._tagPOSEmitP = tagPOSEmitP
        self._tagHiddens = tagHiddens
        self._tag2tagTransP = tag2tagTransP
        
    def trainModel(self, tagMatrix, POSSeq, modelDiskPath=None):
        '''
        '''
        start_p = nerStatisticalOpt.cptStartP(tagMatrix)
        emit_p = nerStatisticalOpt.cptEmitP(tagMatrix)
        tag_states, trans_p = nerStatisticalOpt.cptTags_TransP(tagMatrix)
        
        model = self.__init__(start_p, emit_p, tag_states, trans_p)
        
        if modelDiskPath != None:
            try:
                modelWriteObj = open(modelDiskPath, 'w')
                
                modelLines = []
                start_p_line = 'start_p@' + JSONEncoder().encode(tagPOSSeqModel._tagStartP)
                emit_p_line = 'emit_p@' + JSONEncoder().encode(tagPOSSeqModel._tagPOSEmitP)
                tag_states = 'tag_states@' + JSONEncoder().encode(model._tagHiddens)
                trans_p = 'trans_p@' + JSONEncoder().encode(model._tag2tagTransP)
                modelLines.append(start_p_line)
                modelLines.append(emit_p_line)
                modelLines.append(tag_states)
                modelLines.append(trans_p)
                modelWriteObj.writelines(modelLines)
                
                modelWriteObj.close()
            
            except Exception, e:
                print 'write model into disk failed: ', e
        
        return model
    
    def loadModelFromDisk(self, modelDiskPath):
        '''
        '''
        modelReadObj = open(modelDiskPath, 'r')
        
        modelLines = modelReadObj.readlines()
        modelCntDic = {'start_p' : None, 'emit_p' : None, 'tag_states' : None, 'trans_p' : None}
        for line in modelLines:
            label, element = line[ : line.find('@')], JSONDecoder().decode(line[line.find('@') + 1 :])
            modelCntDic[label] = element
        if None in modelCntDic.values():
            print('model with some errors, please check!')
            return None
        
        model = self.__init__(modelCntDic['start_p'], modelCntDic['emit_p'], modelCntDic['tag_states'], modelCntDic['trans_p'])
        
        return model

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
            if len(none_part):
                parts.append((u'none', none_part))
            # fetch the named part part
            entity_part = rest_sentence[rest_sentence.find(u'>') + 1 : rest_sentence.find(u'<END>')]
            entity_tag = rest_sentence[rest_sentence.find(u':') + 1 : rest_sentence.find(u'>')]
            if len(entity_part):
                parts.append((entity_tag, entity_part))
            rest_sentence = rest_sentence[rest_sentence.find(u'<END>') + 5 : ]
        # the last part
        if len(rest_sentence):
            parts.append((u'none', rest_sentence))
        
        return parts
    
    def transTagSentencesIntoRole(self, tagTrainSentenceList, preWinSize=2, latWinSize=2):
        '''
        '''
        wordSegObj = wordSeg('e', [])
        
        tagMatrix = []
        for sentence in tagTrainSentenceList:
            if type(sentence).__name__ != "unicode":
                sentence = sentence.decode('utf-8')
            if sentence.find(u'<START') != -1:
                sentence_part = self.interceptEntityPart(sentence)
                for i in range(0, len(sentence_part)):
                    if sentence_part[i][0] != u'none':
                        tagVector = []
                        
                        tag = sentence_part[i][0]
                        entity = sentence_part[i][1]
#                         if i - 1 >= 0 or i + 1 <= len(sentence_part) - 1:
                        if i - 1 >= 0:
                            pre = sentence_part[i - 1][1]
                            pre_seg = wordSegObj.singlePosSegEngine(pre)
                            for j in range((len(pre_seg) - preWinSize if len(pre_seg) - preWinSize > 0 else 0), len(pre_seg)):
                                preword = pre_seg[j].split(u'/')[0]
                                preword_POS = pre_seg[j].split(u'/')[1]
                                elementTag = u'_'.join((u'pre', tag, preword_POS))
                                tagVector.append((preword, elementTag))
                                
                        entity_seg = wordSegObj.singlePosSegEngine(entity)
                        for seg in entity_seg:
                            entityword = seg.split(u'/')[0]
                            entityword_POS = seg.split(u'/')[1]
                            elementTag = u'_'.join((u'ent', tag, entityword_POS))
                            tagVector.append((entityword, elementTag)) 
                        
                        if i + 1 <= len(sentence_part) - 1:
                            later = sentence_part[i + 1][1]
                            later_seg = wordSegObj.singlePosSegEngine(later)
                            for j in range(0, (latWinSize if latWinSize < len(later_seg) else len(later_seg))):
                                laterword = later_seg[j].split(u'/')[0]
                                laterword_POS = later_seg[j].split(u'/')[1]
                                elementTag = u'_'.join((u'lat', tag, laterword_POS))
                                tagVector.append((laterword, elementTag))
                        
                        tagMatrix.append(tagVector)
        
        return tagMatrix
    
    def prodSeqModel(self):
        '''
        '''
                
if __name__ == '__main__':  
    nerObj = ner()
    
    s = '习近平总书记表扬小明，小明硕士毕业于<START:pos>中国科学院计算所<END>，后在<START:pos>日本京都大学<END>深造'
    s2 = '<START:pos>肯尼亚政府<END>表示支持<START:pos>中国<END>在<START:pos>南海问题<END>上的立场'
    
#     s = '习近平总书记表扬小明，小明硕士毕业于中国科学院计算所，后在日本京都大学深造'
#     s = s.decode('utf-8')
#     p = s.find('<START')
#     
#     print(type('习近平').__name__)
#     s1 = '习近平'
#     s1 = s1.decode('utf-8')
#     print(type(s1).__name__)
#     print(len('习近平'.decode('utf-8')))
#     print(u's1_len: ' + str(len(s1)))
#     
#     parts = ner().interceptEntityPart(s)
#     for part in parts:
#         print(part[0] + u' ' + part[1])
    
    sentences = []
    sentences.append(s)
    sentences.append(s2)
    
    parts = nerObj.interceptEntityPart(s2.decode('utf-8'))
    for part in parts:
        print(part[0] + u':' + part[1] + u' '),
    print(u'')
    
    tagM = ner().transTagSentencesIntoRole(sentences)
    for vec in tagM:
        for element in vec:
            print(element[0] + u': '),
            print(element[1] + u' '),
        print(u'')
