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

class neoGraphDBBean:
    def __init__(self, user=_user, password=_password):
        self.user = user;
        self.password = password
        self.graph = self.connectGraph()
        
    def connectGraph(self):
        # graph = Graph(user = self.user, password = self.password)
        authenticate("localhost:7474", self.user, self.password)
        graph = Graph("http://localhost:7474/db/data/")
        
        return graph
        
    def createNode(self, nodeType, nodeName):
        return Node(nodeType, name=nodeName)
    
    def createNodeWithProperty(self, propertyDic):
        # set property with dic
        pass
    
    def createRelationship(self, relationship, node1, node2):
        return Relationship(node1, relationship, node2)
    
    def createNodeAndRelats(self, nodeTyep1, nodeName1, nodeTyep2, nodeName2, relationship):
        node1 = self.createNode(nodeTyep1, nodeName1)
        node2 = self.createNode(nodeTyep2, nodeName2)
        relat = self.createRelationship(relationship, node1, node2)
        
        return relat
    
    def createRelationShipWithNodes(self, relationship):
        # get a graph's new transactions
        trs = self.graph.begin()  # autocommit = false
        trs.create(relationship)
        trs.commit()
        
        # check commit success or not
        print(self.graph.exists(relationship))

if __name__ == '__main__':
    neoObj = neoGraphDBBean()
    relat = neoObj.createNodeAndRelats("teacher", "huangqingsong", "student", "huyang", "teach")
    print(relat)
    
    # print(neoObj.graph)
    # todo: warning don't repeat add relationships, the function is not completed
    neoObj.createRelationShipWithNodes(relat)
