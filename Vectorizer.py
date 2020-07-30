"""
v0.3.9
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
    - tf-idf
    - word2vec
    - n-gramms
- формирование матрицы текста с возможностью подачи текста 
по предложениям/по словам/по абзацам
"""

import sys
import numpy as np
from numpy import linalg as la
from utility import Table
from math import log10

class Vectorizer:
    
    
    _globalDict = None
    _table = None
    _corpusSize = 0
    _metric = "" # выбор метрики вычисления векторов
    _idfArray = None
    _tfidfGlobalArray = None
    
    def __init__(self, metricType:str="tf"):
        self.metric = metricType
        
    
    def addGlobDict(self, globalDictionary):
        self._globalDict = globalDictionary
        
    def addIdfDict(self, idfDictionary, corpusSize:int):
        self._table = idfDictionary
        self._corpusSize = corpusSize
        self.idfCalc()
        
    def idfCalc(self):
        if ((len(self._table.getRows()) != 0) and \
            (len(self._table.getColumns()) != 0)):
            for key in self._globalDict.keys():
                idf = log10(self._corpusSize / self._table.getVal(key, "count"))
                # <- вычисление idf, путём деления размера корпуса на
                # количество текстов, в котором встречается слово key
                self._table.setVal(key, "idf", idf)
                # <- добавление результата вычисления в таблицу 
        else:
            sys.exit("Error: Additional Table with IDF not have enough \
                     rows or columns")
        
        
        self._idfArray = np.zeros(len(self._globalDict), float)
        # <- создание пустого массива для значений idf
        for key, i in zip(self._globalDict.keys(), 
                          range(len(self._globalDict))):
            self._idfArray[i] = self._table.getVal(key, "idf")
        # <- добавление idf параметра в массив
        
    def getIdf(self):
        return self._idfArray
                   
    def tfidfGlobalCalc(self):
        self._tfidfGlobalArray = np.zeros(len(self._globalDict), float)
        maxVal = max(self._globalDict.values())
        for key, val, i in zip(self._globalDict.keys(), 
                          self._globalDict.values(),
                          range(len(self._globalDict))):
            self._tfidfGlobalArray[i] = (val / maxVal) * self._idfArray[i]
            
    def getTfidfGlobal(self):
        return self._tfidfGlobalArray
                 
    
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
        npArray = npArray/la.norm(npArray)
        # <- переводим массив в numpy массив и нормируем его
        
        if (self._metric == "tfidf"):
            npArray = npArray*self._idfArray
            npArray = npArray/la.norm(npArray)
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
        
    
    
    
    
if __name__ == '__main__':
    v = Vectorizer()
    d = {'a':32, 'b':43, 'c':33, 'd':44, 'e':55, 'f':66}
    d2 = {'b':91, 'd':95, 'a':93}
    v.addGlobDict(d)
    testArray = v.getArrayFromDict(d2)