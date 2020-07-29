"""
v0.6.0
Dictionary - файл, содержащий класс для работы со словарем/словарями 
корпуса текстов

#!!! - добавить описание общее
#!!! - добавить для каждого слова подсчёт числа документов, в которые 
оно входит
#!!! - добавить описание каждого метода
#!!! - удалить ненужные комментарии с описанием
#!!! - реализовать недостающие методы
#!!! - реализовать метод report() с выводом полного текстового отчета
"""
from utility import Table

class Dictionary:
    
    _global = None # глобальный словарь
    _last = None # последний локальный словарь
    _t = None # таблица для хранения дополнительных параметров слов
    
    
    _wordsList = None # список всех слов в тексте
    
    def __init__(self):
        self._global = {}
        self._last = {}
        self._t = Table(["count", "idf"])
    
    
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
    
    def getGlobalDictionary(self):
        # метод возвращает глобальный словарь
        return self._global
    
    def getLastDictionary(self):
        # метод возвращает последний локальный словарь
        return self._last
    
    def getGlobalSize(self):
        return len(self._global)
    
    def getLastSize(self):
        return len(self._last)
    
    def getAdditionalTable(self):
        #!!! реализовать более красивый способ передачи данных из таблицы,
        # а не просто возврат всей таблицы
        return self._t
    
    
    # @private methods
    def _addToGlobal(self, last):
        for key, val in last.items():
            if self._global.get(key) == None:
                self._global[key] = val
                self._t.setVal(key, "count", 1)
            else:
                self._global[key] = self._global[key] + val
                self._t.setVal(key, "count", self._t.getVal(key, "count") + 1)
    
            
    
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