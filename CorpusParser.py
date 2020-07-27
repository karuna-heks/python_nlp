"""
27.07.2020 v0.1.9
CorpusParser - файл, содержащий методы и классы для парсинга 
исходных текстов:
    1. Разбивка текста на отдельные токены (слова)
    2. Удаление общеупотребительных-слов
    3. Выполнение операции стемминга/лемматизации
Обработка рассчитана на тексты, написанные кириллицей и/или латиницей

Параметры, которые используются классом CorpusParser задаются при
инициализации класса

#!!! - реализовать недостающие методы
#!!! - реализовать:
- поддержка русского, английского и рус/англ (mul, multilanguage) языков
- добавить стеммер портера для русского языка
- добавить лемматизацию для русского языка
- добавить лемматизацию для английского языка
- добавить фильтр общеупотребительных слов:
        - для английского языка
        - для русского языка
        - настройка фильтра (какое кол-во слов будет удаляться (степень
        жесткости фильтра))
- возможность фильтрации слов со слишком низкой частотой
- оптимизировать медленный метод фильтрации слов, либо удалить коммент о
необходимости оптимизации
"""
import re
from nltk.stem import PorterStemmer
import sys


class CorpusParser:
    
    _tempWordList = None # весь текст в виде списка слов
    _stopList = [] # список общеупотребительных слов
    _stopListEng = []
    _stopListRus = []
    _ps = None # porter Stemmer
    
    #@ params
    _language = None
    _stemType = None
    _stopWordsType = None
    
    def __init__(self, language: str = 'eng', stemType: str = 'stemming',
                 stopWordsType: str = 'default'):
        """
        В конструкторе класса выполняется определение дальнейших параметров,
        которые будут использоваться при выполнении обработки текстов
        Parameters
        ----------
        language : str, optional
            Язык корпуса данных. Может принимать значения "eng", "rus", "mul". 
             "mul" - мультиязычный (англ и рус). Каждый вариант, 
             в первую очередь, влияет на то, какие слова будут 
             игнорироваться фильтром. The default is 'eng'.
             #!!! - пока работает только "eng"
        stemType : str, optional
            Тип операции приведения слова к своей основе. Доступны 2 варианта
            "lemma" - лемматизация, "stemming" - стемминг. алгоритмы 
            различаются между собой как по скорости работы, так и по 
            качеству приведения к основе. The default is 'stemming'.
        stopWordsType : str, optional
            выбор способа отсечения стоп-слов. The default is 'default'.
            #!!! - пока работает только отсечение заранее определённого списка
            слов
        Returns
        -------
        None.
        """
        self._language = language
        
        if (stemType == 'stemmer' or stemType == 'stem' or 
            stemType == 'stemming'):
            self._stemType = 'stem'
            self._ps = PorterStemmer()
        elif (stemType == 'lemmatization' or stemType == 'lemmatizing' or 
            stemType == 'lemma'):
            self._stemType = 'lemma'
        elif (stemType == 'none' or stemType == 'no' or stemType == 'not' or
              stemType == 'n'):
            self._stemType = 'none'
        else:
            self._stemType = 'stem'
            self._ps = PorterStemmer()
            
        if (stopWordsType == 'default'):
            self._stopWordsType = 'default'
            #!!! продумать логику использования параметра стопВордс
            self._initStopWords()
        
        
    def parsing(self, text:str):
        """
        public parsing(self, text):
        Метод получает на вход исходный необработанный текст и возвращает
        текст, прошедший все выбранные этапы фильтрации. Во многом итоговый
        результат будет зависеть от того, какие параметры были заданы в
        конструкторе класса
        Parameters
        ----------
        text : str
            исходный текст.
        Returns
        -------
        str
            итоговый текст.
        """
        # получаем текст
        # отправляем в токенайзер
        # получаем список
        # удаляем общеупотребительные слова из списка
        # отправляем список в стеммер/лемматизатор
        # возвращаем текст
        
        self._tempWordList = self._tokenizer(text)
        # <- токенайзер делит текст на токены и приводит к нижнему регистру
        
        # -> удаление стоп-слов
        if (self._stopWordsType == 'default'):
            #!!! продумать логику использования параметра стопВордс
            self._tempWordList = self._deleteStopWords(self._tempWordList)
        
        # -> выделение основы слова
        if (self._stemType == 'stem'):
            tempList = []
            for w in self._tempWordList:
                tempList.append(self._ps.stem(w))
            self._tempWordList = tempList
            # <- создание списка. наполнение списка словами после стемминга
            #!!! добавить мультиязычность (пока только англ)
        elif (self._stemType == 'lemma'):
            print("lemma")
            #!!! реализовать лемматизацию мультиязычную
        return " ".join(self._tempWordList)
        
        
    # @private methods
    
    # def _stemmer(self, wordList):
        # print("CP__stemmer")
    
    # def _lemmatizer(self, wordList):
        # print("CP__lemmatizer")
        
    def _tokenizer(self, text:str):
        """
        private _tokenizer(self, text):
        метод приводит весь текст к нижнему регистру, затем выполняется 
        замена последовательности небуквенных символов (в зависимости
        от выбранного языка) на одиночные пробелы. по пробелам происходит
        разделение текста на список слов
        Parameters
        ----------
        text : str
            Исходный текст.
        Returns
        -------
        TYPE
            список слов в тексте.
        """
        text = text.lower()
        if self._language == 'eng':
            text = re.sub(r"[^a-z]+", " ", text)
        elif self._language == 'rus':
            text = re.sub(r"[^а-яё]+", " ", text)
        elif self._language == 'mul':
            text = re.sub(r"[^a-zа-яё]+", " ", text)
        else:
            sys.exit("Error: unknown language")
        # <- перевод в нижний регистр и замена небуквенных символов пробелами
        #!!! продумать, что делать с цифрами. нужны ли они, или 
        # их нужно как другой мусор удалять
        # подсказка по регулярным выражениям:
        # \b\W+\b|\b\W+$ - последовательности между словами (англ) и цифрами
        # \b[\W0-9]+\b|\b\W+$ - последовательности между словами  (англ)
        # [^a-zа-яA-ZА-ЯёЁ]+ - последовательности между словами русс и англ (любых)
        # [^a-zа-яё]+ - последовательности между словами русс и англ (нижн)
        # [^a-zа-яA-ZА-ЯёЁ0-9]+ - посл. межд. словами и цифрами любыми
        # [^a-z]+ - последовательности между словами (англ)
        return text.split(" ")

    
    def _deleteStopWords(self, wordList):
        """
        private _deleteStopWords(self, wordList):
        метод получает список со всеми словами в тексте и удаляет лишние
        слова, согласно правилам, которые задаются в конструкторе класса
        Parameters
        ----------
        wordList : TYPE
            Исходный список.
        Returns
        -------
        wordList : TYPE
            Отформатированный список.
        """
        #!!! скорее всего, это медленный метод. нужно оптимизировать
        for word in self._stopList:
            for i in range(wordList.count(word)):
                wordList.remove(word)
        return wordList
    
            
    def _initStopWords(self):
        """
        #!!! лучше использовать инструменты nltk
        метод со списком общеупотребительных слов
        """
        if (self._language == 'eng' or self._language == 'mul'):
            stopListEng = ['and', 'the', 'if', 'how', 'that', 
                              'then', 'those', 'this', 'those', 'it',
                              'can', 'be', 'will', 'would', 'for',
                              'are', 'as', 'is', 'to', 'of', 'with']
            self._stopList.extend(stopListEng)
        if (self._language == 'rus' or self._language == 'mul'):
            stopListRus = ['а', 'или', 'и', 'в', 'у', 'к',
                                  'от', 'под', 'над', 'этот', 
                                  'тот', 'те', 'их']
            self._stopList.extend(stopListRus)
        #!!! дополнить список общеупотребительных слов для обоих языков
        # и/или использовать инструменты из NLTK
                              

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
    