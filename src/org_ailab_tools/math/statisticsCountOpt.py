# -*- coding: UTF-8 -*-

'''
Created on 2016年6月5日

@author: hylovedd
'''

def countElePorbInList(eleList, allList):
    '''
    '''
    eleProbDic = {}
    for ele in eleList:
        eleProbDic[ele] = (allList.count(ele) + 1) * 1.0 / (len(allList) + 1)
    
    return eleProbDic
if __name__ == '__main__':
    p = [u'1', u'2', u'3', u'4', u'5', u'6', u'1', u'2', u'2', u'3', u'6', u'6', u'6', u'6', u'6', u'6']
    pp = [u'2', u'6', u'3', u'7']
    eleProbDic = countElePorbInList(pp, p)
    
    print(eleProbDic)
