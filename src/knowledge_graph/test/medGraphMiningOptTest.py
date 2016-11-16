# -*- coding: UTF-8 -*-

'''
Created on 2016年8月18日

@author: hylovedd
'''
'''
test find relate BZ from patient
then find +/- food for patient's
'''

from json.decoder import JSONDecoder
from json.encoder import JSONEncoder
import platform
import time

from classifier.networks.layer import NeuralLayerClassifier
from knowledge_graph.medGraphMiningOpt import MedGraphMining
from tools.cache import ROOT_PATH
from word_seg.word2vec.wordVecOpt import WordVecOpt
from word_seg.wordSeg import WordSeg


def testFindRelatBzFromPatient():
    medMiningObj = MedGraphMining()
    
    print('load w2v-model from path: ' + medMiningObj.medW2VModelPath)
    
    ask = '胸闷，气喘，头昏四肢酸，嘴巴没味道，胸口胀气有时还一直打嗝，比以前瞌睡多，肺部没问题，只有点纵膈淋巴结肥大，心率64，去三甲医院看专家科医生说是哮喘，拿了哮喘药也没治到胸口气胀打嗝，还是头昏脚酸的，请问到底是肺部问题还是肠胃，还是心脏的问题？'
    seg_ask = WordSeg('e').singlePosSegEngine(ask)
    
    confBZRes = medMiningObj.findRelatBzFromPatient(seg_ask, 0.14)
    for bz in confBZRes.keys():
        print(bz + ' '),
        print(confBZRes[bz])
        
    return confBZRes

def loadSCforBZDicIntoFile():
    labeledLinksFilePath = ROOT_PATH.auto_config_root() + u'model_cache/shicai2bingzheng_res_links(all).txt'
    
    trans_start = time.clock()
    
    labeledLinksFile = open(labeledLinksFilePath, 'r')
    lines = labeledLinksFile.readlines()
    
    '''
    linkTupleList looks like this: [(start1, end1, label1),(start2, end2, label2),...]
    '''
    linkTupleList = []
    for line in lines:
        link = line[:line.find('{')]
        start = link.split('-->')[0]
        end = link.split('-->')[1]
        label = line[line.find('}') + 1 :line.find('}') + 2]
        linkTupleList.append((start, end, label))
    
    bzRecForbDics = {}
    for tuple in linkTupleList:
        if tuple[1] not in bzRecForbDics.keys():
            bzRecForbDics[tuple[1]] = {'0':[], '1':[]}
#         print(tuple[2])
        if tuple[2] == '0':
            bzRecForbDics[tuple[1]]['0'].append(tuple[0])
        else:
            bzRecForbDics[tuple[1]]['1'].append(tuple[0])
    
    # trans dic into json code and store it on file
    bzRFDicsJson = JSONEncoder().encode(bzRecForbDics)
    rfCacheFilePath = ROOT_PATH.auto_config_root() + u'model_cache/find_cache/bzRecForbDics.json'
    rfCacheFile = open(rfCacheFilePath, 'w')
    rfCacheFile.write(bzRFDicsJson)
    rfCacheFile.close()
    
    trans_end = time.clock()
    print('trans data into json run time: %f s' % (trans_end - trans_start))
    
def testGetBasicRecForbResFromBZ(bzList):
    '''
    in this function, bzList must be the dic--confBZRes's keys
    '''
    rfCacheFilePath = ROOT_PATH.auto_config_root() + u'model_cache/find_cache/bzRecForbDics.json'
    
    recommend_start = time.clock()
    
    rfCacheFile = open(rfCacheFilePath, 'r')
    line = rfCacheFile.readline()
    bzRecForbDics = JSONDecoder().decode(line)
    rfCacheFile.close()
    
    recSCList = []
    forbSCList = []
    for bz in bzList:
        if bz in bzRecForbDics.keys():
            recSCList.extend(bzRecForbDics[bz]['0'])
            forbSCList.extend(bzRecForbDics[bz]['1'])
    recSCList = list(set(recSCList))  # de-duplication, same below
    forbSCList = list(set(forbSCList))
    
    recommend_end = time.clock()
    print('recommend foods run time: %f s' % (recommend_end - recommend_start))
    
    print('推荐食材（基础）：')
    for sc in recSCList:
        print(sc + ', '),
    print('\n----------------------------------------------------------')
    print('禁忌食材（基础）：')
    for sc in forbSCList:
        print(sc + ', '),
    print('\n----------------------------------------------------------')

if __name__ == '__main__':
    '''
    test find related bingzheng from patient's text
    '''
    #===========================================================================
    # testFindRelatBzFromPatient()
    #===========================================================================
    
#     compMaxTextLength()
#     testLoadLinksReps()
#     testLinksRepsToEmbeddingData()
    
    # load gensim word vector model from file
#     gensimModelPath = ROOT_PATH.auto_config_root() + u'model/word2vec/zongheword2vecModel.vector'
#     wordVecObj = WordVecOpt(modelPath=gensimModelPath)
#     w2vModel = wordVecObj.loadModelfromFile(gensimModelPath)

    '''
    consistent test: find bz from patient firstly
    then find the rec-foods and forb-foods secondly
    
    test 1: test load the sc for bz dic into file
    test 2: test find rec and forb foods by bzResList
    '''
    #===========================================================================
    # loadSCforBZDicIntoFile()
    #===========================================================================
    
    #===========================================================================
    # confBZRes = testFindRelatBzFromPatient()
    # bzList = confBZRes.keys()
    # testGetBasicRecForbResFromBZ(bzList)
    #===========================================================================
    