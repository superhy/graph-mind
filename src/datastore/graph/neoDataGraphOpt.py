# -*- coding:utf-8 -*-
'''
Created on 2016年3月23日
@author: hylovedd

Update on 2016年8月10日
@author: kw_wang, jj_ma
'''

from py2neo import Node, Relationship, NodeSelector, Walkable
from py2neo.database import Graph, cypher
from py2neo.database.auth import authenticate


_user = 'neo4j'
# _password = 'qdhy199148'
_password = 'b3432'
# _service_ip = 'localhost:7474'
_service_ip = '222.201.145.229:7474'

class NeoDataGraphOpt(object):
    def __init__(self, user=_user, password=_password, service_ip = _service_ip):
        self.user = user;
        self.password = password
        self.service_ip = service_ip
        self.graph = self.connectGraph()
        self.selector = NodeSelector(self.graph)
                
    '''
    connect to database
    '''
    
    def connectGraph(self):
        # graph = Graph(user = self.user, password = self.password)
        authenticate(self.service_ip, self.user, self.password)
        graph = Graph('http://%s/db/data/' % self.service_ip)
#         authenticate("localhost:7474", self.user, self.password)
#         graph = Graph("http://localhost:7474/db/data/")
        
        return graph
        
    '''
    construct graph
    '''
    
    '''
    #2016年8月9号修改
    #把创建节点和创建关系给抽象化
    #属性添加用自带的创建函数
    '''
    def createNode(self, nodeType=[], properties={}):
        return Node(*nodeType, **properties)
                 
    def createRelationship(self, relationshipName, node1, node2,propertyDic={}):
        return Relationship(node1, relationshipName, node2,**propertyDic)
    
    
    def unionSubGraphs(self, subGraphs):
        if len(subGraphs) <= 1:
            return subGraphs[0]
        unionGraph = subGraphs[0] | subGraphs[1]
        for i in range(2, len(subGraphs)):  # range is [...)
            unionGraph = (unionGraph | subGraphs[i])
            
        return unionGraph
    
    def constructSubGraphInDB(self, subGraph, primary_label = None, primary_key = []):
        '''
        get a graph's new transactions
        '''
        '''
        #2016年8月3日 16:05:34：修改了创建方式，由merge()函数实现，避免重复创建节点、关系
        #参数说明：subgraph – a Node, Relationship or other Subgraph object
                primary_label – label on which to match any existing nodes
                primary_key – property key(s) on which to match any existing nodes
        #存在疑问：单个节点创建后，会仿照相同类型的结点，建立关系，怎么回事？
        #2016.8.8 修改了参数primary_key，改为列表，以便当作不定参数输入（原函数 merge要求的是不定参数）
        '''
        '''
        trs = self.graph.begin()  # autocommit = false
        trs.create(subGraph)
        trs.commit()
        '''
        self.graph.merge(subGraph, primary_label, *primary_key)
    
    '''
    query records from graph
    ''' 

    def selectNodeElementsFromDB(self, labels = None, condition = [], properties = {}):
        '''
        select elements from graph
        #通过selector查询的暂时只能是结点类型的，关系类型的查询暂时使用match()函数匹配
        #参数说明：labels – node labels to match
                properties – set of property keys and values to match
                                        注：关于labels参数：如果输入的参数元组是空的，默认是查询所有节点
        #返回数据：对查询到的结点数据以列表的形式返回
        ''' 
        nodes = []
        if labels == None:
            selected = self.selector.select()
        else :
            if properties == None:
                selected = self.selector.select(labels)
            else :
                selected = self.selector.select(labels).where(*condition,**properties)
        for node in selected:
            nodes.append(node)
        return nodes   

    
    def selectRelationshipsFromDB(self, start_node = None, rel_type = None, end_node = None, bidirectional = False, limit = None):
        '''
        select relationships from graph
        #函数功能：实现从图数据库中查找与输入参数相对应的关系
        #函数说明：通过调用graph.match()函数来实现关系的查找操作
        #参数说明：start_node – start node of relationships to match (None means any node)
                rel_type – type of relationships to match (None means any type)
                end_node – end node of relationships to match (None means any node)
                bidirectional – True if reversed relationships should also be included
                limit – maximum number of relationships to match (None means unlimited)
        #返回数据：return all relationships with specific criteria
        '''
        relationships = []
        rels = self.graph.match(start_node, rel_type, end_node, bidirectional, limit)
        for rel in rels:
            relationships.append(rel)
        return relationships
    
    def searchInfNode(self,node):
        #返回与节点相关的所有关系，不管方向是向外还是向内
        AllRelation=self.graph.match(node, None, None, True, None)
        #返回指向外面的关系
        outerRelation=self.graph.match(node, None, None, False, None)
        #返回指向里面的关系
        innerRelation=self.graph.match(None, None, node, False, None)
        #对于得到的关系进行操作
        for rel in AllRelation:
            #获得关系的标签
            label=rel.type()
            #获得关系的所有属性，生成字典
            properties=dict(rel)
            #获得属性的数量
            ProNum=len(rel)
        return None
        
    '''
    update or delete elements from graph
    '''
        
    '''
    截至2016年8月4日21:06:25，完成至此
    '''
    def deleteNodeFromDB(self, node):
        '''
        delete node from graph
        #函数功能：实现对单结点node的删除操作
        #函数说明：首先判断该结点存在与否：
                    1、否：直接返回True;
                    2、是：继续下一步判断；
                                        然后再判断与其它结点是否有关系存在：
                    1、否：直接删除该结点；
                    2、是：先删除与其它结点的关系，然后再删除该结点
        #参数说明：node – 待删除的结点
        #返回数据：如果完成删除操作，则返回True,否则返回异常提示
        #2016年8月9号修改
        #原先删除的关系只有指向其他节点的关系，没有删掉指向自己的关系，改为删掉两个方向的关系
        '''
        if self.graph.exists(node):
            innerRelationships = self.selectRelationshipsFromDB(node, None, None, True, None)

            if len(innerRelationships) < 1:
                self.graph.delete(node)
            else:
                for rel in innerRelationships:
                    self.graph.separate(rel)

                self.graph.delete(node)

    def deleteNodesFromDB(self, nodes):
        '''
        delete nodes(tuple、set or frozenset) from graph
        #函数功能：实现对多结点的删除操作
        #函数说明：首先判断传入的结点参数nodes是单个节点还是集合：
                    1、单个结点：直接调用deleteNodeFromDB(self.node);
                    2、集合：依次提取每个结点，并调用deleteNodeFromDB(self.node)。
        #参数说明：nodes - 由执行selectNodesFromDB()函数返回的结果
        #返回结果：无
        '''
        for node in nodes:
            self.deleteNodeFromDB(node)

        
    def deleteRelationshipsFromDB(self, relationships):        
        '''
        select relationships from graph
        #函数功能：实现对结点之间关系的删除操作
        #函数说明：首先判断传入的关系参数relationships是单个关系还是集合：
                    1、单个关系：直接调用graph.separate();
                    2、集合：依次提取每个关系，并调用graph.separate()来完成删除操作。
        #参数说明：relationships – 由执行selectRelaionshipsFromDB()函数返回的结果
        #返回数据：如果完成删除操作，则返回True,否则返回异常提示
        #2016年8月9号修改
        len(relationship)使用错误，返回的不是关系的长度，而是关系里属性的多少
        separate(subgraph)可以接受一个子图最为参数，用for循环反而会报错
        '''
        if self.graph.exists(relationships):       
            self.graph.separate(relationships)               

            
    def updateKeyInNode(self, node, updateProperty = False, properties = {}):
        '''
        #函数功能：实现对结点的一个或多个属性的添加、修改或删除操作
        #函数说明：判断结点是否存在：
                    1、不存在：直接返回None;
                    2、存在：则判断待 添加的属性是否存在于指定的结点node中：
                        1、不存在：则创建属性并赋值；
                        2、存在：根据布尔变量updateProperty的值判断是否要改变原属性值：
                            1)如果为True，则改变原属性值；
                            2)如果为Flase,则不改变原属性值。
                        3、如果待修改的属性值为None，则删除该属性。
        #参数说明：node - 待添加属性的结点
                updateProperty - 如果属性已经存在，指示是否要修改原属性值
                properties - 待添加的属性键值对
        #返回数据：如果完成修改属性操作，则返回True,否则返回异常提示
        '''
        '''
        #2016年8月9日修改
                     修改了把新节点加入数据库的方式,保留关系的信息
        '''
        if self.graph.exists(node): 
            newNode = node     
            for key in properties:
                if newNode[key] == None:
                    newNode[key] = properties[key]
                else :
                    if updateProperty:
                        newNode[key] = properties[key]        
            self.modifyNodeInDB(node, newNode)
            return newNode
        else :
            return None
    
    def updateKeyInRelationship(self, relation, updateProperty = False, relationshipName=None,properties = {}):
        '''
        #函数功能：实现对结点的一个或多个属性的添加、修改或删除操作
        #函数说明：判断结点是否存在：
                    1、不存在：直接返回None;
                    2、存在：则判断待 添加的属性是否存在于指定的结点node中：
                        1、不存在：则创建属性并赋值；
                        2、存在：根据布尔变量updateProperty的值判断是否要改变原属性值：
                            1)如果为True，则改变原属性值；
                            2)如果为Flase,则不改变原属性值。
                        3、如果待修改的属性值为None，则删除该属性。
        #参数说明：node - 待添加属性的结点
                updateProperty - 如果属性已经存在，指示是否要修改原属性值
                properties - 待添加的属性键值对
        #返回数据：如果完成修改属性操作，则返回True,否则返回异常提示
        '''
        '''
        #2016年8月9日修改
        #修改了把新节点加入数据库的方式,保留关系的信息
        #添加了修改关系名字（标签）的功能            
        '''
        if self.graph.exists(relation): 
            newRelation = relation     
            for key in properties:
                if newRelation[key] == None:
                    newRelation[key] = properties[key]
                else :
                    if updateProperty:
                        newRelation[key] = properties[key] 
            if not relationshipName==None:
                if relationshipName==newRelation.type():
                    self.modifyRelationshipInDB(relation, newRelation)
                    return newRelation
                else:
                    newRelation=self.createRelationship(relationshipName,newRelation.start_node(),newRelation.end_node(),dict(newRelation))           
            self.modifyRelationshipInDB(relation, newRelation)
            return newRelation
        else :
            return None
        
    def addLabelsInNode(self, node, *labels):
        '''
        #函数功能：实现对节点node的标签添加功能。
        #函数说明：判断结点是否存在有参数labels中的标签：
                    1、存在：不操作
                    2、不存在：执行添加标签的操作，无异常提示
                                                判断原节点是否在图数据库里：
                    1.存在：把新节点替换原节点加入数据库
                    2.不存在：直接把新节点加入数据库                            
        #参数说明：node - 待添加标签labels的结点
                labels - 待添加的标签列表
        #返回数据：返回添加完标签的新节点
        '''                    
        '''
        #2016年8月9日修改
                    原先的方法错误，不能简单地删除节点，那样把关系也给删了的，丢失了关系的信息
                    改为把与原节点相关的所有关系和节点提取出来，删除旧节点，建立新节点与那些节点的关系
                    构建新子图，在把新子图放进数据库，会自动过滤掉已存在的节点。
        '''
        newNode=node
        for label in labels:
            if not newNode.has_label(label):
                newNode.add_label(label)
        if self.graph.exists(node):
            self.modifyNodeInDB(node, newNode)
        else:
            self.constructSubGraphInDB(newNode)
        return newNode
    
    def deleteLabelsFromNode(self, node, *labels):
        '''
        #函数功能：实现对节点node的标签删除功能。
        #函数说明：判断结点是否存在有参数labels中的标签：
                    1、存在：执行删除标签的操作，无异常提示
                    2、不存在：不操作
                                                判断原节点是否在图数据库里：
                    1.存在：把新节点替换原节点加入数据库
                    2.不存在：直接把新节点加入数据库           
        #参数说明：node - 待删除标签labels的结点
                labels - 待删除的标签列表
        #返回数据：如果操作成功，返回True,否则返回Flase。
        '''
        '''
        #2016年8月9日修改
                    与添加标签一样，修改了把新节点加入数据库的方式
        '''
        newNode=node
        for label in labels:
            if newNode.has_label(label):
                newNode.remove_label(label)
        if self.graph.exists(node):
            self.modifyNodeInDB(node, newNode)
        else:
            self.constructSubGraphInDB(newNode)
        
        return newNode
        
    def testElementsInDB(self,subGraph):
        '''
        For test
        '''
        print 'evaluate'
        
        n = self.graph.evaluate("MATCH (a:teacher) RETURN a")
        print n
        print 'run'
        n = self.graph.run("MATCH (a:teacher) where a.age = {x} RETURN a",x = 37)
        for node in n:
            print node

    
    def modifyNodeInDB(self,oldNode,newNode):
        
        '''
        #2016年8月9日创建
        #函数功能：实现修改后的节点加入数据库的功能。
        #函数说明：在原节点已经存在于数据库的前提下，找到所有与原节点直接相关的节点与关系，构建子图
                                                 利用与原节点相关的关系，建立新节点与 那些节点的关系，用于构建新子图
                                                 把新子图加入数据库，自动过滤掉已经存在的直接相关的节点，这样不会丢失掉与原节点相关的关系数据
        #参数说明：oldNode - 已经存在于数据库的旧节点
                  newNode - 修改后的新节点，准备加入数据库
        #返回数据：无
        '''
        outerRelation=self.graph.match(start_node=oldNode)
        innerRelation=self.graph.match(end_node=oldNode)
        newGraph=oldNode
        for rel in outerRelation:
            newRel=Relationship(oldNode,rel.type(),rel.end_node(),**dict(rel))
            newGraph=newGraph|newRel
            
        for rel in innerRelation:
            newRel=Relationship(rel.start_node(),rel.type(),oldNode,**dict(rel))
            newGraph=newGraph|newRel 
        
        self.deleteNodeFromDB(oldNode)
        self.constructSubGraphInDB(newGraph)
          
        return None  
    
    def modifyRelationshipInDB(self,oldRelationship,newRelationship):
        '''
        #2016年8月9日创建
        #函数功能：实现修改后的关系加入数据库的功能。
        #函数说明：简单地先删旧关系再加新关系
        #参数说明：oldRelationship - 已经存在于数据库的旧关系
                  newRelationship - 修改后的新关系，准备加入数据库
        #返回数据：无
        '''
        if self.graph.exists(oldRelationship):
            self.graph.separate(oldRelationship)
            self.constructSubGraphInDB(newRelationship)
        return None   
    
    def addLink(self,path,startLabelName,endLabelName,relationName):
        relation=[]
        
        f=open(path)
        line=f.readline()
        while line:
            if len(line)>0:
                startNodeName=line[:line.find('-->')]
                endNodeName=line[line.find('-->')+3:line.find("{")]
                pro={}
                s=line[line.find("{")+1:line.find("}")]
                print s
                for i in s.split(','):
                    j=i.split(':')
                    pro[j[0]]=j[1]
                snode=self.createNode([startLabelName], {'name':startNodeName})  
                enode=self.createNode([endLabelName], {'name':endNodeName})
                rel=self.createRelationship(relationName, snode, enode, pro)
                relation.append(rel)
                if len(relation)==100:
                    print relation
                    sub=self.unionSubGraphs(relation)
                    self.constructSubGraphInDB(sub)
                    relation=[]
                line=f.readline()
        f.close()
    
if __name__ == '__main__':
    
 
    #初始化,输入数据库帐号密码
    neoObj = NeoDataGraphOpt("neo4j","qdhy199148")
#     #创建节点,返回节点
#     node1=neoObj.createNode([u"Person"], {u'name':u'Jerr'})
#     #把节点、关系、子图加入数据库，自动过滤掉已存在的，无返回值
#     neoObj.constructSubGraphInDB(node1)
#     
#     #根据标签，条件，属性查找节点，返回节点列表
#     node2=neoObj.selectNodeElementsFromDB('Person',condition=[],properties={u'name':u'Emil'})
#     node3=neoObj.selectNodeElementsFromDB("Person", condition=[], properties={u'name':u'Ian'})
#     
#     #创建关系，指定标签，起始、终止节点，以及属性列表，返回关系
#     rel=neoObj.createRelationship("KNOWS", node1, node2[0], propertyDic={})
#     neoObj.constructSubGraphInDB(rel)
#     
#     #查找起始节点与终止节点之间的关系      
#     print "找到的关系：",neoObj.selectRelationshipsFromDB(node2[0], None, node3[0], True, None)
#     
#     #修改关系属性，返回修改完的关系
#     neoObj.updateKeyInRelationship(rel, True,relationshipName="friend" ,properties={})
#     
#     #修改节点属性，返回修改完的节点
#     neoObj.updateKeyInNode(node1, True, properties={u'name':u'Jrre'})
#     
#     #添加节点标签，返回修改完的节点
#     neoObj.addLabelsInNode(node1,*['star'])
#     
#     #删除关系，无返回
#     #neoObj.deleteRelationshipsFroNeoDataGraphOpt 
#     #删除节点，无返回
#     #neoObj.deleteNodeFromDB(node1)
    #输入文件地址，开始节点名，终止节点名，两者之间的关系名
    neoObj.addLink(u'G:\\Xi\\学习\\大数据饮食推荐\\词典\\shicai2bingzheng_links.txt', '食材','病症','关联')