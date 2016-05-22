# -*- coding: UTF-8 -*-

'''
Created on 2016年3月23日

@author: hylovedd
'''

from py2neo import Node, Relationship
from py2neo.database import Graph
from py2neo.database.auth import authenticate

_user = "neo4j"
_password = "qdhy199148"

class neoDataGraphOpt:
    def __init__(self, user=_user, password=_password):
        self.user = user;
        self.password = password
        self.graph = self.connectGraph()
                
    '''
    connect to database
    '''
    
    def connectGraph(self):
        # graph = Graph(user = self.user, password = self.password)
        authenticate("localhost:7474", self.user, self.password)
        graph = Graph("http://localhost:7474/db/data/")
        
        return graph
        
    '''
    construct graph
    '''
    
    def createNode(self, nodeType, nodeName):
        return Node(nodeType, name=nodeName)
    
    def createNodeWithProperty(self, nodeType, nodeName, propertyDic):
        '''
        set property with dic
        ''' 
        node = self.createNode(nodeType, nodeName)
        for key in propertyDic:
            node[key] = propertyDic[key]
        
        return node  
             
    def createRelationship(self, relationshipName, node1, node2):
        return Relationship(node1, relationshipName, node2)
    
    def createRelationshipWithProperty(self, relationshipName, node1, node2, propertyDic):
        '''
        ditto
        note: relationship is a kind of subgraph
        ''' 
        relationship = self.createRelationship(relationshipName, node1, node2)
        for key in propertyDic:
            relationship[key] = propertyDic[key]
            
        return relationship
    
    def unionSubGraphs(self, subGraphs):
        if len(subGraphs) <= 1:
            return subGraphs[0]
        unionGraph = subGraphs[0] | subGraphs[1]
        print(u'union subGraphs' + str(subGraphs[0].relationships()))
        print(u'union subGraphs' + str(subGraphs[1].relationships()))
        for i in range(2, len(subGraphs)):  # range is [...)
            unionGraph = (unionGraph | subGraphs[i])
            print(u'union subGraphs' + str(subGraphs[i].relationships()))
            
        return unionGraph
    
    def constructSubGraphInDB(self, subGraph):
        '''
        get a graph's new transactions
        '''
        trs = self.graph.begin()  # autocommit = false
        trs.create(subGraph)
        trs.commit()
        
        # check commit success or not
        print(self.graph.exists(subGraph))
        
    '''
    update or delete elements from graph
    '''
        
    '''
    query records from graph
    '''
    
if __name__ == '__main__':
    
    # all test
    
    neoObj = neoDataGraphOpt()
#     relat = neoObj.combNodeAndRelats("teacher", "huangqingsong", "student", "huyang", "teach")
#     print(relat)
    
    dic1 = {}
    dic1[u'post'] = [u'yuanzhang', u'jaoshou']
    dic1[u'age'] = 56
    node1 = neoObj.createNodeWithProperty("teacher", "huangqingsong", dic1)
    
    dic2 = {}
    dic2[u'hobby'] = [u'coding', u'movie', u'game']
    dic2[u'age'] = 25
    node2 = neoObj.createNodeWithProperty("student", "huyang", dic2)
    
    dic3 = {}
    dic3[u'year'] = [2013, 2014, 2015, 2016]
    dic3[u'subject'] = u'ML'
    relat1 = neoObj.createRelationshipWithProperty("teach", node1, node2, dic3)
    # print(relat1)
    # print(node1[u'post'])
    
    dic4 = {}
    dic4[u'post'] = [u'jiangshi']
    dic4[u'age'] = 37
    node3 = neoObj.createNodeWithProperty("teacher", "liulijun", dic4)
    
    dic5 = {}
    dic5[u'year'] = [2013, 2014, 2015, 2016]
    dic5[u'subject'] = u'health'
    relat2 = neoObj.createRelationshipWithProperty("help", node3, node2, dic5)
    
    relat3 = neoObj.createRelationship('help', node1, node3)
    
    graph = neoObj.unionSubGraphs([relat1, relat2, relat3])
    print(graph.relationships())
    
    # todo: warning don't repeat add relationships, the function is not completed
    neoObj.constructSubGraphInDB(graph)
