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
        
def compMaxTextLength():
    linksTextFilePath = ROOT_PATH.auto_config_root() + u'model_cache/shicai2bingzheng_links.txt'
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
    
    trainLinksFilePath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_train_links1-1000.txt'
    textWordsList, maxTextLength, labelList = medMiningObj.loadSingleLinksReps(trainLinksFilePath)
    
    for textWords in textWordsList:
        print(' '.join(textWords))
    
    print(len(textWordsList))
    print(maxTextLength)
    print(labelList)

def testClassifyLinks():
    medMiningObj = MedGraphMining()
    gensimModelPath = ROOT_PATH.auto_config_root() + u'model/word2vec/zongheword2vecModel.vector'
    trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_train_links1-1200.txt'
    testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_test_links1201-1500.txt'
    
    layerModel = medMiningObj.trainHybirdLinksClassifier_file(gensimModelPath, trainLinksDataPath, testLinksDataPath)
    classes, proba = medMiningObj.testLayerLinksClasses_file(layerModel, gensimModelPath, trainLinksDataPath, testLinksDataPath)
    
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
    gensimModelPath = ROOT_PATH.auto_config_root() + u'model/word2vec/zongheword2vecModel.vector'
    trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_train_links1-1200.txt'
    testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_test_links1201-1500.txt'
    
    layerModel = medMiningObj.trainHybirdLinksClassifier_file(gensimModelPath, trainLinksDataPath, testLinksDataPath,
                                                        testWithLabel=True, v_ratio=0.15)
    score = medMiningObj.evalLayerLinksClassifier_file(layerModel, gensimModelPath, trainLinksDataPath, testLinksDataPath)
    
    print(score)
    
'''
test save the layer model into file
and load it from file(sometimes need to recompile)
then evaluate the loaded model
'''
     
def testSaveLinksClassifier():
    medMiningObj = MedGraphMining()
#     layerObj = NeuralLayerClassifier()
    gensimModelPath = ROOT_PATH.auto_config_root() + u'model/word2vec/zongheword2vecModel.vector'
#     trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_train_links1-1200.txt'
#     testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_test_links1201-1500.txt'
    
    '''1'''
#     trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/1/shicai2bingzheng_train_links301-1500.txt'
#     testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/1/shicai2bingzheng_test_links1-300.txt'
    '''2'''
#     trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/2/shicai2bingzheng_train_links1-300,601-1500.txt'
#     testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/2/shicai2bingzheng_test_links301-600.txt'
    '''3'''
#     trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/3/shicai2bingzheng_train_links1-600,901-1500.txt'
#     testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/3/shicai2bingzheng_test_links601-900.txt'
    '''4'''
#     trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/4/shicai2bingzheng_train_links1-900,1201-1500.txt'
#     testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/4/shicai2bingzheng_test_links901-1200.txt'
    '''5'''
    trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/5/shicai2bingzheng_train_links1-1200.txt'
    testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/5/shicai2bingzheng_test_links1201-1500.txt'
    
#     storeFilePath = ROOT_PATH.auto_config_root() + u'model/keras/links(sc2bz)_classifiecr_cnnlstmT'
    storeFilePath = ROOT_PATH.auto_config_root() + u'model/keras/links(sc2bz)_classifiecr_cnnsT' 
    
    '''cnns + lstm part'''
#     medMiningObj.trainHybirdLinksClassifier_file(gensimModelPath,
#                                            trainLinksDataPath,
#                                            testLinksDataPath,
#                                            v_ratio=0.15,
#                                            storeFilePath=storeFilePath)
    '''cnns part'''
    medMiningObj.trainCNNsLinksClassifier_file(gensimModelPath,
                                           trainLinksDataPath,
                                           testLinksDataPath,
                                           v_ratio=0.15,
                                           storeFilePath=storeFilePath)
    
def testLoadLinksClassifier():
    medMiningObj = MedGraphMining()
    layerObj = NeuralLayerClassifier()
    gensimModelPath = ROOT_PATH.auto_config_root() + u'model/word2vec/zongheword2vecModel.vector'
#     trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_train_links1-1200.txt'
#     testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_test_links1201-1500.txt'

    '''1'''
#     trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/1/shicai2bingzheng_train_links301-1500.txt'
#     testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/1/shicai2bingzheng_test_links1-300.txt'
    '''2'''
#     trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/2/shicai2bingzheng_train_links1-300,601-1500.txt'
#     testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/2/shicai2bingzheng_test_links301-600.txt'
    '''3'''
#     trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/3/shicai2bingzheng_train_links1-600,901-1500.txt'
#     testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/3/shicai2bingzheng_test_links601-900.txt'
    '''4'''
#     trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/4/shicai2bingzheng_train_links1-900,1201-1500.txt'
#     testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/4/shicai2bingzheng_test_links901-1200.txt'
    '''5'''
    trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/5/shicai2bingzheng_train_links1-1200.txt'
    testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/5/shicai2bingzheng_test_links1201-1500.txt'
    
#     storeFilePath = ROOT_PATH.auto_config_root() + u'model/keras/links(sc2bz)_classifiecr_cnnlstmT'
    storeFilePath = ROOT_PATH.auto_config_root() + u'model/keras/links(sc2bz)_classifiecr_cnnsT' 
    
    layerModel = layerObj.loadStoredModel(storeFilePath, recompile=True)
#     print(layerModel.to_json())
    #===========================================================================
    # classes, proba = medMiningObj.testLayerLinksClasses_file(layerModel, gensimModelPath, testLinksDataPath)
    # 
    # return classes, proba
    #===========================================================================
    
    score = medMiningObj.evalLayerLinksClassifier_file(layerModel, gensimModelPath,
                                                      trainLinksDataPath, testLinksDataPath)
    print(score)
    
'''
do some real predict, and write the result into new file
'''
    
def testPredictNewLinks():
    medMiningObj = MedGraphMining()
    layerObj = NeuralLayerClassifier()
    gensimModelPath = ROOT_PATH.auto_config_root() + u'model/word2vec/zongheword2vecModel.vector'
    trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_train_links1-1200.txt'
    predictLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_predict_links1501-2834.txt'
    
    storeFilePath = ROOT_PATH.auto_config_root() + u'model/keras/links(sc2bz)_classifier_cnnlstm'
    
    layerModel = layerObj.loadStoredModel(storeFilePath, recompile=False)
    classes, proba = medMiningObj.testLayerLinksClasses_file(layerModel, gensimModelPath,
                                                        trainLinksDataPath, predictLinksDataPath,
                                                        testWithLabel=False)
     
    return classes, proba

def writePredictResIntoFile(classes):
    originalDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_predict_links1501-2834.txt'
    predictResFilePath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_res_links1501-2834.txt'
    
    orgFile = open(originalDataPath, 'r')
    lines = orgFile.readlines()
    newLines = ''
    for i in range(len(lines)):
        newLines += (lines[i][:len(lines[i]) - 1] + str(classes[i][0]) + '\n')
    orgFile.close()
    resFile = open(predictResFilePath, 'w')
    resFile.write(newLines)
    resFile.close()
    
#============================================================================================#

def testLoadPreEmbedingMat():
    medMiningObj = MedGraphMining()
    layerObj = NeuralLayerClassifier()
    gensimModelPath = ROOT_PATH.auto_config_root() + u'model/word2vec/zongheword2vecModel.vector'
    trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_train_links1-1200.txt'
    testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_test_links1201-1500.txt'
    
    linksDataPathList = [trainLinksDataPath, testLinksDataPath]
    
    totalSequenceList, totalTextList, interBoundary, labelLists = medMiningObj.loadDetachedLinksReps(linksDataPathList, testWithLabel=True)
    
    nb_words, EMBEDDING_DIM, embedding_matrix = layerObj.prodPreWordEmbedingMat(gensimModelPath, totalSequenceList)
    MAX_SEQUENCE_LENGTH, pad_data = layerObj.prodPadData(totalTextList, nb_words)
    x_train, y_train = layerObj.prodTrainTestData(pad_data, interBoundary, labelLists[0])
    x_test, y_test = layerObj.prodTrainTestData(pad_data, interBoundary - len(totalSequenceList), labelLists[1])
    
    print('x_train:---------------------------')
    print(x_train)
    print('x_test:----------------------------')
    print(x_test)
    
def testSVMLinksTrainTest():
    medMiningObj = MedGraphMining()
#     svmObj = SupportVectorMachine()
    trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_train_links1-1200.txt'
#     testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_test_links1201-1500.txt'
    testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_train_links1-1200.txt'
    
    estimator = medMiningObj.trainSVMLinksClassifier_file(trainLinksDataPath, testLinksDataPath)
    accuracy, recall = medMiningObj.evalEstimatorlinksClasses_file(estimator, trainLinksDataPath, testLinksDataPath)
    
    print('accuracy: ' + str(accuracy))
    print('recall: ' + str(recall))

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

    '''
    test relation classify from shicai to bingzheng
    give the classify result
    '''
#     classes, proba = testClassifyLinks()
#     
#     testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_test_links1000-1500.txt'
#     printLinksClassifyRes(testLinksDataPath, classes, proba)
    
    '''
    test evaluate the relation classify result from shicai to bingzheng
    '''
#     testEvaluateLinksClassify()
    
    '''
    test save model on disk
    then load it from disk and use it to classify
    '''
#===============================================================================
# #     print ROOT_PATH.auto_config_root()
#     testSaveLinksClassifier()
# #     classes, proba = testLoadLinksClassifier()
#     testLoadLinksClassifier()
#===============================================================================
    
#     testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_test_links1201-1500.txt'
#     printLinksClassifyRes(testLinksDataPath, classes, proba)

    '''
    predict new links without labels
    '''
    #===========================================================================
    # classes, proba = testPredictNewLinks()
    # writePredictResIntoFile(classes)
    #===========================================================================
    
    '''
    test load pad words sequences
    load pre-trained word embedding matrix
    '''
    #===========================================================================
    # testLoadPreEmbedingMat()
    #===========================================================================
    
    '''
    test use total data train a svm estimator
    then, evaluate the trained estimator
    '''
    testSVMLinksTrainTest()
    