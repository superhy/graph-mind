# -*- coding: UTF-8 -*-

'''
Created on 2016年11月8日

@author: superhy
'''

import numpy
from sklearn import metrics
from sklearn.model_selection._validation import cross_val_predict
from sklearn.svm.classes import SVC

from org_ailab_tools.decorator import deprecated


class SupportVectorMachine(object):
    
    
    @deprecated
    def prodWeightsVecPadData(self, wordWeightSeqList, MAX_VEC_LENGTH=3000):
        '''
        @deprecated: 
        '''
        totalWordDic = {}
        for seq in wordWeightSeqList:
            for tup in seq:
                if tup[0] in totalWordDic.keys():
                    totalWordDic[tup[0]] += 1
                else:
                    totalWordDic[tup[0]] = 1
        # sort all words by their weight, use python's function programming
        sortedWordTuplelist = sorted(totalWordDic.iteritems(), key=lambda asd:asd[1])
        # filter the selected word's dic
        selectedWordList = []
        print('words number: ' + str(len(sortedWordTuplelist)))
        for i in range(MAX_VEC_LENGTH):
            selectedWordList.append(sortedWordTuplelist[i][0])
            
        # prod word sequence vectors
        pad_vec_list = []
        for seq in wordWeightSeqList:
            repsVecArray = numpy.zeros(MAX_VEC_LENGTH)
            for tup in seq:
                if tup[0] in selectedWordList:
                    repsVecArray[selectedWordList.index(tup[0])] = tup[1]
                    print(tup[0] + ' '),
            print('')
            pad_vec_list.append(repsVecArray)
        # np array the pad_vec_list
        pad_data = numpy.array(pad_vec_list)
        
        return MAX_VEC_LENGTH, pad_data
    
    def prodTrainTestData(self, pad_data, interBoundary, labelList=[]):
        '''
        prod sequence padding train & test data
        (split pad_data by inter_boundary, so get the single train_data or test_data)
        
        if interBoundary > 0, intercept the first len_boundary elements from
        pad_data as x_data, if interBoundary < 0, intercept the last len_boundary
        elements from pad_data as x_data
        
        interBoundary can not be 0
        '''
        
        x_data = None
        y_data = None
        
        print('total size: ' + str(len(pad_data))),
        
        if interBoundary == 0:
            print('interBoundary can not be zero!')
            return x_data, y_data
        
        if interBoundary > 0:
            x_data = pad_data[:interBoundary]
        elif interBoundary < 0:
            x_data = pad_data[len(pad_data) + interBoundary:]  # add a negative value equaled  subtract
        if len(labelList) != 0:
            y_data = numpy.asarray(labelList)
            
        print('treated size: ' + str(len(x_data)) + '\n#===================================#')
        print(x_data),
        print(list(x_data[500]).count(0.))
        print(y_data)
            
        return x_data, y_data
    
    def SVCClassify(self, x_train, y_train):
        '''
        Basic Support Vector Machine Classifier
        '''
        
        # the parameter can be set
        kernel = 'rbf'
        # init classifier and train it
        # if need the proba-predict result, parameter probability must be =True
        clf = SVC(kernel=kernel, probability=True)
        clf.fit(x_train, y_train)
        
        return clf
    
    def svmClassifyPredict(self, clf,
                           x_test,
                           withProba=False):
        '''
        predict the label of input data by svm classifier 
        '''
        
        classes = None
        proba = None
        
        classes = clf.predict(x_test)
        if withProba == True:
            proba = clf.predict_proba(x_test)
        
        return classes, proba
    
    def svmClassifiyEvaluate(self, clf,
                             x_test, y_test):
        '''
        evaluate the svm classifier by accuracy and recall
        '''
        
        # parameter that average recall score compute method
        average = 'micro'
        
        predicted = cross_val_predict(clf, x_test, y_test)
        print('predicted: ' + str(predicted) + 'num of label0: ' + str(list(predicted).count(0)) + ', num of label1: ' + str(list(predicted).count(1)))
        
        accuracy = metrics.accuracy_score(y_test, predicted)
        recall = metrics.recall_score(y_test, predicted, average=average)
        
        return accuracy, recall
    
    def classifyResEvaluate(self, classes, y_test):
        '''
        evaluate the classify result directly
        '''
        
        # parameter that average recall score compute method
        average = 'micro'
        
        accuracy = metrics.accuracy_score(y_test, classes)
        recall = metrics.recall_score(y_test, classes, average=average)
        
        return accuracy, recall

if __name__ == '__main__':
    x_train = numpy.array([[-1, -1], [-2, -1], [1, 1], [2, 1], [3, 2], [1, -1], [-1, 0], [-1, 1], [1, 3], [2, 2]])
    y_train = numpy.array([0, 0, 1, 1, 1, 0, 0, 0, 1, 1])
    
    x_test = numpy.array([[-2, -1], [-1, -1], [1, -1], [-2, 2], [2, 3], [2, -1], [-1, -2], [1, -2], [3, 3], [3, 2]])
    y_test = numpy.array([0, 0, 1, 0, 1, 1, 0, 1, 1, 1])
    
    svmObj = SupportVectorMachine()
    clf = svmObj.SVCClassify(x_train, y_train)
    print('estimator\'s info: ' + str(clf))
    print('#=============================================================#')
    
    classes, proba = svmObj.svmClassifyPredict(clf, x_test, withProba=True)
    print('classes: ' + str(classes))
    print('proba: ' + str(proba))
    print('')
    res_accuracy, res_recall = svmObj.classifyResEvaluate(classes, y_test)
    print('res_accuracy: ' + str(res_accuracy))
    print('res_recall: ' + str(res_recall))
    print('#=============================================================#')
    
    accuracy, recall = svmObj.svmClassifiyEvaluate(clf, x_test, y_test)
    print('accuracy: ' + str(accuracy))
    print('recall: ' + str(recall))
