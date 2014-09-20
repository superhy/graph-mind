# -*- coding: UTF-8 -*-

import logRegres

def gradAscent():
    dataArr, labelMat = logRegres.loadDataSet()
    weights = logRegres.gradAscent(dataArr, labelMat)
    print weights
    
    logRegres.plotBestFit(weights.getA())
    
def test():
    testId = int(raw_input('输入数据：'))
    if testId == 0:
        gradAscent()

if __name__ == '__main__':
    test()