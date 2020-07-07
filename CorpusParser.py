# -*- coding: utf-8 -*-
import re


class CorpusParser:
    
    __tempWordList = None # список слов в тексте
    __stopList = [] # список стоп-слов
    __stopListEng = []
    __stopListRus = []
    
    #@ params
    __language = None
    __stemType = None
    __stopWordsType = None
    
    def __init__(self, language = 'eng', stemType = 'lemmatization',
                 stopWordsType = 'default'):
        print("CP__init")
        self.__language = language
        self.__stemType = stemType
        self.__stopWordsType = stopWordsType
        if (self.__stopWordsType == 'default'):
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
        
        return text
        
        
         
        
    # @private methods
    def __stemmer(self, wordList):
        print("CP__stemmer")
    
    def __lemmatizer(self, wordList):
        print("CP__lemmatizer")
        
    def __tokenizer(self, text):
        print("CP__tokenizer")
        text = text.lower()
        text = re.sub(r"[^a-zа-яA-ZА-ЯёЁ0-9]+", " ", text)
        # <- перевод в нижний регистр и замена небуквенных символов пробелами
        # \b\W+\b|\b\W+$ - последовательности между словами (англ) и цифрами
        # \b[\W0-9]+\b|\b\W+$ - последовательности между словами  (англ)
        # [^a-zа-яA-ZА-ЯёЁ]+ - последовательности между словами русс и англ (любых)
        # [^a-zа-яA-ZА-ЯёЁ0-9]+ - посл. межд. словами и цифрами любыми
        # [^a-z]+ - последовательности между словами (англ)
        

    
    def __deleteStopWords(self, wordList):
        print("CP__deleteStopWords")
        #!!! реалиовать метод
        return wordList
        
            
    def __initStopWords(self):
        print("CP__initStopWords")
        if (self.__language == 'eng' | self.__language == 'mul'):
            stopListEng = ['and', 'the', 'if', 'how', 'that', 
                              'then', 'those', 'this', 'those',
                              'can', 'be', 'will', 'would']
            self.__stopList.extend(stopListEng)
        if (self.__language == 'rus' | self.__language == 'mul'):
            stopListRus = ['а', 'или', 'и', 'в', 'у', 'к',
                                  'от', 'под', 'над', 'этот', 
                                  'тот', 'те', 'их']
            self.__stopList.extend(stopListRus)
        #!!! дополнить список стоп-слов для обоих языков
                              
                          
        
        

    
    