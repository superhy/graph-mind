# -*- coding: UTF-8 -*-

'''
Created on 2016年7月21日

@author: hylovedd
'''

class auxiliaryFunction(object):
    
    def createC1(self, dataSet):
        C1 = []
        for transaction in dataSet:
            for item in transaction:
                if not [item] in C1:
                    C1.append([item])
                    
        C1.sort()
        return map(frozenset, C1)  # use frozen set so we
                                # can use it as a key in a dict    

    def scanD(self, D, Ck, minSupport):
        ssCnt = {}
        for tid in D:
            for can in Ck:
                if can.issubset(tid):
                    if not ssCnt.has_key(can): ssCnt[can] = 1
                    else: ssCnt[can] += 1
        numItems = float(len(D))
        retList = []
        supportData = {}
        for key in ssCnt:
            support = ssCnt[key] / numItems
            if support >= minSupport:
                retList.insert(0, key)
            supportData[key] = support
        return retList, supportData

class aprioriAss(auxiliaryFunction):
    
    def aprioriGen(self, Lk, k):  # creates Ck
        retList = []
        lenLk = len(Lk)
        for i in range(lenLk):
            for j in range(i + 1, lenLk): 
                L1 = list(Lk[i])[:k - 2]; L2 = list(Lk[j])[:k - 2]
                L1.sort(); L2.sort()
                if L1 == L2:  # if first k-2 elements are equal
                    retList.append(Lk[i] | Lk[j])  # set union
        return retList

    def apriori(self, dataSet, minSupport=0.5):
        C1 = super(aprioriAss, self).createC1(dataSet)
        D = map(set, dataSet)
        L1, supportData = super(aprioriAss, self).scanD(D, C1, minSupport)
        L = [L1]
        k = 2
        while (len(L[k - 2]) > 0):
            Ck = self.aprioriGen(L[k - 2], k)
            Lk, supK = super(aprioriAss, self).scanD(D, Ck, minSupport)  # scan DB to get Lk
            supportData.update(supK)
            L.append(Lk)
            k += 1
        return L, supportData
    
    def generateRules(self, L, supportData, minConf=0.7):  # supportData is a dict coming from scanD
        bigRuleList = []
        for i in range(1, len(L)):  # only get the sets with two or more items
            for freqSet in L[i]:
                H1 = [frozenset([item]) for item in freqSet]
                if (i > 1):
                    self.rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
                else:
                    self.calcConf(freqSet, H1, supportData, bigRuleList, minConf)
        return bigRuleList         
    
    def calcConf(self, freqSet, H, supportData, brl, minConf=0.7):
        prunedH = []  # create new list to return
        for conseq in H:
            conf = supportData[freqSet] / supportData[freqSet - conseq]  # calc confidence
            if conf >= minConf: 
                print freqSet - conseq, '-->', conseq, 'conf:', conf
                brl.append((freqSet - conseq, conseq, conf))
                prunedH.append(conseq)
        return prunedH
    
    def rulesFromConseq(self, freqSet, H, supportData, brl, minConf=0.7):
        m = len(H[0])
        if (len(freqSet) > (m + 1)):  # try further merging
            Hmp1 = self.aprioriGen(H, m + 1)  # create Hm+1 new candidates
            Hmp1 = self.calcConf(freqSet, Hmp1, supportData, brl, minConf)
            if (len(Hmp1) > 1):  # need at least two sets to merge
                self.rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)

if __name__ == '__main__':
    pass
