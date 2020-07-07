# -*- coding: utf-8 -*-
import re
from nltk.stem import PorterStemmer
import sys


class CorpusParser:
    
    __tempWordList = None # список слов в тексте
    __stopList = [] # список стоп-слов
    __stopListEng = []
    __stopListRus = []
    __ps = None # porter Stemmer
    
    #@ params
    __language = None
    __stemType = None
    __stopWordsType = None
    
    def __init__(self, language = 'eng', stemType = 'stemming',
                 stopWordsType = 'default'):
        print("CP__init")
        self.__language = language
        
        if (stemType == 'stemmer' or stemType == 'stem' or 
            stemType == 'stemming'):
            self.__stemType = 'stem'
            self.__ps = PorterStemmer()
        elif (stemType == 'lemmatization' or stemType == 'lemmatizing' or 
            stemType == 'lemma'):
            self.__stemType = 'lemma'
        elif (stemType == 'none' or stemType == 'no' or stemType == 'not' or
              stemType == 'n'):
            self.__stemType = 'none'
        else:
            self.__stemType = 'stem'
            self.__ps = PorterStemmer()
            
        if (stopWordsType == 'default'):
            self.__stopWordsType = 'default'
            #!!! продумать логику использования параметра стопВордс
            self.__initStopWords()
        
        
    def parsing(self, text):
        print("CPparsing")
        # получаем текст
        # отправляем в токенайзер
        # получаем список
        # удаляем стоп-слова из списка
        # отправляем список в стеммер/лемматизатор
        # возвращаем текст
        
        self.__tempWordList = self.__tokenizer(text)
        
        if (self.__stopWordsType == 'default'):
            #!!! продумать логику использования параметра стопВордс
            self.__tempWordList = self.__deleteStopWords(self.__tempWordList)
        
        if (self.__stemType == 'stem'):
            tempList = []
            for w in self.__tempWordList:
                tempList.append(self.__ps.stem(w))
            self.__tempWordList = tempList
            # <- создание списка. наполнение списка словами после стемминга
            #!!! добавить мультиязычность (пока только англ)
        elif (self.__stemType == 'lemma'):
            print("lemma")
            #!!! реализовать лемматизацию мультиязычную
             
            
        return " ".join(self.__tempWordList)
        
        
         
        
    # @private methods
    def __stemmer(self, wordList):
        print("CP__stemmer")
    
    def __lemmatizer(self, wordList):
        print("CP__lemmatizer")
        
    def __tokenizer(self, text):
        print("CP__tokenizer")
        text = text.lower()
        if self.__language == 'eng':
            text = re.sub(r"[^a-z]+", " ", text)
        elif self.__language == 'rus':
            text = re.sub(r"[^а-яё]+", " ", text)
        elif self.__language == 'mul':
            text = re.sub(r"[^a-zа-яё]+", " ", text)
        else:
            sys.exit("Error: unknown language")
        # <- перевод в нижний регистр и замена небуквенных символов пробелами
        #!!! продумать, что делать с цифрами. нужны ли они, или 
        # их нужно как другой мусор удалять
        # \b\W+\b|\b\W+$ - последовательности между словами (англ) и цифрами
        # \b[\W0-9]+\b|\b\W+$ - последовательности между словами  (англ)
        # [^a-zа-яA-ZА-ЯёЁ]+ - последовательности между словами русс и англ (любых)
        # [^a-zа-яё]+ - последовательности между словами русс и англ (нижн)
        # [^a-zа-яA-ZА-ЯёЁ0-9]+ - посл. межд. словами и цифрами любыми
        # [^a-z]+ - последовательности между словами (англ)
        return text.split(" ")

    
    def __deleteStopWords(self, wordList):
        print("CP__deleteStopWords")
        #!!! скорее всего, это медленный метод. нужно оптимизировать
        for word in self.__stopList:
            for i in range(wordList.count(word)):
                wordList.remove(word)
        return wordList
    
        
            
    def __initStopWords(self):
        print("CP__initStopWords")
        if (self.__language == 'eng' or self.__language == 'mul'):
            stopListEng = ['and', 'the', 'if', 'how', 'that', 
                              'then', 'those', 'this', 'those',
                              'can', 'be', 'will', 'would']
            self.__stopList.extend(stopListEng)
        if (self.__language == 'rus' or self.__language == 'mul'):
            stopListRus = ['а', 'или', 'и', 'в', 'у', 'к',
                                  'от', 'под', 'над', 'этот', 
                                  'тот', 'те', 'их']
            self.__stopList.extend(stopListRus)
        #!!! дополнить список стоп-слов для обоих языков
                              
                          
        
        

if __name__ == '__main__':
    cp = CorpusParser(language = 'eng', stemType = 'stemming',
                 stopWordsType = 'default')
    testText = """The colour designations for these iron plates are as follows: \
    1 kg is green, 1.5 kg is yellow, 2 kg is blue, 2.5 kg is red, \
    5 kg and 0.5 kg are white. It is useful to note the colour assignment \
    of these iron plates is consistent with the heavier bumper plates \
    (i.e. 1 kg and 10 kg are green, 1.5 kg and 15 kg are yellow, etc.)."""
    testText = cp.parsing(testText)
    print(testText)
    