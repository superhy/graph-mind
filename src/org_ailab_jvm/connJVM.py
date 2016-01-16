# -*- coding: UTF-8 -*-

'''
Created on 2016年1月16日

@author: hylovedd
'''
import jpype

class connJVM():
    def __init__(self):
        self.JVMPath = jpype.getDefaultJVMPath()
    
    def testRunJVM(self):
        jpype.startJVM(self.JVMPath)
        javaClass = jpype.JClass('Hello')
        print('javaClass: ' + str(javaClass))
        javaInstance = javaClass()
        print('javaInstance: ' + str(javaInstance))
        javaInstance.printHello()
        jpype.shutdownJVM()
        

if __name__ == '__main__':
    connObj = connJVM()
    connObj.testRunJVM()
    