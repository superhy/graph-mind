# -*- coding: UTF-8 -*-

'''
Created on 2016年11月17日

@author: super
'''
from classifier.networks.layer import NeuralLayerClassifier
from knowledge_graph.medGraphMiningOpt import MedGraphMining
from tools.cache import ROOT_PATH
from knowledge_graph.medLinksPredictOpt import MedLinksPredict


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
    linksPredictObj = MedLinksPredict()
    
    trainLinksFilePath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_train_links1-1000.txt'
    textWordsList, maxTextLength, labelList = linksPredictObj.loadSingleLinksReps(trainLinksFilePath)
    
    for textWords in textWordsList:
        print(' '.join(textWords))
    
    print(len(textWordsList))
    print(maxTextLength)
    print(labelList)

def testClassifyLinks():
    linksPredict =MedLinksPredict()
    gensimModelPath = ROOT_PATH.auto_config_root() + u'model/word2vec/zongheword2vecModel.vector'
#     trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_train_links1-1200.txt'
#     testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_test_links1201-1500.txt'
    '''2'''
    trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/2/shicai2bingzheng_train_links1-300,601-1500.txt'
    testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/2/shicai2bingzheng_test_links301-600.txt'
    
    layerModel = linksPredict.trainHybirdLinksClassifier_file(gensimModelPath, trainLinksDataPath, testLinksDataPath)
    classes, proba = linksPredict.testLayerLinksClasses_file(layerModel, gensimModelPath, trainLinksDataPath, testLinksDataPath)
    
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
    linksPredictObj = MedLinksPredict()
    gensimModelPath = ROOT_PATH.auto_config_root() + u'model/word2vec/zongheword2vecModel.vector'
    trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_train_links1-1200.txt'
    testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_test_links1201-1500.txt'
    
    layerModel = linksPredictObj.trainHybirdLinksClassifier_file(gensimModelPath, trainLinksDataPath, testLinksDataPath,
                                                        testWithLabel=True, v_ratio=0.15)
    score = linksPredictObj.evalLayerLinksClassifier_file(layerModel, gensimModelPath, trainLinksDataPath, testLinksDataPath)
    
    print(score)
    
'''
test save the layer model into file
and load it from file(sometimes need to recompile)
then evaluate the loaded model
'''
     
def testSaveLinksClassifier():
    linksPredictObj = MedLinksPredict()
#     layerObj = NeuralLayerClassifier()
    gensimModelPath = ROOT_PATH.auto_config_root() + u'model/word2vec/zongheword2vecModel.vector'
#     trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_train_links1-1200.txt'
#     testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_test_links1201-1500.txt'
    
    '''1'''
    trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/1/shicai2bingzheng_train_links301-1500.txt'
    testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/1/shicai2bingzheng_test_links1-300.txt'
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
#     trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/5/shicai2bingzheng_train_links1-1200.txt'
#     testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/5/shicai2bingzheng_test_links1201-1500.txt'
    
#     storeFilePath = ROOT_PATH.auto_config_root() + u'model/keras/links(sc2bz)_classifiecr_cnnlstmT'
    storeFilePath = ROOT_PATH.auto_config_root() + u'model/keras/links(sc2bz)_classifiecr_cnnsT' 
    
    '''cnns + lstm part'''
    linksPredictObj.trainHybirdLinksClassifier_file(gensimModelPath,
                                           trainLinksDataPath,
                                           testLinksDataPath,
                                           v_ratio=0.15,
                                           storeFilePath=storeFilePath)
    '''cnns part'''
#     linksPredictObj.trainCNNsLinksClassifier_file(gensimModelPath,
#                                            trainLinksDataPath,
#                                            testLinksDataPath,
#                                            v_ratio=0.15,
#                                            storeFilePath=storeFilePath)
    
def testLoadLinksClassifier():
    linksPredictObj = MedLinksPredict()
    layerObj = NeuralLayerClassifier()
    gensimModelPath = ROOT_PATH.auto_config_root() + u'model/word2vec/zongheword2vecModel.vector'
#     trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_train_links1-1200.txt'
#     testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_test_links1201-1500.txt'

    '''1'''
    trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/1/shicai2bingzheng_train_links301-1500.txt'
    testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/1/shicai2bingzheng_test_links1-300.txt'
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
#     trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/5/shicai2bingzheng_train_links1-1200.txt'
#     testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/cross_test/5/shicai2bingzheng_test_links1201-1500.txt'
    
#     storeFilePath = ROOT_PATH.auto_config_root() + u'model/keras/links(sc2bz)_classifiecr_cnnlstmT'
    storeFilePath = ROOT_PATH.auto_config_root() + u'model/keras/links(sc2bz)_classifiecr_cnnsT' 
    
    layerModel = layerObj.loadStoredModel(storeFilePath, recompile=True)
#     print(layerModel.to_json())
    #===========================================================================
    # classes, proba = linksPredictObj.testLayerLinksClasses_file(layerModel, gensimModelPath, testLinksDataPath)
    # 
    # return classes, proba
    #===========================================================================
    
    score = linksPredictObj.evalLayerLinksClassifier_file(layerModel, gensimModelPath,
                                                      trainLinksDataPath, testLinksDataPath)
    print(score)
    
'''
do some real predict, and write the result into new file
'''
    
def testPredictNewLinks():
    linksPredictObj = MedLinksPredict
    layerObj = NeuralLayerClassifier()
    gensimModelPath = ROOT_PATH.auto_config_root() + u'model/word2vec/zongheword2vecModel.vector'
    trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_train_links1-1200.txt'
    predictLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_predict_links1501-2834.txt'
    
    storeFilePath = ROOT_PATH.auto_config_root() + u'model/keras/links(sc2bz)_classifier_cnnlstm'
    
    layerModel = layerObj.loadStoredModel(storeFilePath, recompile=False)
    classes, proba = linksPredictObj.testLayerLinksClasses_file(layerModel, gensimModelPath,
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
    linksPredictObj = MedLinksPredict()
    layerObj = NeuralLayerClassifier()
    gensimModelPath = ROOT_PATH.auto_config_root() + u'model/word2vec/zongheword2vecModel.vector'
    trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_train_links1-1200.txt'
    testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_test_links1201-1500.txt'
    
    linksDataPathList = [trainLinksDataPath, testLinksDataPath]
    
    totalSequenceList, totalTextList, interBoundary, labelLists = linksPredictObj.loadDetachedLinksReps(linksDataPathList, testWithLabel=True)
    
    nb_words, EMBEDDING_DIM, embedding_matrix = layerObj.prodPreWordEmbedingMat(gensimModelPath, totalSequenceList)
    MAX_SEQUENCE_LENGTH, pad_data = layerObj.prodPadData(totalTextList, nb_words)
    x_train, y_train = layerObj.prodTrainTestData(pad_data, interBoundary, labelLists[0])
    x_test, y_test = layerObj.prodTrainTestData(pad_data, interBoundary - len(totalSequenceList), labelLists[1])
    
    print('x_train:---------------------------')
    print(x_train)
    print('x_test:----------------------------')
    print(x_test)
    
def testSVMLinksTrainTest():
    linksPredictObj = MedLinksPredict()
#     svmObj = SupportVectorMachine()
    trainLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_train_links1-1200.txt'
#     testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_test_links1201-1500.txt'
    testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_train_links1-1200.txt'
    
    estimator = linksPredictObj.trainSVMLinksClassifier_file(trainLinksDataPath, testLinksDataPath)
    accuracy, recall = linksPredictObj.evalEstimatorlinksClasses_file(estimator, trainLinksDataPath, testLinksDataPath)
    
    print('accuracy: ' + str(accuracy))
    print('recall: ' + str(recall))

if __name__ == '__main__':
    
    '''
    test relation classify from shicai to bingzheng
    give the classify result
    '''
    #===========================================================================
    # classes, proba = testClassifyLinks()
    # print('classify res: ' + str(classes))
    # print('num of label 1: ' + str(list(classes).count(1)))
    #===========================================================================
     
    #===========================================================================
    # testLinksDataPath = ROOT_PATH.auto_config_root() + u'model_cache/relation_learning/shicai2bingzheng_test_links1000-1500.txt'
    # printLinksClassifyRes(testLinksDataPath, classes, proba)
    #===========================================================================
    
    '''
    test evaluate the relation classify result from shicai to bingzheng
    '''
#     testEvaluateLinksClassify()
    
    '''
    test save model on disk
    then load it from disk and use it to classify
    '''
#     print ROOT_PATH.auto_config_root()
    testSaveLinksClassifier()
#     classes, proba = testLoadLinksClassifier()
    testLoadLinksClassifier()
    
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
    #===========================================================================
    # testSVMLinksTrainTest()
    #===========================================================================
