# -*- coding: utf-8 -*-
import sys

class Vectorizer:
    
    
    _globalDict = None
    
    def __init__(self, vType = "tf"):
        print("V__init")
    
    def addGlobDict(self, globalDictionary):
        self._globalDict = globalDictionary
        #!!! необходимо передавать копию словаря, а не просто ссылку
    
    def getVecFromDict(self, d): 
        print("VaddDict")
        if (self._globalDict == None):
            sys.exit("Error: Global Dictionary is not initiliazed")
        
        tempArray = []
        # for key, val, i in zip(self._globalDict.keys(), 
        #                        self._globalDict.values(),
        #                        range(len(self._globalDict))):
        for key, val, in self._globalDict.items():
            if d.get(key) != None:
                tempArray.append(d.get(key))
            else:
                tempArray.append(0)
        return tempArray
    # <- метод получает словарь, содержащий все слова определённого текста
    # и сравнивая его содержимое с глобальным словарём, который должен
    # быть добавлен заранее, методом addGlobDict, формирует вектор
    #!!! - необходимо строить вектор на основе метрики tf и/или  tf-idf (дополнить)
    
    
    
    
    def numToOutputVec(self, num, size):
        tempVec = []
        tempVec = [0]*size
        tempVec[num] = 1
        
    
    
    
    
if __name__ == '__main__':
    v = Vectorizer()
    d = {'a':32, 'b':43, 'c':33, 'd':44, 'e':55, 'f':66}
    d2 = {'b':91, 'd':95, 'a':93}
    v.addGlobDict(d)
    testArray = v.getArrayFromDict(d2)