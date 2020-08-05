"""
v0.7.1
Dictionary - файл, содержащий класс для работы со словарем/словарями 
корпуса текстов

#!!! - добавить описание общее
#!!! - исправить ошибку добавления точек в словарь, в случае, если они были
в отпарсеном тексте
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
import nltk
from nltk import ngrams
import re

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
    
    def __init__(self, metricType:str="tf", ngram:str="unigram", 
                 ignoreWordOrder:bool=True):
        self._globalDict = {}
        self._last = {}
        self._metric = metricType
        self._ignoreWordOrder = ignoreWordOrder
        self._ngram = ngram
        self._t = Table(["count", "idf", "tfidf"])
    
    
    def addData(self, text):
        """ 
        public addData(self, text):
        метод берёт отпарсеный текст и получает из него токены, которые
        добавляются в локальные и глобальный словарь
        Returns: none
        """
        self._last.clear()
        if (self._ngram == "unigram"):
            self._wordsList = text.split(" ")
            for word in self._wordsList:
                if self._last.get(word) == None:
                    self._last[word] = 1
                else: 
                    self._last[word] = self._last[word] + 1
            # <- если необходимо искать униграммы, то происходит перебор всего
            # текста по словам. если слово есть в словаре, то увеличить
            # счетчик этого слова в нём. если нет, то добавить и сделать
            # счетчик = 1
                 
        else: 
            if (self._ngram == 'bigram'):
                self._parseNgram(text, self._last, 2, self._ignoreWordOrder)
            elif (self._ngram == 'trigram'):
                self._parseNgram(text, self._last, 3, self._ignoreWordOrder)
                self._parseNgram(text, self._last, 2, self._ignoreWordOrder)
            else:
                sys.exit("Error: Unknown ngram parameter: " + self._ngram)
            # <- если необходимо искать би- или три-граммы, то отправить
            # всю работу на выполнение в метод парсинга н-грамм
                
            text = re.sub(r"[a-zа-яё]{0,0}[\s]+[$a-zа-яё]{0,0}", 
                          " ", text)
            text = re.sub(r"[a-zа-яё]{0,0}[\s.]*[.]+[\s.]*[a-zа-яё]{0,0}", 
                              " . ", text)
            sentenceList = text.split(" . ")
            for sentence in sentenceList:
                self._wordsList = sentence.split(" ")
                for word in self._wordsList:
                    if word == ' ' or word == '':
                        continue
                    if self._last.get(word) == None:
                        self._last[word] = 1
                    else:
                        self._last[word] = self._last[word] + 1
            # <- после выявления три- и би-грамм, происходит поиск униграмм
            #!!! продумать более простую конструкцию для этих действий всех

                        
        if len(self._last) < 1:
            sys.exit("Error: Local dictionary size is zero")

        self._addToGlobal(self._last)
        # метод получает текст, получает из него 
        # локальный словарь, затем дополняет им глобальный 
        # словарь
    
    def _parseNgram(self, fullText:str, localDict, n:int, ignoreWordOrder: bool):
        """
        private _parseNgram(self, text:str, localDict, 
        n:int, ignoreWordOrder: bool):
        
        Метод выполняет создание локального словаря n-грамм, в зависимости
        от параметров
        """
        text = re.sub(r"[a-zа-яё]{0,0}[\s]+[$a-zа-яё]{0,0}", 
                          " ", fullText)
        text = re.sub(r"[a-zа-яё]{0,0}[\s.]*[.]+[\s.]*[a-zа-яё]{0,0}", 
                          " . ", text)
        sentenceList = text.split(" . ")
        for sentence in sentenceList:
            self._wordsList = sentence.split(" ")
            for ngram in ngrams(self._wordsList, n):
                if ignoreWordOrder:
                    ngramFinal = ' '.join(sorted(ngram))
                else:
                    ngramFinal = ' '.join(ngram)
                if localDict.get(ngramFinal) == None:
                    localDict[ngramFinal] = 1
                else:
                    localDict[ngramFinal] = localDict[ngramFinal] + 1
            # <- текст разбивается на предложения. затем, они на список слов
            # выполняется составление н-грамм предложения. 
            # если для алгоритма не важен порядок слов при сравнении н-грамм
            # то происходит сортировка токена (из 2х или 3х слов), 
            # далее, далее идёт сравнение со словарем локальным. елси же 
            # порядок слов важен, то сортировки не происходит
        return localDict

    
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
    d = Dictionary("tf", "trigram", False)
    t1 = ". text test lol kek cheburek . prikol . prikol . lol kek . kek lol"
    t2 = "fast text  lol chto prikol . fast fast text slova lol . a"
    t3 = "text text fast fast text lol . azaza slova slovo none . none prikol ."
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
    ddd = d.getGlobalDictionary()