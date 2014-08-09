# -*- coding: UTF-8 -*-

import bayes
from numpy import *

def loadClassifierNum():
    # 初始化数据
    listOPosts, ListClasses = bayes.loadDataSet()
    myVocabList = bayes.createVocabList(listOPosts)
    print myVocabList
    
    # 查看每个测试集的映射结果
    num = 0
    for postinDoc in listOPosts:
        oPostVec = bayes.setOfWords2Vec(myVocabList, postinDoc)
        print repr(num) + ':' + repr(oPostVec)
        num += 1

def execTrainClassifier():
    listOPosts, listClasses = bayes.loadDataSet();
    myVocabList = bayes.createVocabList(listOPosts)
    
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(bayes.setOfWords2Vec(myVocabList, postinDoc))
    
    p0V, p1V, pAb = bayes.trainNBPre(trainMat, listClasses)
    print pAb
    print p0V
    print p1V
    
def execTrainClassifier0():
    listOPosts, listClasses = bayes.loadDataSet();
    myVocabList = bayes.createVocabList(listOPosts)
    
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(bayes.setOfWords2Vec(myVocabList, postinDoc))
    
    p0V, p1V, pAb = bayes.trainNB0(trainMat, listClasses)
    print pAb
    print p0V
    print p1V

def execTestClassifier():
    bayes.testingNB()
    
def test():
    testId = int(raw_input('输入数据：'))
    if testId == 0:
        loadClassifierNum()
    elif testId == 1:
        execTrainClassifier()
    elif testId == 2:
        execTrainClassifier0()
    elif testId == 3:
        execTestClassifier()

if __name__ == '__main__':
    test()
