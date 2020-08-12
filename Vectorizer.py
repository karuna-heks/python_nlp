"""
v0.3.20
Vectorizer - файл, содержащий класс для формирования векторов 
текстов на основе набора токенов и/или локальных и глобального словарей 


#!!! - добавить описание общее
#!!! - добавить описание каждого метода
#!!! - перенести глобальные переменные класса внутрь конструктора
#!!! - удалить ненужные комментарии с описанием
#!!! - удалить ненужные закомментированные print'ы
#!!! - перенести в файл Vectorizer класс Dictionary, т.к. они всё равно 
могут работать только вместе
#!!! - реализовать:
- векторизация на основе метрик:
    - word2vec
    - n-gramms
- формирование матрицы текста с возможностью подачи текста 
по предложениям/по словам/по абзацам
"""

import sys
import numpy as np
from numpy import linalg as la
from navec import Navec


class Vectorizer:
    
    
    _globalDict = None
    _table = None
    _metric = "" # выбор метрики вычисления векторов
    _idfArray = None
    _idfDict = None
    
    def __init__(self, metricType:str="tf"):
        self._metric = metricType
        if self._metric == 'emb' or self._metric == 'embm':
            self._embModel = Navec.load('navec_news_v1_1B_250K_300d_100q.tar')
        
    
    def addGlobDict(self, globalDictionary):
        self._globalDict = globalDictionary
        
    def addIdfDict(self, idfDict):
        self._idfDict = idfDict
        globalDictSize = len(self._globalDict)
        self._idfArray = np.zeros(globalDictSize, float)
        for key, i in zip(self._globalDict.keys(), range(globalDictSize)):
            self._idfArray[i] = self._idfDict[key]
            
    
                 
    
    def getVecFromDict(self, localDict): 
        if (self._globalDict == None):
            sys.exit("Error: Global Dictionary is not initiliazed")
        
        tempArray = []
        for key, val, in self._globalDict.items():
            if localDict.get(key) != None:
                tempArray.append(localDict.get(key))
                # <- в конец массива добавляет элемент, если найден ключ
            else:
                tempArray.append(0)
                # <- если ключ не найден, то добавляет 0       
        
        npArray = np.array(tempArray)
        norm = la.norm(npArray)
        if (norm == 0):
            print("\nWarning: Null vector text")
            return list(npArray/1.)
            sys.exit("Error: Text vector sum is zero")
        npArray = npArray/norm
        # <- переводим массив в numpy массив и нормируем его
        
        if (self._metric == "tfidf"):
            npArray = npArray*self._idfArray
            norm = la.norm(npArray)
            npArray = npArray/norm
        # <- если выбрана метрика tfidf, то домножаем tf на массив с
            #idf параметрами каждого слова и снова нормируем его
        
        return list(npArray)
    # <- метод получает словарь, содержащий все слова определённого текста
    # и сравнивая его содержимое с глобальным словарём, который должен
    # быть добавлен заранее, методом addGlobDict, формирует вектор
    #!!! - необходимо строить вектор на основе метрики tf и/или  tf-idf (дополнить)
    
    
    def numToOutputVec(self, num, size):
        tempVec = []
        tempVec = [0]*size
        tempVec[num] = 1
        return tempVec
        
    
    
    
    
    
    
    
    def _getWordVec(self, word:str):
        """
        Метод получает embedding model и слово. возвращает вектор этого
        слова
        """
        if word in self._embModel:
            return self._embModel[word]
        else:
            return self._embModel['<unk>']

    def _textToVectors(self, tokenizedText):
        """
        Метод получает embedding model и текст, в виде списка слов.
        Возвращает набор векторов текста
        """
        vectors = [self._getWordVec(word) for word in tokenizedText]
        return np.array(vectors)
    
    def _trimAndPadVectors(self, textVectors, embDimension:int, seqLen:int):
        """
        метод преобразует входящую матрицу (набор векторов) во входной вектор, 
        согласно необходимому формату (удаляет лишние строки 
        последовательности и добавляет недостающие)
        """
        output = np.zeros((seqLen, embDimension))
        trimmedVectors = textVectors[:seqLen]
        endOfPaddingIndex = seqLen - trimmedVectors.shape[0]
        output[endOfPaddingIndex:] = trimmedVectors
        return output.reshape((seqLen, embDimension))
    
    def _trimAndPadVectorsMatrix(self, textVectors, embDimension:int, seqLen:int):
        """
        метод преобразует входящую матрицу (набор векторов) в входную матрицу, 
        согласно необходимому формату (удаляет лишние строки 
        последовательности и добавляет недостающие)
        """
        output = np.zeros((seqLen, embDimension))
        trimmedVectors = textVectors[:seqLen]
        endOfPaddingIndex = seqLen - trimmedVectors.shape[0]
        output[endOfPaddingIndex:] = trimmedVectors
        return output.reshape((seqLen, embDimension, 1))
    
    def embPreprocess(self, seqLen:int, tokenizedText):
        """
        метод преобразует список слов в вектор нужного формата
        """
        textVectors = self._textToVectors(tokenizedText)
        if self._metric == 'emb':
            output = self._trimAndPadVectors(textVectors, 
                                             self._embModel.pq.dim, 
                                             seqLen)
        elif self._metric == 'embm':
            output = self._trimAndPadVectorsMatrix(textVectors, 
                                             self._embModel.pq.dim, 
                                             seqLen)
        return output
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    v = Vectorizer()
    d = {'a':32, 'b':43, 'c':33, 'd':44, 'e':55, 'f':66}
    d2 = {'b':91, 'd':95, 'a':93}
    v.addGlobDict(d)
    testArray = v.getArrayFromDict(d2)