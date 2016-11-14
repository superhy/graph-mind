# -*- coding: UTF-8 -*-

'''
Created on 2016年6月5日

@author: hylovedd
'''

from json.encoder import JSONEncoder
from json.decoder import JSONDecoder


def countElePorbInList(eleList, allList, smooth=1):
    '''
    '''
    eleProbDic = {}
    for ele in eleList:
        eleProbDic[ele] = (allList.count(ele) + 1) * 1.0 / (len(allList) + smooth)
    
    return eleProbDic
if __name__ == '__main__':
    p = [u'1', u'2', u'3', u'4', u'5', u'6', u'1', u'2', u'2', u'3', u'6', u'6', u'6', u'6', u'6', u'6']
    p2 = [u'1', u'2', u'3', u'4', u'5', u'6', u'1', u'2', u'2', u'3', u'6', u'6', u'6', u'6', u'6', u'6', u'1', u'2', u'2', u'3', u'6']
    p3 = []
    for i in range(6):
        p3.append((u'2', u's'))
    print(p3[0][1])
    pp = [u'2', u'6', u'3', u'7']
    
    q1 = {u'key1': None}
    print(None not in q1.values())
    q1[u'key1'] = 1
    print(q1)
    
    print(u'2' in pp)
    print(JSONEncoder().encode(pp))
    
    eleProbDic = countElePorbInList(pp, p)
    eleProbDic2 = countElePorbInList(pp, p2)
#     eleProbDic3 = countElePorbInList(pp, p3)
    
    print('---------------JSON---------------')
    eleProbDicJson = JSONEncoder().encode(eleProbDic)
    print(type(eleProbDicJson))
    print(JSONDecoder().decode(eleProbDicJson))
    print('----------------------------------')
    
#     print(eleProbDic)
    print(eleProbDic2)
#     print(eleProbDic3)
    print(eleProbDic.keys())
