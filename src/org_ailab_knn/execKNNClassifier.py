# -*- coding: UTF-8 -*-

import kNN
import matplotlib
import matplotlib.pyplot as plt
from numpy.core.numeric import array

def loadClassifierNum():
    # 生成数据
    group, labels = kNN.createDataSet()
    
    # 打印数据
    print group
    print labels
    
    # 图形化显示数据
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(group[:, 0], group[:, 1])
    plt.show()
    
def loadTextClassifierNum():
    # 加载数据
    datingDataMat, datingLabels = kNN.file2matrix('datingTestSet2.txt')
    
    # 打印数据
    print datingDataMat
    print datingLabels[0:20]
    
    # 图形化显示数据
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(datingDataMat[:, 0], datingDataMat[:, 1], 15.0 * array(datingLabels), 15.0 * array(datingLabels))
    plt.show()
    
def loadClassifierNormNum():
    # 加载数据
    datingDataMat, datingLabels = kNN.file2matrix('datingTestSet2.txt')
    normMat, ranges, minVals = kNN.autoNorm(datingDataMat)
    
    # 打印数据
    print normMat
    print ranges
    print minVals
    
    # 图形化显示数据
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(normMat[:, 0], normMat[:, 1], 15.0 * array(datingLabels), 15.0 * array(datingLabels))
    plt.show()
    
def execClassifier():
    # 执行分类器进行测试
    kNN.datingClassTest()

def test():
    testId = int(raw_input('输入数据：'))
    if testId == 0:
        loadClassifierNum()
    elif testId == 1:
        loadTextClassifierNum()
    elif testId == 2:
        loadClassifierNormNum()
    elif testId == 3:
        execClassifier()
    
if __name__ == '__main__':
    test()
