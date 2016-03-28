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
_database = "http://localhost:7474/db/data/"

class neoGraphOpt:
    def __init__(self, host=None, http_port=None, bolt_port=None, user=_user, password=_password, datebase=_database):
        self.host = host
        self.http_port = http_port
        self.bolt_port = bolt_port
        self.user = user;
        self.password = password
        self.datebase = datebase
        
    def connectGraph(self):
        #graph = Graph(u'http://neo4j:<qdhy199148>@localhost:7474/db/data/')
        authenticate("localhost:7474", "neo4j", "qdhy199148")
        graph = Graph("http://localhost:7474/db/data/")
        #graph = Graph(user = self.user, password = self.password)
        return graph
        
    def createNode(self, nodeType, nodeName):
        return Node(nodeType, name=nodeName)
    
    def createRelationship(self, relationship, node1, node2):
        return Relationship(node1, relationship, node2)
    
    def createNodeAndRelats(self, nodeTyep1, nodeName1, nodeTyep2, nodeName2, relationship):
        node1 = self.createNode(nodeTyep1, nodeName1)
        node2 = self.createNode(nodeTyep2, nodeName2)
        relat = self.createRelationship(relationship, node1, node2)
        
        return relat

if __name__ == '__main__':
    neoObj = neoGraphOpt()
    print(neoObj.createNodeAndRelats("teacher", "huangqingsong", "student", "huyang", "teach"))
    
    test_graph = neoObj.connectGraph()
    print test_graph
