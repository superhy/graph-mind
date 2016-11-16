# -*- coding: UTF-8 -*-

'''
Created on 2016年11月17日

@author: super
'''
import time

from classifier.liner.svm import SupportVectorMachine
from classifier.networks.layer import NeuralLayerClassifier
from knowledge_graph import medGraphSupOpt
from tools.cache import ROOT_PATH


_medW2VModelPath = ROOT_PATH.auto_config_root() + u'model/word2vec/zongheword2vecModel.vector'
# _scDictPath = ROOT_PATH.seg_dictwin64 + u'jieba_shicai.txt'
# _bzDictPath = ROOT_PATH.seg_dictwin64 + u'jieba_yixuebaike.txt'
_medBZEntities = []
_medSCEntities = []

class MedLinksPredict():
    
    def __init__(self, medW2VModelPath=_medW2VModelPath):
        self.medW2VModelPath = medW2VModelPath
        self.wordVecOptObj, self.model = medGraphSupOpt.loadW2VModelFromDisk(medW2VModelPath)
        
    '''
    Part 1: load data & pre-processing
    '''
        
    def loadSingleLinksReps(self, linksDataPath, loadType='test'):
        '''
        load train or test reps links without weights
        
        loadType is 'test' or 'train'
        return: 
            textWordSequences -list, every element own a list like [word1, word2, ...]
            textList -list, every element with all words in one string(split by space)
            labelList -list, every element is a single number donate the label of each sequence
        '''
        linksFile = open(linksDataPath, 'r')
        
        labelList = []
        linkDataLines = linksFile.readlines()
        textWordSequences = []
        textList = []
        for line in linkDataLines:
            wordReps = line[line.find('{') + 1 : line.find('}')]
            words = []
            words.extend(pair.split(':')[0] for pair in wordReps.split(','))
            # words for embedding matrix loading need decode to utf-8
            textWordSequences.append(word.decode('utf-8') for word in words)
            
            # words for pad sequence need keep unicode string
            textStr = ' '.join(words)
            textList.append(textStr)
            
        if linksFile.name.find('train') != -1 or loadType == 'train':
            for i in range(len(linkDataLines)):
                line = linkDataLines[i]
                label = line[line.find('}') + 1:line.find('}') + 2]
                if(label == '0' or label == '1'):
                    labelList.append(int(label))
                else:
                    labelList.append(0)
                    print('no label:' + (i + 1))
                    
        linksFile.close()
        
        return textWordSequences, textList, labelList
    
    def loadSingleLinksWeightReps(self, linksDataPath, loadType='test'):
        '''
        load train or test reps links with *weights
        
        loadType is 'test' or 'train'
        return: 
            wordWeightSequences -list, every element own a list like [(word1, weight1), (word2, weight2), ...]
            labelList -list, every element is a single number donate the label of each sequence
        '''
        linksFile = open(linksDataPath, 'r')
        
        labelList = []
        linkDataLines = linksFile.readlines()
        wordWeightSequences = []
        for line in linkDataLines:
            wordReps = line[line.find('{') + 1 : line.find('}')]
            words = []
            # words for embedding matrix loading need decode to utf-8
            words.extend((pair.split(':')[0].decode('utf-8'), float(pair.split(':')[1])) for pair in wordReps.split(','))
            wordWeightSequences.append(words)
#             wordWeightSequences.append(word.decode('utf-8') for word in words)
            
        if linksFile.name.find('train') != -1 or loadType == 'train':
            for i in range(len(linkDataLines)):
                line = linkDataLines[i]
                label = line[line.find('}') + 1:line.find('}') + 2]
                if(label == '0' or label == '1'):
                    labelList.append(int(label))
                else:
                    labelList.append(0)
                    print('no label:' + (i + 1))
                    
        linksFile.close()
        
        return wordWeightSequences, labelList
    
    def loadDetachedLinksReps(self, linksDataPathList, testWithLabel=False):
        '''
        load train & test reps links without weights
        
        linkDataPathList has 2 elements: [0, 1]
        1: train data Links path, with labelList
        2: test data links path, without labelList
        
        return: testSequenceList, interBoundary, labelLists(1,2)
        '''
        trainSequenceList, trainTextList, trainLabelList = self.loadSingleLinksReps(linksDataPathList[0], loadType='train')
        testLoadType = 'test' if testWithLabel == False else 'train'
        testSequenceList, testTextList, testLabelList = self.loadSingleLinksReps(linksDataPathList[1], loadType=testLoadType)
        
        totalSequenceList = trainSequenceList + testSequenceList  # totalSequenceList contain train and test text list
        totalTextList = trainTextList + testTextList
        
        interBoundary = len(trainSequenceList)
        labelLists = [trainLabelList, testLabelList]
        
        return totalSequenceList, totalTextList, interBoundary, labelLists
    
    def loadDetachedLinksWeightReps(self, linksDataPathList, testWithLabel=False):
        '''
        load train & test reps links with weights
        
        linkDataPathList has 2 elements: [0, 1]
        1: train data Links path, with labelList
        2: test data links path, without labelList
        
        return: testWeightSequenceList, interBoundary, labelLists(1,2)
        '''
        trainWeightSequenceList, trainLabelList = self.loadSingleLinksWeightReps(linksDataPathList[0], loadType='train')
        testLoadType = 'test' if testWithLabel == False else 'train'
        testWeightSequenceList, testLabelList = self.loadSingleLinksWeightReps(linksDataPathList[1], loadType=testLoadType)
        
        totalWeightSequenceList = trainWeightSequenceList + testWeightSequenceList  # totalWeightSequenceList contain train and test text list
        
        interBoundary = len(trainWeightSequenceList)
        labelLists = [trainLabelList, testLabelList]
        
        return totalWeightSequenceList, interBoundary, labelLists
    
    '''
    Part 2: call the function of supervised predictor
    '''
    
    def trainCNNsLinksClassifier_file(self, gensimModelPath,
                                      trainLinksDataPath,
                                      testLinksDataPath,
                                      testWithLabel=False,
                                      v_ratio=0.15, storeFilePath=None):
        '''
        Only CNNs
        return model is Keras-Neural Networks Layer model
        '''
        
        layerObj = NeuralLayerClassifier()
        
        load_start = time.clock()
        
        linksDataPathList = [trainLinksDataPath, testLinksDataPath]
        totalSequenceList, totalTextList, interBoundary, labelLists = self.loadDetachedLinksReps(linksDataPathList, testWithLabel=testWithLabel)
        
        nb_words, EMBEDDING_DIM, embedding_matrix = layerObj.prodPreWordEmbedingMat(gensimModelPath, totalSequenceList)
        MAX_SEQUENCE_LENGTH, pad_data = layerObj.prodPadData(totalTextList, nb_words)
        x_train, y_train = layerObj.prodTrainTestData(pad_data, interBoundary, labelLists[0])
        
        embeddingParamsDic = {'nb_words':nb_words,
                              'EMBEDDING_DIM':EMBEDDING_DIM,
                              'embedding_matrix':embedding_matrix,
                              'MAX_SEQUENCE_LENGTH':MAX_SEQUENCE_LENGTH}
        
        load_end = time.clock()
        print('load data runtime %f s' % (load_end - load_start))
        
        train_start = time.clock()
        
        model = layerObj.CNNsClassify_Embed(embeddingParamsDic,
                                     x_train, y_train,
                                     validation_split=v_ratio,
                                     auto_stop=False)
        
        train_end = time.clock()
        print('train model runtime %f s' % (train_end - train_start))
        # save the model's framework and data on disk
        if storeFilePath != None:
            layerObj.modelPersistentStorage(model, storeFilePath)
        
        return model
    
    def trainHybirdLinksClassifier_file(self, gensimModelPath,
                                  trainLinksDataPath,
                                  testLinksDataPath,
                                  testWithLabel=False,
                                  v_ratio=0.15, storeFilePath=None):
        '''
        Hybird by CNNs and LSTM
        return model is Keras-Neural Networks Layer model
        '''
        
        layerObj = NeuralLayerClassifier()
        
        load_start = time.clock()
        
        linksDataPathList = [trainLinksDataPath, testLinksDataPath]
        totalSequenceList, totalTextList, interBoundary, labelLists = self.loadDetachedLinksReps(linksDataPathList, testWithLabel=testWithLabel)
        
        nb_words, EMBEDDING_DIM, embedding_matrix = layerObj.prodPreWordEmbedingMat(gensimModelPath, totalSequenceList)
        MAX_SEQUENCE_LENGTH, pad_data = layerObj.prodPadData(totalTextList, nb_words)
        x_train, y_train = layerObj.prodTrainTestData(pad_data, interBoundary, labelLists[0])
        
        embeddingParamsDic = {'nb_words':nb_words,
                              'EMBEDDING_DIM':EMBEDDING_DIM,
                              'embedding_matrix':embedding_matrix,
                              'MAX_SEQUENCE_LENGTH':MAX_SEQUENCE_LENGTH}
        
        load_end = time.clock()
        print('load data runtime %f s' % (load_end - load_start))
        
        train_start = time.clock()
        
        model = layerObj.CNNPoolingLSTMClassify_Embed(embeddingParamsDic,
                                                x_train, y_train,
                                                validation_split=v_ratio,
                                                auto_stop=False)
        
        train_end = time.clock()
        print('train model runtime %f s' % (train_end - train_start))
        # save the model's framework and data on disk
        if storeFilePath != None:
            layerObj.modelPersistentStorage(model, storeFilePath)
        
        return model
    
    def trainSVMLinksClassifier_file(self, trainLinksDataPath,
                                     testLinksDataPath,
                                     testWithLabel=False,
                                     storeFilePath=None):
        '''
        SVM
        return model is sklearn estimator model
        '''
        
        svmObj = SupportVectorMachine()
        
        load_start = time.clock()
        
        linksDataPathList = [trainLinksDataPath, testLinksDataPath]
        totalWeightSequenceList, interBoundary, labelLists = self.loadDetachedLinksWeightReps(linksDataPathList, testWithLabel)
        
        MAX_VEC_LENGTH, pad_data = svmObj.prodWeightsVecPadData(totalWeightSequenceList, MAX_VEC_LENGTH=3000)
        x_train, y_train = svmObj.prodTrainTestData(pad_data, interBoundary, labelLists[0])
        
        load_end = time.clock()
        print('load data runtime %f s' % (load_end - load_start))
        
        train_start = time.clock()
        
        estimator = svmObj.SVCClassify(x_train, y_train)
        
        train_end = time.clock()
        print('train model runtime %f s' % (train_end - train_start))
        
        if storeFilePath != None:
            pass
        
        return estimator
    
    def testLayerLinksClasses_file(self, layerModel,
                              gensimModelPath,
                              trainLinksDataPath,
                              testLinksDataPath,
                              testWithLabel=False):
        '''
        test links' classes by Keras-Neural Networks Layer model
        (input model must be produced by Keras)
        '''
        layerObj = NeuralLayerClassifier()
        
        load_start = time.clock()
        
        linksDataPathList = [trainLinksDataPath, testLinksDataPath]
    
        totalSequenceList, totalTextList, interBoundary, labelLists = self.loadDetachedLinksReps(linksDataPathList, testWithLabel=testWithLabel)
    
        nb_words, EMBEDDING_DIM, embedding_matrix = layerObj.prodPreWordEmbedingMat(gensimModelPath, totalSequenceList)
        MAX_SEQUENCE_LENGTH, pad_data = layerObj.prodPadData(totalTextList, nb_words)
        x_test, y_test = layerObj.prodTrainTestData(pad_data, interBoundary - len(totalSequenceList), labelLists[1])
        
#         print(x_test)
        
        load_end = time.clock()
        print('load data runtime %f s' % (load_end - load_start))
        
        classes, proba = layerObj.layerClassifyPredict(layerModel, x_test)
        print('give the predict result')
        
        return classes, proba
    
    def testEstimatorlinksClasses_file(self, sk_estimator,
                                       trainLinksDataPath,
                                       testLinksDataPath,
                                       testWithLabel=False):
        '''
        '''
        svmObj = SupportVectorMachine()
        
        load_start = time.clock()
        
        linksDataPathList = [trainLinksDataPath, testLinksDataPath]
        totalWeightSequenceList, interBoundary, labelLists = self.loadDetachedLinksWeightReps(linksDataPathList, testWithLabel)
        
        MAX_VEC_LENGTH, pad_data = svmObj.prodWeightsVecPadData(linksDataPathList, MAX_VEC_LENGTH=3000)
        x_test, y_test = svmObj.prodTrainTestData(pad_data, interBoundary - len(totalWeightSequenceList), labelLists[0])
        
        load_end = time.clock()
        print('load data runtime %f s' % (load_end - load_start))
        
        classes, proba = svmObj.svmClassifyPredict(sk_estimator, x_test, withProba=True)
        print('give the predict result')
        
        return classes, proba
    
    def evalLayerLinksClassifier_file(self, layerModel,
                              gensimModelPath,
                              trainLinksDataPath,
                              testLinksDataPath,
                              testWithLabel=True):
        '''
        evaluate Keras-Neural Networks Layer model
        (input model must be produced by Keras)
        '''
        layerObj = NeuralLayerClassifier()
        
        print('loading evaluate data...')
        load_start = time.clock()
        
        linksDataPathList = [trainLinksDataPath, testLinksDataPath]
    
        totalSequenceList, totalTextList, interBoundary, labelLists = self.loadDetachedLinksReps(linksDataPathList, testWithLabel=testWithLabel)
    
        nb_words, EMBEDDING_DIM, embedding_matrix = layerObj.prodPreWordEmbedingMat(gensimModelPath, totalSequenceList)
        MAX_SEQUENCE_LENGTH, pad_data = layerObj.prodPadData(totalTextList, nb_words)
        x_test, y_test = layerObj.prodTrainTestData(pad_data, interBoundary - len(totalSequenceList), labelLists[1])
        
        load_end = time.clock()
        print('load data runtime %f s' % (load_end - load_start))
        
        score = layerObj.layerClassifiyEvaluate(layerModel, x_test, y_test)
        print('give the evaluate result')
        
        return score
    
    def evalEstimatorlinksClasses_file(self, sk_estimator,
                                       trainLinksDataPath,
                                       testLinksDataPath,
                                       testWithLabel=True):
        '''
        '''
        svmObj = SupportVectorMachine()
        
        print('loading evaluate data...')
        load_start = time.clock()
        
        linksDataPathList = [trainLinksDataPath, testLinksDataPath]
        totalWeightSequenceList, interBoundary, labelLists = self.loadDetachedLinksWeightReps(linksDataPathList, testWithLabel)
        
        MAX_VEC_LENGTH, pad_data = svmObj.prodWeightsVecPadData(totalWeightSequenceList, MAX_VEC_LENGTH=3000)
        x_test, y_test = svmObj.prodTrainTestData(pad_data, interBoundary - len(totalWeightSequenceList), labelLists[1])
        
        load_end = time.clock()
        print('load data runtime %f s' % (load_end - load_start))
        
        accuracy, recall = svmObj.svmClassifiyEvaluate(sk_estimator, x_test, y_test)
        print('give the evaluate result')
        
        return accuracy, recall

if __name__ == '__main__':
    pass