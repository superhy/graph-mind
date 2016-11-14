# -*- coding:utf-8 -*-
'''
Created on 2016年4月10日

@author: hylovedd, jj_ma
'''
from orgdatastoreaph.neoDataGraphOpt import NeoDataGraphOpt, _user, \
    _password, _service_ip

class NeoDataAdvanceOpt(NeoDataGraphOpt):
    
    global _user
    global _password
    global _service_ip
    
    def __init__(self, user=_user, password=_password, service_ip=_service_ip):
        NeoDataGraphOpt.__init__(self, user, password, service_ip)
    
    def getConnectNodesByName(self, inqLabel, adjLabel, inqNodeName):
        '''
        #输入查询节点的标签和名字，返回向外，向内，全部关联的节点列表
        2016.8.16 inqLabel = 'bz', adjLabel = 'bz'
        '''
        pro = {}
        pro['name'] = inqNodeName
        outEntities = []
        inEntities = []
        allEntities = []
        
        nodes = NeoDataGraphOpt.selectNodeElementsFromDB(self, labels=(inqLabel), properties=pro)
        outRelation = self.graph.match(nodes[0], None, None, False, None)
        inRelation = self.graph.match(None, None, nodes[0], False, None)
#         outRelation = NeoDataGraphOpt.graph.match(nodes[0], None, None, False, None)
#         inRelation = NeoDataGraphOpt.graph.match(None, None, nodes[0], False, None)
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
            
    def getEntityNameByNodes(self, nodes):
        entityNames = []
        entityNames.extend(node['name'] for node in nodes)
        return entityNames   

if __name__ == '__main__':
    
    neoObj = NeoDataAdvanceOpt('neo4j', 'b3432')
    
    Out, In, All = neoObj.getConnectNodesByName('bz', 'bz', '伤寒/n')
    print 'out:', Out
    print 'in:', In
    print 'all:', All
    for bz_name in neoObj.getEntityNameByNodes(All):
        print(bz_name)
