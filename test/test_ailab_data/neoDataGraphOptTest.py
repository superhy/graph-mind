# -*- coding: UTF-8 -*-

'''
Created on 2016年8月14日

@author: hylovedd
'''
from org_ailab_data.graph.neoDataGraphOpt import NeoDataGraphOpt
from org_ailab_tools.cache import ROOT_PATH


def testAddLinks():
    neoObj = NeoDataGraphOpt("neo4j","qdhy199148")
    neoObj.addLink(ROOT_PATH.root_win64 + u'model_cache\\shicai2bingzheng_links.txt', '食材名缺失','病症名缺失','sc2bz')

if __name__ == '__main__':
    testAddLinks()