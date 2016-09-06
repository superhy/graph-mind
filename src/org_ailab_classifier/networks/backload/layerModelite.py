# -*- coding: UTF-8 -*-

'''
Created on 2016年8月1日

@author: hylovedd
'''
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.optimizers import SGD
import numpy

def generateData(size, dim, lab_num):
    data = numpy.random.random((size, dim))
    labels = numpy.random.randint(lab_num, size=(size, 1))
    
    return data, labels

def multilayerPerceptron(data, labels):
    '''
    use for test
    '''
    
    # 初始化层次模型
    model = Sequential()
    
    # 逐步加入各层层次
    model.add(Dense(64, input_dim=20, init='uniform', activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    
    # 编译模型
    model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
    
    # 训练模型
    model.fit(data, labels, nb_epoch=10, batch_size=16)
    
    return model

def predict(model, data):
    # 利用模型进行预测
    classes = model.predict_classes(data, batch_size=16)
    proba = model.predict_proba(data, batch_size=16)
    
    return classes, proba

if __name__ == '__main__':
    data, labels = generateData(500, 20, 2)
    
    print(data)
    
    model = multilayerPerceptron(data, labels)
    
    data_test, labels_test = generateData(10, 20, 2)
    print('test data: '),
    print(data_test)
    print('label: ')
    print(labels_test)
    print('---------------------------------------------------------------------------------------------------')
    classes, proba = predict(model, data_test)
    print('result classes: '),
    print(classes)
    print('result prob: '),
    print(proba)
   