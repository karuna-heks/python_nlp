# -*- coding: utf-8 -*-



class CorpusParser:
    
    def __init__(self):
        print("CP__init")
        
    def parsing(self, text):
        print("CPparsing")
        # получаем текст
        # отправляем в токенайзер
        # получаем список
        # отправляем в удалитель небукв. символов
        # делаем нижний регистр
        # удаляем стоп-слова из списка
        # отправляем список в стеммер/лемматизатор
        # возвращаем текст
        return text
        
        
    def setParam(self):
        print("CPsetParam")
        
        
         
        
    # @private methods
    def __stemmer(self, wordList):
        print("CP__stemmer")
    
    def __lemmatizer(self, wordList):
        print("CP__lemmatizer")
        
    def __tokenizer(self, text):
        print("CP__tokenizer")
        
    def __deleteStopWords(self, wordList):
        print("CP__deleteStopWords")
        return wordList
        
    def __deleteSymbols(self, wordList):
        print("CP__deleteSymbols")
        return wordList
    
    