"""
v0.6.10
Dictionary - файл, содержащий класс для работы со словарем/словарями 
корпуса текстов

#!!! - добавить описание общее
#!!! - перенести глобальные переменные класса внутрь конструктора
#!!! - перенести класс Dictionary в файл Vectorizer, т.к. они всё равно должны
работать только вместе
#!!! - добавить для каждого слова подсчёт числа документов, в которые 
оно входит
#!!! - добавить описание каждого метода
#!!! - удалить ненужные комментарии с описанием
#!!! - реализовать недостающие методы
#!!! - реализовать метод report() с выводом полного текстового отчета
"""
from utility import Table
from math import log10
import sys
import numpy as np

class Dictionary:
    
    _globalDict = None # глобальный словарь
    _last = None # последний локальный словарь
    _t = None # таблица для хранения дополнительных параметров слов
    _corpusSize = 0 
    _metric = ""
    _idfArray = None
    _tfidfGlobalArray = None
    _tfidfGlobalDict = None
    
    _wordsList = None # список всех слов в тексте
    
    def __init__(self, metricType:str="tf"):
        self._globalDict = {}
        self._last = {}
        self._metric = metricType
        self._t = Table(["count", "idf", "tfidf"])
    
    
    def addData(self, text):
        self._last.clear()
        self._wordsList = text.split(" ")
        for word in self._wordsList:
            if self._last.get(word) == None:
                self._last[word] = 1
            else: 
                self._last[word] = self._last[word] + 1
        if len(self._last) < 1:
            sys.exit("Error: Local dictionary size is zero")
            
        self._addToGlobal(self._last)
        # метод получает текст, получает из него 
        # локальный словарь, затем дополняет им глобальный 
        # словарь
    
    def getGlobalDictionary(self):
        # метод возвращает глобальный словарь
        return self._globalDict
    
    def getLastDictionary(self):
        # метод возвращает последний локальный словарь
        return self._last
    
    def getGlobalSize(self):
        return len(self._globalDict)
    
    def getLastSize(self):
        return len(self._last)
    
    def getAdditionalTable(self):
        #!!! реализовать более красивый способ передачи данных из таблицы,
        # а не просто возврат всей таблицы
        return self._t
    
        
    def setCorpusSize(self, val:int):
        self._corpusSize = val
        
    def getCorpusSize(self):
        return self._corpusSize
    
    # @private methods
    def _addToGlobal(self, last):
        for key, val in last.items():
            if self._globalDict.get(key) == None:
                self._globalDict[key] = val
                self._t.setVal(key, "count", 1)
            else:
                self._globalDict[key] = self._globalDict[key] + val
                self._t.setVal(key, "count", self._t.getVal(key, "count") + 1)
        self._corpusSize += 1 # подсчёт числа текстов пройденных


    
    def idfGlobalCalc(self):
        if ((len(self._t.getRows()) != 0) and \
            (len(self._t.getColumns()) != 0)):
            for key in self._globalDict.keys():
                idf = log10(self._corpusSize / self._t.getVal(key, "count"))
                # <- вычисление idf, путём деления размера корпуса на
                # количество текстов, в котором встречается слово key
                self._t.setVal(key, "idf", idf)
                # <- добавление результата вычисления в таблицу 
        else:
            sys.exit("Error: Additional Table with IDF not have enough \
                     rows or columns")
        
        
        self._idfArray = np.zeros(len(self._globalDict), float)
        # <- создание пустого массива для значений idf
        for key, i in zip(self._globalDict.keys(), 
                          range(len(self._globalDict))):
            self._idfArray[i] = self._t.getVal(key, "idf")
        # <- добавление idf параметра в массив
        self._tfidfGlobalCalc()
            
    def getIdfGlobal(self):
        return self._idfArray
                   
    def _tfidfGlobalCalc(self):
        self._tfidfGlobalArray = np.zeros(len(self._globalDict), float)
        maxVal = max(self._globalDict.values())
        for key, val, i in zip(self._globalDict.keys(), 
                          self._globalDict.values(),
                          range(len(self._globalDict))):
            tfidfValue = (val / maxVal) * self._idfArray[i]
            self._tfidfGlobalArray[i] = tfidfValue
            self._t.setVal(key, "tfidf", tfidfValue)
            
    def getTfidfGlobal(self):
        return self._tfidfGlobalArray
    
    def getTfidfDict(self):
        if (self._featureIsReducing):
            return self._tfidfGlobalDict
        else:
            sys.exit("Error: tfitfGlobalDict does not exist")
    
    
    def reduceFeatures(self, maxFeatures:int):
        """
        условный оператор. если тф, то удаляем по кол-ву слов, иначе
        по параметру тфидф
        копируем словарь
        
            сортировка словаря по возрастанию
            проходим по таблице итератором и удаляем первые 
            (dictSize - maxFeatures) слов  
            
            проходим по всему словарю и заменяем все значения по ключам
            на значения тфидф из таблицы
            сводим задачу к предыдущей
            создаем идф словарь 
            
        удаляем все лишние вещи
        """
        copyOfDict = dict(self._globalDict)
        
        if self._metric == "tf":
            self._deleteFeaturesFromDictionary(self._globalDict, 
                                               copyOfDict, maxFeatures)
        elif self._metric == "tfidf":
            for key in self._globalDict.keys():
                copyOfDict[key] = self._t.getVal(key, "tfidf")
            # <- заполнение нового словаря значениями tfidf из таблицы _t
            self._deleteFeaturesFromDictionary(self._globalDict, 
                                               copyOfDict, maxFeatures)
            # <- удаление лишних свойств из глобального словаря
            copyOfDict = dict(self._globalDict)
            for key in self._globalDict.keys():
                copyOfDict[key] = self._t.getVal(key, "tfidf")
            self._tfidfGlobalDict = copyOfDict
            # <- создание нового, сокращенного словаря и заполнение 
                # его значениями tfidf из таблицы _t
        self.idfGlobalCalc()
        self._featureIsReducing = True
        
    
    
    def _deleteFeaturesFromDictionary(self, dictMain, 
                                      dictForSorting, maxFeatures):
        
        dictForSorting = {k: v for k, v in sorted(dictForSorting.items(),
                                      key=lambda item: item[1])}
        # <- сортировка массива dictForSorting по возрастанию
        dictSize = len(dictMain)
        for key, i in zip(dictForSorting.keys(), range(len(dictMain))):
            if (i > dictSize - maxFeatures):
                break
            del dictMain[key]
    

    
if __name__ == '__main__':
    d = Dictionary()
    t1 = "text test lol kek cheburek"
    t2 = "fast text lol chto prikol"
    t3 = "text text fast fast text lol azaza slova slovo none"
    d.addData(t1)
    print("\nFullDict")
    print(d.getGlobalDictionary())
    print("\nLocDict")
    print(d.getLastDictionary())
    d.addData(t2)
    print("\nFullDict")
    print(d.getGlobalDictionary())
    print("\nLocDict")
    print(d.getLastDictionary())
    d.addData(t3)
    print("\nFullDict")
    print(d.getGlobalDictionary())
    print("\nLocDict")
    print(d.getLastDictionary())