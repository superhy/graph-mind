# -*- coding: UTF-8 -*-

'''
@author: superhy
'''

import numpy
from sklearn import metrics
from sklearn.model_selection._validation import cross_val_predict
from sklearn.svm.classes import SVC


class SupportVectorMachine(object):
    
    def prodWordRepTrainTestData(self):
        '''
        '''
    
    def SVCClassify(self, x_train, y_train):
        '''
        Basic Support Vector Machine Classifier
        '''
        
        # the parameter can be set
        kernel = 'rbf'
        # init classifier and train it
        # 
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
        print('predicted: ' + str(predicted))
        
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
