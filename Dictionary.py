"""
27.07.2020 v0.5
Dictionary - файл, содержащий класс для работы со словарем/словарями 
корпуса текстов

#!!! - добавить описание общее
#!!! - добавить описание каждого метода
#!!! - удалить ненужные комментарии с описанием
#!!! - реализовать недостающие методы
"""

class Dictionary:
    
    _global = None # глобальный словарь
    _last = None # последний локальный словарь
    
    _wordsList = None # список всех слов в тексте
    
    def __init__(self):
        self._global = {}
        self._last = {}
    
    
    def addData(self, text):
        self._last.clear()
        self._wordsList = text.split(" ")
        for word in self._wordsList:
            if self._last.get(word) == None:
                self._last[word] = 1
            else: 
                self._last[word] = self._last[word] + 1
        
        self._addToGlobal(self._last)
        # метод получает текст, получает из него 
        # локальный словарь, затем дополняет им глобальный 
        # словарь
        #!!! - реализовать метод
    
    def getGlobalDictionary(self):
        # метод возвращает глобальный словарь
        #!!! - реализовать метод
        return self._global
    
    def getLastDictionary(self):
        # метод возвращает последний локальный словарь
        #!!! - реализовать метод
        return self._last
    
    def getGlobalSize(self):
        return len(self._global)
    
    def getLastSize(self):
        return len(self._last)
    
    
    # @private methods
    def _addToGlobal(self, last):
        for key in last.keys():
            if self._global.get(key) == None:
                self._global[key] = last[key]
            else:
                self._global[key] = self._global[key] + last[key]
    
            
    
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