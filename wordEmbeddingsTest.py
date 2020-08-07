from navec import Navec
from numpy import linalg as ln
import numpy as np
import time
import json
import tensorflow as tf
from tensorflow.keras import layers
import matplotlib.pyplot as plt
from random import random
from slovnet.model.emb import NavecEmbedding
import torch

path = 'navec_news_v1_1B_250K_300d_100q.tar'
navec = Navec.load(path)
# emb = NavecEmbedding(navec)

# print(ln.norm(navec['каспийский'] - navec['море']))
# navec.vocab

# path = 'navec_hudlit_v1_12B_500K_300d_100q.tar'
# navec = Navec.load(path)

# sentences1 = [
#                 [[0.1, 0.3,0.7,0.8,0.9], [0.1, 0.12,0.15,0.21,0.24], 
#                 [0.1, 0.3,0.7,0.8,0.9], [0.1, 0.3,0.7,0.8,0.9],
#                 [0.1, 0.3,0.7,0.8,0.9]],
                
#                 [[0.01, 0.08,0.12,0.13,0.13], [0.58, 0.59,0.63,0.63,0.64], 
#                 [0.1, 0.3,0.7,0.8,0.9], 
#                 [0.2, 0.22,0.23,0.25,0.28]],
                
#                 [[0.32, 0.34,0.35,0.38,0.39], [0.1, 0.12,0.15,0.21,0.24], 
#                 [0.78, 0.79,0.79,0.8,0.82]],
                
#                 [[0.9, 0.7,0.7,0.6,0.4], [0.24, 0.21,0.15,0.12,0.12], 
#                 [0.9, 0.8,0.78,0.76,0.71], [0.5, 0.3,0.25,0.21,0.2],
#                 [0.5, 0.35,0.32,0.31,0.31]],
                
#                 [[0.21, 0.18,0.12,0.11,0.10], [0.58, 0.5,0.43,0.42,0.41], 
#                 [0.7, 0.65,0.62,0.6,0.58], 
#                 [0.3, 0.25,0.23,0.22,0.21]],
                
                
#                 ]

# sentences2 = [[[0.32, 0.34,0.35,0.38,0.39], [0.1, 0.12,0.15,0.21,0.24], 
#                 [0.78, 0.79,0.79,0.8,0.82]],
#               [[0.8, 0.79,0.78,0.76,0.75], [0.65, 0.63,0.6,0.58,0.56], 
#                 [0.78, 0.5,0.48,0.38,0.28]]
#               ]

# answer1 = [
#             [1, 0], [1, 0], 
#             [0, 1], [0, 1]
#             ]

# answer2 = [
#             [1, 0], [0, 1]
#             ]

# navec.vocab['b']
# b = navec.pq.__getitem__(972)
# navec.vocab['<unk>']
# navec.vocab['<pad>']

# def getNum():
#     r = int(random()*4)
#     return np.array(sentences1[r]), np.array(answer1[r])





#%%


xData = [
            ['овощь', "ферма", "корова", "дача"],
            ["поле", "огород", "деревня", "свинья"],
            ["село", "трактор", "картофель", "петух"],
            ["чернозем", "ягода"],
            ["пшеница", "поле", "трава", "мясо", "говядина", "яйца", "сад"],
            ["дача", "огород", "комбайн", "элеватор", "колхоз"],
            ["сад", "фрукты", "жук", "трава", "лук", "укроп", "томат"],
            
            ["город", "фонтан", "парк", "здание"],
            ["администрация", "асфальт", "мост"],
            ["стена", "бордюр", "инфраструктура", "электричка", "троллейбус"],
            ["клуб", "офис", "город", "улица", "район"],
            ["бизнес", "центр", "памятник", "мэр", "проспект"],
            ["центр", "парк", "урбанист"],
            ["площадь", "сквер", "развязка", "перекрёсток"]
    ]

xTestData = [
            ["небоскреб", "машина", "брусчатка", "трасса"],
            ["посев", "ячмень", "кукуруза", "гусь"],
            ["амбар", "загон", "скот", "чеснок"],
            ["район", "вокзал", "сквер", "мост"],
            ["зал", "микрорайон", "губернатор"],
            ['морковь', "саженец", "колхозник", "сарай"]
            
    ]

yTestData = [
            [0, 1],
            [1, 0],
            [1, 0],
            [0, 1],
            [0, 1],
            [1, 0]
            
    ]

yData = [
            [1, 0],
            [1, 0],
            [1, 0],
            [1, 0],
            [1, 0],
            [1, 0],
            [1, 0],
            
            [0, 1],
            [0, 1],
            [0, 1],
            [0, 1],
            [0, 1],
            [0, 1],
            [0, 1]
    ]

#%%

def getWordVec(embModel, word):
    if word in embModel:
        return embModel[word]
    else:
        return embModel['<unk>']

def textToVectors(embModel, tokenizedText):
    vectors = [getWordVec(embModel, word) for word in tokenizedText]
    return np.array(vectors)

def trimAndPadVectors(textVectors, embDimension:int, seqLen:int):
    output = np.zeros((seqLen, embDimension))
    trimmedVectors = textVectors[:seqLen]
    endOfPaddingIndex = seqLen - trimmedVectors.shape[0]
    output[endOfPaddingIndex:] = trimmedVectors
    return output.reshape((1, seqLen, embDimension))

def embPreprocess(embModel, seqLen:int, tokenizedText):
    textVectors = textToVectors(embModel, tokenizedText)
    output = trimAndPadVectors(textVectors, embModel.pq.dim, seqLen)
    return output
    

# text = ['абажур', "журавль", "человек", "артист", "убийца", "кекс"]
# print(textToVectors(navec, text))
# l = trimAndPadVectors(textToVectors(navec, text), 300, 30)
# l3 = l.reshape((1, 300*30))

dim = 300
seq = 30
batch = 1

#%%
model = tf.keras.Sequential()
model.add(layers.Bidirectional(layers.LSTM(300), 
                                input_shape=(seq,dim)))
# model.add(layers.Bidirectional(layers.LSTM(10)))
model.add(layers.Dense(300, 'relu'))
model.add(layers.Dense(2, 'softmax'))
model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop')
model.summary()

#%%
for epoch in range(14):
    
    x = embPreprocess(navec, seq, xData[epoch])
    y = np.array(yData[epoch]).reshape(1,2)

    model.fit(x,y, epochs=1, batch_size=batch, verbose=2)
    
#%%
for i in range(6):
    
    x = embPreprocess(navec, seq, xTestData[i])
    y = np.array(yTestData[i]).reshape(1,2)
    
    yhat = model.predict_classes(x)
    print("Expected: ", y, " Predict: ", yhat)
    
    
    
    
    