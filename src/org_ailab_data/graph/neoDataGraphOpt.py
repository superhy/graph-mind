# -*- coding: UTF-8 -*-

'''
Created on 2016年3月23日

@author: hylovedd
'''

from py2neo import Node, Relationship

neoHost = "http://localhost:7474/db/data/"

class neoGraphOpt:
    def __init__(self):
        self.host = neoHost
        
    def createNode(self, nodeType, nodeName):
        pass
    
    def createRelationship(self, relationship):
        pass
    
    def createNodeAndRelats(self, nodeTyep1, nodeName1, nodeTyep2, nodeName2, relationship):
        node1 = Node(nodeTyep1, name = nodeName1)
        node2 = Node(nodeTyep2, name = nodeName2)
        relat = Relationship(node1, relationship, node2)
        
        return relat

if __name__ == '__main__':
    neoObj = neoGraphOpt()
    print(neoObj.createNodeAndRelats("teacher", "huangqingsong", "student", "huyang", "teach"))