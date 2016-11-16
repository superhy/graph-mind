# -*- coding: UTF-8 -*-

'''
Created on 2016年8月16日

@author: hylovedd
'''

import time

from datastore.graph.neoDataAdvanceOpt import NeoDataAdvanceOpt
from datastore.graph.neoDataGraphOpt import NeoDataGraphOpt
from knowledge_graph import medGraphSupOpt
from tools.cache import ROOT_PATH


_medW2VModelPath = ROOT_PATH.auto_config_root() + u'model/word2vec/zongheword2vecModel.vector'
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
