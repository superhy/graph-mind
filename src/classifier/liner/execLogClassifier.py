# -*- coding: UTF-8 -*-

import logRegres
from numpy.core.numeric import array

def gradAscent():
    dataArr, labelMat = logRegres.loadDataSet()
    weights = logRegres.gradAscent(dataArr, labelMat)
    print weights
    
    logRegres.plotBestFit(weights.getA())
    
def stocGradAscent0():
    dataArr, labelMat = logRegres.loadDataSet()
    weights = logRegres.stocGradAscent0(array(dataArr), labelMat);
    print weights
    
    logRegres.plotBestFit(weights);
    
def stocGradAscent1(numIter):
    dataArr, labelMat = logRegres.loadDataSet()
    weights = logRegres.stocGradAscent1(array(dataArr), labelMat, numIter);
    print weights
    
    logRegres.plotBestFit(weights);
    
def test():
    testId = int(raw_input('输入数据：'))
    if testId == 0:
        gradAscent()
    elif testId == 1:
        stocGradAscent0();
    elif testId == 2:
        numIter = int(raw_input('输入参数：'))
        stocGradAscent1(numIter)

if __name__ == '__main__':
    test()