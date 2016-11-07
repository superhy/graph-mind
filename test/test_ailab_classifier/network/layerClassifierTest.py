# -*- coding: UTF-8 -*-

'''
Created on 2016年8月26日

@author: hylovedd
'''
import numpy
from org_ailab_classifier.networks.layerClassifier import NeuralLayerClassifier
from org_ailab_tools.cache import ROOT_PATH


def generateTrainMatData(size, length, dim, lab_num):
    data = numpy.random.random((size, length, dim))
    labels = numpy.random.randint(lab_num, size=(size, 1))
    
    return data, labels

def generateTestMatData(size, length, dim):
    data = numpy.random.random((size, length, dim))
    return data

def testCNNPoolingLSTMClassify(x_train, y_train, input_shape, x_test, x_evaluate=None, y_evaluate=None):
    layerObj = NeuralLayerClassifier()
    
    model = layerObj.CNNPoolingLSTMClassify(x_train, y_train, input_shape, x_evaluate, y_evaluate)
    classes, proba = layerObj.layerClassifyPredict(model, x_test)
    
    print(classes)
    print(proba)
    
def testCNNClassify(x_train, y_train, input_shape, x_test, x_evaluate=None, y_evaluate=None):
    layerObj = NeuralLayerClassifier()
    
    model = layerObj.CNNsClassify(x_train, y_train, input_shape, x_evaluate, y_evaluate)
    classes, proba = layerObj.layerClassifyPredict(model, x_test)
    
    print(classes)
    print(proba)
    
def testStorageModel(x_train, y_train, input_shape, x_evaluate=None, y_evaluate=None):
    layerObj = NeuralLayerClassifier()
    
    storeFilePath = ROOT_PATH.root_win64 + u'model\\keras\\testCNNLSTM'
    model = layerObj.CNNPoolingLSTMClassify(x_train, y_train, input_shape, x_evaluate, y_evaluate)
    layerObj.modelPersistentStorage(model, storeFilePath)
    
def testLoadStoredModel(x_test):
    layerObj = NeuralLayerClassifier()
    
    storeFilePath = ROOT_PATH.root_win64 + u'model\\keras\\testCNNLSTM'
    model = layerObj.loadStoredModel(storeFilePath)
    classes, proba = layerObj.layerClassifyPredict(model, x_test)
    
    print(model.to_json())
    
    print(classes)
    print(proba)

if __name__ == '__main__':
    
    x_train, y_train = generateTrainMatData(5000, 20 , 150, 2)
    x_evaluate, y_evaluate = generateTrainMatData(100, 20, 150, 2)
    input_shape = (20, 150)
#     print(x_train)
#     print(y_train)
    
    x_test = generateTestMatData(10, 20, 150)
#     print(x_test)

#     testCNNPoolingLSTMClassify(x_train, y_train, input_shape, x_test, x_evaluate=x_evaluate, y_evaluate=y_evaluate)
#     testCNNPoolingLSTMClassify(x_train, y_train, input_shape, x_test)
#     testCNNClassify(x_train, y_train, input_shape, x_test, x_evaluate=x_evaluate, y_evaluate=y_evaluate)
#     testCNNClassify(x_train, y_train, input_shape, x_test)

    testStorageModel(x_train, y_train, input_shape, x_evaluate, y_evaluate)
    testLoadStoredModel(x_test)