# -*- coding: UTF-8 -*-

'''
Created on 2016年8月18日

@author: hylovedd
'''

import time

from org_ailab_classifier.networks.layerClassifier import NeuralLayerClassifier
from org_ailab_kg.medGraphMiningOpt import MedGraphMining
from org_ailab_seg.word2vec.wordVecOpt import WordVecOpt
from org_ailab_seg.wordSeg import WordSeg
from org_ailab_tools.cache import ROOT_PATH


def testFindRelatBzFromPatient():
    medMiningObj = MedGraphMining()
    
    print('load w2v-model from path: ' + medMiningObj.medW2VModelPath)
    
    ask = '胸闷，气喘，头昏四肢酸，嘴巴没味道，胸口胀气有时还一直打嗝，比以前瞌睡多，肺部没问题，只有点纵膈淋巴结肥大，心率64，去三甲医院看专家科医生说是哮喘，拿了哮喘药也没治到胸口气胀打嗝，还是头昏脚酸的，请问到底是肺部问题还是肠胃，还是心脏的问题？'
    seg_ask = WordSeg('e').singlePosSegEngine(ask)
    
    confBZRes = medMiningObj.findRelatBzFromPatient(seg_ask, 0.135)
    for bz in confBZRes.keys():
        print(bz + ' '),
        print(confBZRes[bz])
        
def compMaxTextLength():
    linksTextFilePath = ROOT_PATH.root_win64 + u'model_cache\\shicai2bingzheng_links.txt'
    file = open(linksTextFilePath)
    max_len = 0
    for line in file.readlines():
        textCnt = line[line.find('{') + 1:line.find('}')]
        wordList = textCnt.split(',')
#         print(len(wordList))
        if len(wordList) > max_len:
            max_len = len(wordList)
    file.close()
          
    print('max_length:'),
    print(max_len)
    
def testLoadLinksReps():
    medMiningObj = MedGraphMining()
    
    trainLinksFilePath = ROOT_PATH.root_win64 + u'model_cache\\relation_learning\\shicai2bingzheng_train_links1-1000.txt'
    textWordsList, maxTextLength, labelList = medMiningObj.loadLinksReps(trainLinksFilePath)
    
    for textWords in textWordsList:
        print(' '.join(textWords))
    
    print(len(textWordsList))
    print(maxTextLength)
    print(labelList)

def testLinksRepsToEmbeddingData():
    medMiningObj = MedGraphMining()
    layerObj = NeuralLayerClassifier()
    
    load_start = time.clock()
    
    trainLinksFilePath = ROOT_PATH.root_win64 + u'model_cache\\relation_learning\\shicai2bingzheng_train_links1-1200.txt'
    textWordsList, maxTextLength, labelList = medMiningObj.loadLinksReps(trainLinksFilePath)
    
    gensimModelPath = ROOT_PATH.root_win64 + u'model\\word2vec\\zongheword2vecModel.vector'
    x_data, y_data = layerObj.preTextEmbeddingProcess(gensimModelPath, textWordsList, maxTextLength, labelList)
    
    load_end = time.clock()
    
    print('load data run time: %f s' % (load_end - load_start))
    print('x_data shape: ', x_data.shape)
    print(x_data)
    print('y_data shape: ', y_data.shape)
    print(y_data)

def testClassifyLinks():
    medMiningObj = MedGraphMining()
    gensimModelPath = ROOT_PATH.root_win64 + u'model\\word2vec\\zongheword2vecModel.vector'
    trainLinksDataPath = ROOT_PATH.root_win64 + u'model_cache\\relation_learning\\shicai2bingzheng_train_links1-1200.txt'
    testLinksDataPath = ROOT_PATH.root_win64 + u'model_cache\\relation_learning\\shicai2bingzheng_test_links1201-1500.txt'
    
    layerModel = medMiningObj.trainLinksClassifier_file(gensimModelPath, trainLinksDataPath)
    classes, proba = medMiningObj.testLinksClasses_file(layerModel, gensimModelPath, testLinksDataPath)
    
#     for i in range(len(classes)):
#         print(str(classes[i]) + ': ' + str(proba[i]))
        
    return classes, proba
        
def printLinksClassifyRes(testLinksDataPath, classes, proba):
    testDataFile = open(testLinksDataPath, 'r')
    links = []
    links.extend(line[:line.find('{')] for line in testDataFile.readlines())
    
    for i in range(min([len(links), len(classes), len(proba)])):
        res = 'induce' + str(classes[i]) if classes[i] == 1 else 'cure' + str(classes[i])
        prob = str(proba[i])
        print(links[i] + '\'s relation is ' + res + ', probability: ' + prob)
        
def testEvaluateLinksClassify():
    medMiningObj = MedGraphMining()
    gensimModelPath = ROOT_PATH.root_win64 + u'model\\word2vec\\zongheword2vecModel.vector'
    trainLinksDataPath = ROOT_PATH.root_win64 + u'model_cache\\relation_learning\\shicai2bingzheng_train_links1-1200.txt'
    testLinksDataPath = ROOT_PATH.root_win64 + u'model_cache\\relation_learning\\shicai2bingzheng_test_links1201-1500.txt'
    
    layerModel = medMiningObj.trainLinksClassifier_file(gensimModelPath, trainLinksDataPath, v_ratio=0.15)
    score = medMiningObj.evaluateLinksClassifier_file(layerModel, gensimModelPath, testLinksDataPath)
    
    print(score)
    
def testSaveLinksClassifier():
    medMiningObj = MedGraphMining()
    layerObj = NeuralLayerClassifier()
    gensimModelPath = ROOT_PATH.root_win64 + u'model\\word2vec\\zongheword2vecModel.vector'
    trainLinksDataPath = ROOT_PATH.root_win64 + u'model_cache\\relation_learning\\shicai2bingzheng_train_links1-1200.txt'
    testLinksDataPath = ROOT_PATH.root_win64 + u'model_cache\\relation_learning\\shicai2bingzheng_test_links1201-1500.txt'
    
    storeFilePath = ROOT_PATH.root_win64 + u'model\\keras\\links(sc2bz)_classifier_cnnlstmT'
    
    medMiningObj.trainLinksClassifier_file(gensimModelPath,
                                           trainLinksDataPath,
                                           v_ratio=0.15,
                                           storeFilePath=storeFilePath)
    
def testLoadLinksClassifier():
    medMiningObj = MedGraphMining()
    layerObj = NeuralLayerClassifier()
    gensimModelPath = ROOT_PATH.root_win64 + u'model\\word2vec\\zongheword2vecModel.vector'
    trainLinksDataPath = ROOT_PATH.root_win64 + u'model_cache\\relation_learning\\shicai2bingzheng_train_links1-1200.txt'
    testLinksDataPath = ROOT_PATH.root_win64 + u'model_cache\\relation_learning\\shicai2bingzheng_test_links1201-1500.txt'
    
    storeFilePath = ROOT_PATH.root_win64 + u'model\\keras\\links(sc2bz)_classifier_cnnlstmE'
    
    layerModel = layerObj.loadStoredModel(storeFilePath, recompile=True)
#     print(layerModel.to_json())
    #===========================================================================
    # classes, proba = medMiningObj.testLinksClasses_file(layerModel, gensimModelPath, testLinksDataPath)
    # 
    # return classes, proba
    #===========================================================================
    
    score = medMiningObj.evaluateLinksClassifier_file(layerModel, gensimModelPath, testLinksDataPath)
    print(score)

if __name__ == '__main__':
    '''
    test find related bingzheng from patient's text
    '''
#     testFindRelatBzFromPatient()
#     compMaxTextLength()
#     testLoadLinksReps()
#     testLinksRepsToEmbeddingData()
    
    # load gensim word vector model from file
#     gensimModelPath = ROOT_PATH.root_win64 + u'model\\word2vec\\zongheword2vecModel.vector'
#     wordVecObj = WordVecOpt(modelPath=gensimModelPath)
#     w2vModel = wordVecObj.loadModelfromFile(gensimModelPath)

    '''
    test relation classify from shicai to bingzheng
    give the classify result
    '''
#     classes, proba = testClassifyLinks()
#     
#     testLinksDataPath = ROOT_PATH.root_win64 + u'model_cache\\relation_learning\\shicai2bingzheng_test_links1000-1500.txt'
#     printLinksClassifyRes(testLinksDataPath, classes, proba)
    
    '''
    test evaluate the relation classify result from shicai to bingzheng
    '''
#     testEvaluateLinksClassify()
    
    '''
    test save model on disk
    then load it from disk and use it to classify
    '''
#     testSaveLinksClassifier()
#     classes, proba = testLoadLinksClassifier()
    testLoadLinksClassifier()
#     testLinksDataPath = ROOT_PATH.root_win64 + u'model_cache\\relation_learning\\shicai2bingzheng_test_links1201-1500.txt'
#     printLinksClassifyRes(testLinksDataPath, classes, proba)    
