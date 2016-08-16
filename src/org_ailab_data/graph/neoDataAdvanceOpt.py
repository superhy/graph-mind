# -*- coding:utf-8 -*-
'''
Created on 2016年4月10日

@author: hylovedd, jj_ma
'''
from org_ailab_data.graph.neoDataGraphOpt import neoDataGraphOpt

class neoDataAdvanceOpt(neoDataGraphOpt):
    
    def GetConnectBzByName(self, inqLabel, adjLabel, inqNodeName):
        '''
        #输入查询节点的标签和名字，返回向外，向内，全部关联的节点列表
        2016.8.16 adjLabel = 'bz'
        '''
        pro = {}
        pro['name'] = inqNodeName
        outEntities = []
        inEntities = []
        allEntities = []
        
        nodes = super.selectNodeElementsFromDB(labels=[inqLabel], properties=pro)
        outRelation = super.graph.match(nodes[0], None, None, False, None)
        inRelation = super.graph.match(None, None, nodes[0], False, None)
        for rel in outRelation:
            if rel.end_node().has_label(adjLabel):
                outEntities.append(rel.end_node())
        for rel in inRelation:
            if rel.start_node().has_label(adjLabel):
                inEntities.append(rel.start_node())
        allEntities.extend(outEntities)
        allEntities.extend(inEntities)
        allEntities = list(set(allEntities))
        
        return outEntities, inEntities, allEntities
            
    def GetNodeNameByNode(self, nodes):
        nodeNames = []
        nodeNames.extend(node['name'] for node in nodes)
        return nodeNames   

if __name__ == '__main__':
    
    neoObj = neoDataAdvanceOpt('neo4j','qdhy199148')
    
    Out,In,All=neoObj.GetConnectBzByName('bz','伤寒/n')
    print 'out:',Out
    print 'in:',In
    print 'all:',All
    for i in All:
        print neoObj.GetNodeNameByNode(i)
