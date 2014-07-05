'''
@author: superhy
'''

import kNN

def showClassifierNum():
    group, labels = kNN.createDataSet()
    print group
    print labels

if __name__ == '__main__':
    showClassifierNum()