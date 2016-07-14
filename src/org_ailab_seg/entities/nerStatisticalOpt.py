# -*- coding: UTF-8 -*-

'''
Created on 2016年6月21日

@author: hylovedd
'''
from org_ailab_tools.math.statisticsCountOpt import countElePorbInList

def cptStartP(tagMatrix):
    '''
    '''
    tagList = []
    allList = []
    
    for vec in tagMatrix:
        for ele in vec:
            if ele[1] not in tagList:
                tagList.append(ele[1])
            allList.append(ele[1])
    start_p_vec = countElePorbInList(tagList, allList)
    
    return start_p_vec

def cptEmitP(tagMatrix):
    '''
    '''
    tagList = []
    POSList = []
    allList = []
    for vec in tagMatrix:
        for ele in vec:
            if ele[1] not in tagList:
                tagList.append(ele[1])
            POS = ele[1][ele[1].rfind(u'_') + 1 :]
            if POS not in POSList:
                POSList.append(POS)
            allList.append(ele[1])
    
    emit_p_mat = {}
    for tag in tagList:
        tagPref = tag[:tag.rfind(u'_')]
        occ_POS = []
        for occ_tag in allList:
            if occ_tag.startswith(tagPref):
                occ_POS.append(occ_tag[occ_tag.rfind(u'_') + 1 :])
        emitProbDic = countElePorbInList(POSList, occ_POS)
        emit_p_mat[tag] = emitProbDic
    
    return emit_p_mat

def cptTags_TransP(tagMatrix):
    '''
    '''
    tag2tagTransMat = {}
    for vec in tagMatrix:
        for i in range(len(vec) - 1):
            if vec[i][1] not in tag2tagTransMat.keys():
                tag2tagTransMat[vec[i][1]] = []
            if vec[i + 1][1] not in tag2tagTransMat.keys():
                tag2tagTransMat[vec[i + 1][1]] = []
            tag2tagTransMat[vec[i][1]].append(vec[i + 1][1])
    
    trans_p_mat = {}
    tagList = tag2tagTransMat.keys()
    for tag in tagList:
        transProbDic = countElePorbInList(tagList, tag2tagTransMat[tag])
        trans_p_mat[tag] = transProbDic
    
    return tagList, trans_p_mat

if __name__ == '__main__':
    p = []
    p.append(u'1')
    p.append(u'1')
    print(u'1' not in p)
    
    s = u'pre_pos_ns'
    s_pref = s[:s.rfind(u'_')]
    print(s_pref)
    print(s[s.rfind(u'_') + 1 :])
    print(s.startswith(s_pref))
