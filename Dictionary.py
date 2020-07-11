# -*- coding: utf-8 -*-

class Dictionary:
    
    __global = None # глобальный словарь
    __last = None # последний локальный словарь
    
    __wordsList = None # список всех слов в тексте
    
    def __init__(self):
        print("D__init")
        self.__global = {}
        self.__last = {}
    
    
    def addData(self, text):
        print("DaddData")
        self.__last.clear()
        self.__wordsList = text.split(" ")
        for word in self.__wordsList:
            if self.__last.get(word) == None:
                self.__last[word] = 1
            else: 
                self.__last[word] = self.__last[word] + 1
        
        self.__addToGlobal(self.__last)
        # метод получает текст, получает из него 
        # локальный словарь, затем дополняет им глобальный 
        # словарь
        #!!! - реализовать метод
    
    def getGlobalDictionary(self):
        print("DgetFullDictionary")
        # метод возвращает глобальный словарь
        #!!! - реализовать метод
        return self.__global
    
    def getLastDictionary(self):
        print("DgetLastDictionary")
        # метод возвращает последний локальный словарь
        #!!! - реализовать метод
        return self.__last
    
    def getGlobalSize(self):
        return len(self.__global)
    
    def getLastSize(self):
        return len(self.__last)
    
    
    # @private methods
    def __addToGlobal(self, last):
        for key in last.keys():
            if self.__global.get(key) == None:
                self.__global[key] = last[key]
            else:
                self.__global[key] = self.__global[key] + last[key]
    
            
    
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