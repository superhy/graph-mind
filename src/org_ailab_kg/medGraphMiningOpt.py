# -*- coding: UTF-8 -*-

'''
Created on 2016年8月16日

@author: hylovedd
'''

import time

from org_ailab_classifier.networks.layerClassifier import NeuralLayerClassifier
from org_ailab_data.graph.neoDataAdvanceOpt import NeoDataAdvanceOpt
from org_ailab_data.graph.neoDataGraphOpt import NeoDataGraphOpt
from org_ailab_kg import medGraphSupOpt
from org_ailab_seg.word2vec.wordVecOpt import WordVecOpt
from org_ailab_tools.cache import ROOT_PATH



_medW2VModelPath = ROOT_PATH.root_win64 + u'model\\word2vec\\zongheword2vecModel.vector'
# _scDictPath = ROOT_PATH.seg_dictwin64 + u'jieba_shicai.txt'
# _bzDictPath = ROOT_PATH.seg_dictwin64 + u'jieba_yixuebaike.txt'
_medBZEntities = []
_medSCEntities = []

class MedGraphMining(object):
    
    def __init__(self, medW2VModelPath=_medW2VModelPath):
        self.medW2VModelPath = medW2VModelPath
        self.wordVecOptObj, self.model = medGraphSupOpt.loadW2VModelFromDisk(medW2VModelPath)
    
    def initEntityDict(self):
        
        neoDataGraphObj = NeoDataGraphOpt()
        neoDataAdvanceObj = NeoDataAdvanceOpt()
        
        global _medSCEntities
        global _medBZEntities
        
        if len(_medSCEntities) == 0:
            sc_nodes = neoDataGraphObj.selectNodeElementsFromDB(labels='sc')
            _medSCEntities = neoDataAdvanceObj.getEntityNameByNodes(sc_nodes)
            print('missing SC-entities, load them from neo-database')
        if len(_medBZEntities) == 0:
            bz_nodes = neoDataGraphObj.selectNodeElementsFromDB(labels='bz')
            _medBZEntities = neoDataAdvanceObj.getEntityNameByNodes(bz_nodes)
            print('missing BZ-entities, load them from neo-database')
            
    def findRelatBzFromPatient(self, queryWordList, confThreshold):
        '''
        find the relat bz-entities from the
        patients' descriptions of the disease
        
        queryWordList - query string seg result
        with pos-tags as words
        '''
        self.initEntityDict()
        global _medBZEntities
        print('has initialization entities successfully!')
        neoDataAdvanceObj = NeoDataAdvanceOpt()
        
#         wordVecOptObj = worWordVecOpt
        
        ir_start = time.clock()

        disBZEntities = []
        confBZResDic = {}
        for BZEntity in _medBZEntities:
            if BZEntity not in disBZEntities:
                bzConfValue = 0.0
                
                # TODO 需要考虑对querywords进行关键词提取，只遍历关键词序列
                for queryWord in queryWordList:
                    if queryWord in self.model.vocab:
                        bzConfValue += self.wordVecOptObj.culSimBtwWordVecs(self.model, queryWord, BZEntity)
                bzConfValue /= len(queryWordList)
                
                if bzConfValue < confThreshold:  
                    inRelatBZNodes, outRelatBZNodes, allRelatBZNodes = neoDataAdvanceObj.getConnectNodesByName('bz', 'bz', BZEntity)
                    relatBZEntities = neoDataAdvanceObj.getEntityNameByNodes(allRelatBZNodes)
                    # TODO 考虑将上面的数据库查询历史载入到缓存中，加速
                    disBZEntities.append(BZEntity)
                    for entity in relatBZEntities:
                        if entity not in disBZEntities:
                            disBZEntities.append(entity)
#                             print('discard relatEntity: ' + entity)
                    print(BZEntity + ' and its relatEntities have been discarded!')
                else:
                    confBZResDic[BZEntity] = bzConfValue
                    print('find confidence BZ entity:' + BZEntity)
#             else:
#                 print('***' + BZEntity + ' in disEntities list')
        
        ir_end = time.clock()
        # compute the running time
        print('ir mission run time: %f s' % (ir_end - ir_start))
        
        return confBZResDic
    
    def loadLinksReps(self, linksDataPath, loadType='test'):
        '''
        loadType is 'test' or 'train'
        '''
        linksFile = open(linksDataPath, 'r')
        
        textWordsList = []
        labelList = []
        maxTextLength = 0
        linkDataLines = linksFile.readlines()
        for line in linkDataLines:
            wordReps = line[line.find('{') + 1 : line.find('}')]
            words = []
            words.extend(pair.split(':')[0] for pair in wordReps.split(','))
            textWordsList.append(words)
            
            if maxTextLength < len(words):
                maxTextLength = len(words)
                        
        if linksFile.name.find('train') != -1 or loadType == 'train':
            for i in range(len(linkDataLines)):
                line = linkDataLines[i]
                label = line[line.find('}') + 1:line.find('}') + 2]
                if(label == '0' or label == '1'):
                    labelList.append(int(label))
                else:
                    labelList.append(0)
                    print(i + 1)
                    
        linksFile.close()
        
        return textWordsList, maxTextLength, labelList
    
    def trainLinksClassifier_file(self, gensimModelPath, trainLinksDataPath, validation_ratio=0.15, storeFilePath = None):
        '''
        '''
        layerObj = NeuralLayerClassifier()
        
        load_start = time.clock()
        
        textWordsList, maxTextLength, labelList = self.loadLinksReps(trainLinksDataPath, loadType='train')
        x_train, y_train = layerObj.preTextEmbeddingProcess(gensimModelPath, textWordsList, maxTextLength, labelList)
        input_shape = (x_train.shape[1], x_train.shape[2])
        # split the validation set from x_train
        valid_b = int(len(x_train) * (1 - validation_ratio))
        x_validation = x_train[valid_b:]
        y_validation = y_train[valid_b:]
        x_train = x_train[:valid_b]
        y_train = y_train[:valid_b]
        
        load_end = time.clock()
        print('load data runtime %f s' % (load_end - load_start))
        
        train_start = time.clock()
        
        model = layerObj.CNNPoolingLSTMClassify(x_train, y_train, input_shape, x_test=x_validation, y_test=y_validation)
        
        train_end = time.clock()
        print('train model runtime %f s' % (train_end - train_start))
        # save the model's framework and data on disk
        if storeFilePath != None:
            layerObj.modelPersistentStorage(model, storeFilePath)
        
        return model
    
    def testLinksClasses_file(self, layerModel, gensimModelPath, testLinksDataPath):
        '''
        '''
        layerObj = NeuralLayerClassifier()
        
        load_start = time.clock()
        
        textWordsList, maxTextLength, labelList = self.loadLinksReps(testLinksDataPath, loadType='test')
        x_test, y_test = layerObj.preTextEmbeddingProcess(gensimModelPath, textWordsList, maxTextLength)
#         print(x_test)
        
        load_end = time.clock()
        print('load data runtime %f s' % (load_end - load_start))
        
        classes, proba = layerObj.layerClassifyPredict(layerModel, x_test)
        print('give the predict result')
        
        return classes, proba
    
    def evaluateLinksClassifier_file(self, layerModel, gensimModelPath, testLinksDataPath):
        '''
        '''
        layerObj = NeuralLayerClassifier()
        
        print('loading evaluate data...')
        textWordsList, maxTextLength, labelList = self.loadLinksReps(testLinksDataPath, loadType='train')
        x_test, y_test = layerObj.preTextEmbeddingProcess(gensimModelPath, textWordsList, maxTextLength, labelList=labelList)
        
        score = layerObj.layerClassifiyEvaluate(layerModel, x_test, y_test)
        
        return score

if __name__ == '__main__':
#     testObj = MedGraphMining()
#     wordVecOptObj = testObj.wordVecOptObj
#     model = testObj.model
#     print(wordVecOptObj.modelPath)
#     print(model)

    print(len(_medSCEntities))
    print(len(_medBZEntities))
    
    ask = '胸闷，气喘，头昏四肢酸，嘴巴没味道，胸口胀气有时还一直打嗝，比以前瞌睡多，肺部没问题，只有点纵膈淋巴结肥大，心率64，去三甲医院看专家科医生说是哮喘，拿了哮喘药也没治到胸口气胀打嗝，还是头昏脚酸的，请问到底是肺部问题还是肠胃，还是心脏的问题？'
    
    print(_medW2VModelPath)
    del(_medW2VModelPath)
    _medW2VModelPath = 's'
    print(_medW2VModelPath)
    
    
#     s = '{1234}0'
#     t = s[:s.find('}') + 1]
#     print(t)
#     print(t == '0' or t == '1')

    s = [0, 1, 2, 3, 4]
    print(s[:2])
    print(s[2:])
