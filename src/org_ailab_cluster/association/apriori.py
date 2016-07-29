# -*- coding: UTF-8 -*-

'''
Created on 2016年7月21日

@author: hylovedd
'''

class auxiliaryFunction(object):
    '''
    input dataSet looks like {(e1, e2, ..., eN): prob<0~1>, ...}
    '''
    
    def createC1(self, dataSet):
        C1 = []
        for transaction in dataSet.keys():
            for item in transaction:
                if [item] not in C1:
                    C1.append([item])   
        C1.sort()
        
        return map(frozenset, C1)  # use frozen set so we
                                # can use it as a key in a dict    

    def scanD(self, dataSet, Ck, minSupport):
        ssCnt = {}
        probSum = 0.0
        for tid in dataSet.keys():
            prob = dataSet[tid]
            probSum += prob
            for can in Ck:
                if can.issubset(tid):
                    if not ssCnt.has_key(can): 
                        ssCnt[can] = prob
                    else: 
                        ssCnt[can] += prob
        retList = []
        supportData = {}
        for key in ssCnt:
            support = ssCnt[key] / probSum
            if support >= minSupport:
                retList.insert(0, key)
            supportData[key] = support
        
        return retList, supportData

class aprioriAss(auxiliaryFunction):
    def __init__(self, minSupport=0.5, minConf=0.7):
        self._minSupport = minSupport
        self._minConf = minConf
    
    def aprioriGen(self, Lk, k):  # creates Ck
        retList = []
        lenLk = len(Lk)
        for i in range(lenLk):
            for j in range(i + 1, lenLk): 
                L1 = list(Lk[i])[:k - 2]
                L2 = list(Lk[j])[:k - 2]
                L1.sort()
                L2.sort()
                if L1 == L2:  # if first k-2 elements are equal
                    retList.append(Lk[i] | Lk[j])  # set union
        
        return retList

    def aprioriAlg(self, dataSet):
        C1 = super(aprioriAss, self).createC1(dataSet)
        L1, supportData = super(aprioriAss, self).scanD(dataSet, C1, self._minSupport)
        L = [L1]
        k = 2
        while (len(L[k - 2]) > 0):
            Ck = self.aprioriGen(L[k - 2], k)
            Lk, supK = super(aprioriAss, self).scanD(dataSet, Ck, self._minSupport)  # scan DB to get Lk
            supportData.update(supK)
            L.append(Lk)
            k += 1
        L.remove([])
            
        return L, supportData
    
    def generateRules(self, L, supportData):  # supportData is a dict coming from scanD
        bigRuleList = []
        for i in range(1, len(L)):  # only get the sets with two or more items
            for freqSet in L[i]:
                H1 = [frozenset([item]) for item in freqSet]
                if (i > 1):
                    self.rulesFromConseq(freqSet, H1, supportData, bigRuleList)
                else:
                    self.calcConf(freqSet, H1, supportData, bigRuleList)
        
        return bigRuleList         
    
    def calcConf(self, freqSet, H, supportData, brl):
        prunedH = []  # create new list to return
        for conseq in H:
            conf = supportData[freqSet] / supportData[freqSet - conseq]  # calc confidence
            if conf >= self._minConf: 
                print freqSet - conseq, '-->', conseq, 'conf:', conf
                brl.append((freqSet - conseq, conseq, conf))
                prunedH.append(conseq)
        
        return prunedH
    
    def rulesFromConseq(self, freqSet, H, supportData, brl):
        m = len(H[0])
        if (len(freqSet) > (m + 1)):  # try further merging
            Hmp1 = self.aprioriGen(H, m + 1)  # create Hm+1 new candidates
            Hmp1 = self.calcConf(freqSet, Hmp1, supportData, brl)
            if (len(Hmp1) > 1):  # need at least two sets to merge
                self.rulesFromConseq(freqSet, Hmp1, supportData, brl)
                
    def p2pAssFilter(self, bigRuleList):
        p2pRuleList = []
        for relat in bigRuleList:
            if len(relat[0]) == 1 and len(relat[1]) == 1:
                p2pRuleList.append((list(relat[0])[0], list(relat[1])[0], relat[2]))
                
        return p2pRuleList
    
    def findAssFromFreqSet(self, dataSet, p2p = True):
        L, supportData = self.aprioriAlg(dataSet)
        rules = self.generateRules(L, supportData)
        
        if p2p == True:
            return self.p2pAssFilter(rules)
        else:
            return rules

if __name__ == '__main__':
    
    dataSet = {(1, 3, 4): 0.6, (2, 3, 5): 0.7, (1, 2, 3, 5): 0.8, (2, 5): 0.9}
#     for tid in dataSet.keys():
#         print(tid)
    
#     print(map(set, dataSet.keys()))
    
    auxObj = auxiliaryFunction()
    C1 = auxObj.createC1(dataSet)
    print(C1)
    for c in C1:
        print(list(c)[0]),
    print('\n---------------------------------------------------------------------------------------------')
#     L, supportData = aprioriAss(0.7, 0.7).aprioriAlg(dataSet)
    L1, supportData1 = auxObj.scanD(dataSet, C1, 0.5)
    print(L1)
    print(supportData1)
    print('---------------------------------------------------------------------------------------------')
    
    aprioriObj = aprioriAss(minSupport=0.3, minConf=0.7)
    L, supportData = aprioriObj.aprioriAlg(dataSet)
    print(L)
    print(supportData)
    print('---------------------------------------------------------------------------------------------')
    
    rules = aprioriObj.generateRules(L, supportData)
    print(rules)
    print('---------------------------------------------------------------------------------------------')
    
    p2pRules = aprioriObj.findAssFromFreqSet(dataSet)
    for rules in p2pRules:
        print(rules)
    
#     r = ()
#     print(len(r))
#     r = (1,)
#     r += (2,)
#     r += (3,)
#     print(r)
#     print(len(r))