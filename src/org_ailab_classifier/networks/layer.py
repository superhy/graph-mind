# -*- coding: UTF-8 -*-

'''
Created on 2016年8月19日

@author: hylovedd
'''
from keras.callbacks import EarlyStopping
from keras.layers.convolutional import Convolution1D, MaxPooling1D
from keras.layers.core import Dropout, Dense, Activation, Flatten
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM, GRU
from keras.models import Sequential, model_from_json
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
import numpy

from org_ailab_seg.word2vec.wordVecOpt import WordVecOpt


class NeuralLayerClassifier(object):
    
    def prodPreWordEmbedingMat(self, gensimModelPath, wordSequencesList):
        '''
        load the pred word embedding matrix
        '''
        
        # load gensim wordvec model
        wordVecObj = WordVecOpt(modelPath=gensimModelPath)
        w2vModel = wordVecObj.loadModelfromFile(gensimModelPath)
        w2vVocab = w2vModel.vocab  # pre-load the vocabulary in w2v-model
        
        # some fixed parameter
        EMBEDDING_DIM = w2vModel.vector_size
        # count all words in word sequence list
        allWords = []
        for sequence in wordSequencesList:
            allWords.extend(sequence)
        allWords = list(set(allWords))
        nb_words = len(allWords)
        print('nb_words: ' + str(nb_words))
        
        embedding_matrix = numpy.zeros((nb_words + 1, EMBEDDING_DIM))
        for i in range(len(allWords)):
            if allWords[i] in w2vVocab:
                embedding_vector = wordVecObj.getWordVec(w2vModel, allWords[i])
                embedding_matrix[i] = embedding_vector
#                 print('scan sequence word: ' + allWords[i]),
#                 print('vector: ' + str(embedding_vector))
            
        return nb_words, EMBEDDING_DIM, embedding_matrix
    
    def prodPadData(self, totalTextList, nb_words):
        '''
        prod word sequence padding data
        
        the order of total word sequence must corresponding to embedding matrix
        (in this function: totalTextList must same as another one in function
        prodPreWordEmbedingMat)
        '''
        
        MAX_NB_WORDS = int(nb_words / 1000) * 1000
        MAX_SEQUENCE_LENGTH = 20
        print('MAX_NB_WORDS: ' + str(MAX_NB_WORDS) + ' MAX_SEQUENCE_LENGTH: ' + str(MAX_SEQUENCE_LENGTH))
        
        # vectorize the text samples into a 2D integer tensor
        tokenizer = Tokenizer(nb_words=MAX_NB_WORDS, lower=False)
#         for text in totalTextList:
#             print(text)
        tokenizer.fit_on_texts(totalTextList)
        totalSequences = tokenizer.texts_to_sequences(totalTextList)
        pad_data = pad_sequences(totalSequences, maxlen=MAX_SEQUENCE_LENGTH)
        
        return MAX_SEQUENCE_LENGTH, pad_data
    
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
            
        print('treated size: ' + str(len(x_data)))
            
        return x_data, y_data
    
    def CNNsClassify(self, embeddingParamsDic,
                    x_train, y_train,
                    validation_split=0.15,
                    auto_stop = False):
        '''
        embeddingParamDic contains {
            nb_words: number of all words in text sequences,
            EMBEDDING_DIM: embedding dim of wordvec model for all texts,
            embedding_matrix: pre-trained wordvec embedding mapping matrix,
            MAX_SEQUENCE_LENGTH: max sequence length of each text line,
                it is also the input_length of Embedding layer}
        '''
        
        # set some fixed parameter in Convolution layer
        nb_filter = 128  # convolution core num       
        filter_length = 3  # convolution core size
        border_mode = 'valid'
        cnn_activation = 'relu'
        subsample_length = 1
        # set some fixed parameter in MaxPooling layer
        pool_length = 2
        # set some fixed parameter in Dense layer
        hidden_dims = 80
        # set some fixed parameter in Dropout layer
        dropout_rate = 0.5
        # set some fixed parameter in Activation layer
        final_activation = 'sigmoid'
        # set some fixed parameter in training
        batch_size = 32
        nb_epoch = 2
        
        #=======================================================================
        # set callbacks function for auto early stopping
        # by monitor the loss or val_loss if not change any more
        #=======================================================================
        callbacks = []
        if auto_stop == True:
            monitor = 'val_loss' if validation_split > 0.0 else 'loss'
            patience = 2
            mode = 'min'
            early_stopping = EarlyStopping(monitor=monitor,
                                           patience=patience,
                                           mode=mode)
            callbacks = [early_stopping]
        
        # produce deep layer model
        model = Sequential()
        model.add(Embedding(embeddingParamsDic['nb_words'] + 1,
                            embeddingParamsDic['EMBEDDING_DIM'],
                            weights=[embeddingParamsDic['embedding_matrix']],
                            input_length=embeddingParamsDic['MAX_SEQUENCE_LENGTH'],
                            trainable=False))
        model.add(Convolution1D(nb_filter=nb_filter,
                                filter_length=filter_length,
                                border_mode=border_mode,
                                activation=cnn_activation,
                                subsample_length=subsample_length))
        if pool_length == None:
            pool_length = model.output_shape[1]
        model.add(MaxPooling1D(pool_length=pool_length))
        
        model.add(Flatten())
        
        model.add(Dense(hidden_dims))
        model.add(Dropout(p=dropout_rate))
        model.add(Activation(activation=cnn_activation))
        
        model.add(Dense(1))
        model.add(Activation(activation=final_activation))
        
        # complie and train the model
#         validation_data = None
#         if x_test is not None and y_test is not None:
#             validation_data = (x_test, y_test)
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.fit(x=x_train, y=y_train,
                  batch_size=batch_size,
                  nb_epoch=nb_epoch,
                  validation_split=validation_split,
                  callbacks=callbacks)
        
        return model
    
    def CNNPoolingLSTMClassify(self, embeddingParamsDic,
                               x_train, y_train,
                               validation_split=0.15,
                               auto_stop=False):
        '''
        embeddingParamDic contains {
            nb_words: number of all words in text sequences,
            EMBEDDING_DIM: embedding dim of wordvec model for all texts,
            embedding_matrix: pre-trained wordvec embedding mapping matrix,
            MAX_SEQUENCE_LENGTH: max sequence length of each text line,
                it is also the input_length of Embedding layer}
        '''
        
        # set some fixed parameter in Convolution layer
        nb_filter = 128  # convolution core num       
        filter_length = 5  # convolution core size
        border_mode = 'valid'
        cnn_activation = 'relu'
        subsample_length = 1
        # set some fixed parameter in MaxPooling layer
        pool_length = 2
        # set some fixed parameter in LSTM layer
        lstm_output_size = 64
        # set some fixed parameter in Dropout layer
        dropout_rate = 0.25
        # set some fixed parameter in Activation layer
        final_activation = 'sigmoid'
        # set some fixed parameter in training
        batch_size = 32
        nb_epoch = 2
        
        #=======================================================================
        # set callbacks function for auto early stopping
        # by monitor the loss or val_loss if not change any more
        #=======================================================================
        callbacks = []
        if auto_stop == True:
            monitor = 'val_loss' if validation_split > 0.0 else 'loss'
            patience = 2
            mode = 'min'
            early_stopping = EarlyStopping(monitor=monitor,
                                           patience=patience,
                                           mode=mode)
            callbacks = [early_stopping]
        
        # produce deep layer model
        model = Sequential()
        # load pre-trained word embeddings into an Embedding layer
        # note that we set trainable = False so as to keep the embeddings fixed
        model.add(Embedding(embeddingParamsDic['nb_words'] + 1,
                            embeddingParamsDic['EMBEDDING_DIM'],
                            weights=[embeddingParamsDic['embedding_matrix']],
                            input_length=embeddingParamsDic['MAX_SEQUENCE_LENGTH'],
                            trainable=False))
        model.add(Convolution1D(nb_filter=nb_filter,
                                filter_length=filter_length,
                                border_mode=border_mode,
                                activation=cnn_activation,
                                subsample_length=subsample_length))
        model.add(MaxPooling1D(pool_length=pool_length))
        
        model.add(LSTM(output_dim=lstm_output_size))
        if dropout_rate > 0:
            model.add(Dropout(p=dropout_rate))
            
        model.add(Dense(1))
        model.add(Activation(activation=final_activation))
        
        # complie and train the model
#         validation_data = None
#         if x_test is not None and y_test is not None:
#             validation_data = (x_test, y_test)
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.fit(x=x_train, y=y_train,
                  batch_size=batch_size,
                  nb_epoch=nb_epoch,
                  validation_split=validation_split,
                  callbacks=callbacks)
        
        return model
    
    def layerClassifyRecompile(self, model):
        '''
        '''
        loss = 'binary_crossentropy'
        optimizer = 'adam' 
        metrics = ['accuracy']
        
        model.compile(loss=loss, optimizer=optimizer, metrics=metrics)
        
        return model
    
    def layerClassifyPredict(self, model, x_test):
        '''
        '''
        batch_size = 32
        
        classes = model.predict_classes(x_test, batch_size=batch_size)
        proba = model.predict_proba(x_test, batch_size=batch_size)
    
        return classes, proba
    
    def layerClassifiyEvaluate(self, model, x_test, y_test):
        '''
        '''
        batch_size = 32
        score = model.evaluate(x_test, y_test, batch_size=batch_size)
#         print('\nmodel score params： ' + str(model.metrics_names))
        
        return score
    
    def modelPersistentStorage(self, model, storeFilePath):
        '''
        use json file to store the model's framework (.json)
        use hdf5 file to store the model's data (.h5)
        storeFilePath must be with .json or nothing(just filename)
        
        when store the .json framework to storeFilePath, also create/store 
        the .h5 file on same path automatically
        .json and .h5 file have same filename
        '''
        storeFileName = storeFilePath
        if storeFilePath.find('.json') != -1:
            storeFileName = storeFilePath[:storeFilePath.find('.json')]
        storeDataPath = storeFileName + '.h5'
        storeFramePath = storeFileName + '.json'
        
        frameFile = open(storeFramePath, 'w')
        json_str = model.to_json()
        frameFile.write(json_str)  # save model's framework file
        frameFile.close()
        model.save_weights(storeDataPath, overwrite=True)  # save model's data file
        
        return storeFramePath, storeDataPath
    
    def loadStoredModel(self, storeFilePath, recompile=False):
        '''
        note same as previous function
        if u just use the model to predict, you need not to recompile the model
        if u want to evaluate the model, u should set the parameter: recompile as True
        '''
        storeFileName = storeFilePath
        if storeFilePath.find('.json') != -1:
            storeFileName = storeFilePath[:storeFilePath.find('.json')]
        storeDataPath = storeFileName + '.h5'
        storeFramePath = storeFileName + '.json'
        
        frameFile = open(storeFramePath, 'r')
#         yaml_str = frameFile.readline()
        json_str = frameFile.readline()
#         print(json_str)
        model = model_from_json(json_str)
        if recompile == True:
            model = self.layerClassifyRecompile(model)  # if need to recompile
#         print(model.to_json())
        model.load_weights(storeDataPath)
        frameFile.close()
        
        return model

if __name__ == '__main__':
    
    p = [[1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5]]
    p_list = []
    for i in range(100):
        p_list.append(numpy.asarray(p, dtype='float32'))
    npx = numpy.asarray(p_list)
    print(type(npx))
    print(len(npx))
    print(len(npx[:80]))
    print(npx)
