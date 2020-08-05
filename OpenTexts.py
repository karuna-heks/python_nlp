"""
v0.6.7
OpenTexts - файл, содержащий класс для открытия текстовых файлов, считывания
текстов. Позволяет работать со следующей структурой файлов:
    - исходная папка содержит n других папок. каждая папка является сборником
    текстов на определённую тематику. имя папки = название темы
    - внутри каждой папки m файлов (предпочтительно в формате .txt, но не 
    обязательно). каждый файл это отдельный текст, имя файла = название текста
Методы данного класса необходимы для прохождения всей структуры файловой и 
последовательным чтением данных из файловой структуры


#!!! - добавить описание общее
#!!! - добавить описание каждого метода
#!!! - удалить ненужные комментарии с описанием
#!!! - реализовать недостающие методы
#!!! - реализовать нормальный итератор
#!!! - реализовать обработчики ошибок
#!!! - перенести глобальные переменные класса внутрь конструктора
"""

import os
import sys
from nltk.corpus import brown
from corus import load_lenta

class OpenTexts:
    
    _path = ''
    _tempData = {'name': '', 
                'topicName': '',
                'baseText': ''}
    _topicNameList = None # список с именами топиков (тем)
    _textNameList = None # список с именами текстов конкретной темы
    
    _chooseMethod = 0 #0 - none, 1-searchFoler, 2-searchTxt, 3-searchAlt
    
    _iterTopic = 0 #iterator 1 - topics
    _iterText = 0 #iterator 2 - texts
    
    _isReady = False # статус прохождения проверки на наличие следующего 
    # текста
    _checkIncTopic = False # проверка разрешения на инкремент номера темы
    _checkIncText = False # проверка разрешения на инкремент номера текста
    
    _countText = 0
    _source = ''
    
    def __init__(self, source:str = "file", path:str="none"):
        self._source = source
        self._path = path
        if self._source == 'file':
            self._searchFolder()
        elif self._source == 'brown':
            self._searchBrown()
        elif (self._source == 'lenta.ru') or (self._source == 'lenta'):
            self._searchLenta()
    
    def _searchFolder(self):
        self._topicNameList = os.listdir(self._path)
        self._chooseMethod = 1
        #!!!добавить: проверка на то, что кол-во списков папок больше 0
        
    def _searchBrown(self):
        self._chooseMethod = 2
        
    def _searchLenta(self):
        path = 'lenta-ru-news.csv.gz'
        self._records = load_lenta(path)
        self._chooseMethod = 3
        self._lentaListOfThemes = {"Бизнес", "Госэкономика", "Кино",
                                   "Люди", "Музыка", "Наука", 
                                   "Происшествия", "Следствие и суд",
                                   "Украина", "Футбол"} 
        # <- 10 тем. в сумме 102.043-1 текстов
        
    def hasNext(self):
        # if self._countText == 5000:
        #     return False
        #!!! <- используется для дебага, для ограничения числа текстов
        if self._chooseMethod == 1:
            return self._hasNextSearchFolder()
        elif self._chooseMethod == 2:
            return self._hasNextSearchBrown()
        elif self._chooseMethod == 3:
            return self._hasNextSearchLenta()
        else: 
            return False
        
    def getNext(self):
        self._countText += 1
        sys.stdout.write("\rОткрыто: "+str(self._countText))
        if self._chooseMethod == 1:
            return self._getNextSearchFolder()
        elif self._chooseMethod == 2:
            return self._getNextSearchBrown()
        elif self._chooseMethod == 3:
            return self._getNextSearchLenta()
        else: 
            return False
  
  
    # @private methods
    def _hasNextSearchFolder(self):
        if (self._iterTopic < 1):
            if (self._iterText < 1):
                self._textNameList = os.listdir(self._path + "/" + 
                             self._topicNameList[self._iterTopic])
        # <- проверка на то, что счетчик пройденных топиков меньше 1
        # что означает, что отсчет только начинается
        # если проверка пройдена, то открыть 
        # папку с текстами, сохранить список текстов
        
        
        if (self._iterText < len(self._textNameList)):
            self._isReady = True
            self._checkIncText = True
            return True
        # <- если текущий счетчик количества пройденных текстов
        # всё ещё меньше количества текстов в папке, то
        # можно разрешать инкрементирование, для открытия этого
        # текста в методе _getNextSearchFoler
        
        else:
            if (self._iterTopic+1 < len(self._topicNameList)):
                self._textNameList = os.listdir(self._path + "/" +
                                 self._topicNameList[self._iterTopic+1])
                # <- если число пройденных топико ещё меньше чем кол-во
                # топиков общее, то строим путь к ещё одной папке с текстами
                # и открываем список файлов в этой папке
                if (len(self._textNameList) < 1):
                    return False
                else:
                    self._isReady = True
                    self._checkIncTopic = True
                    return True
                # <- если в новом списке нет элементов (<1), то 
                # запрещаем считывать новые тексты
                # иначе устанавливаем флаги на разрешение инкрементирования
                # счетчика
            else:
                return False
        #!!! <- возникнет проблема, если одна из папок в середине 
        # списка окажется пустой, тогда он остановит сканирование на ней
        
    
    def _getNextSearchFolder(self):
        if (self._isReady):
            # инкремент счетчиков, если это разрешено
            if self._checkIncTopic:
                self._iterTopic+=1
                self._checkIncTopic = False
                self._isReady = False
                self._iterText = 1
            elif self._checkIncText:
                self._iterText+=1
                self._checkIncText = False
                self._isReady = False
            else: 
                sys.exit("Error: No permission to iterate text number")
        else:
           sys.exit("Error: End of text list")
        # сохранение данных о имени, теме и самого текста 
        # во временной переменной и возврат её к вызываемой программе ->
        self._tempData['name'] = self._textNameList[self._iterText-1]
        self._tempData['topicName'] = self._topicNameList[self._iterTopic]
        self._tempData['baseText'] = self._getText(
            self._topicNameList[self._iterTopic],
            self._textNameList[self._iterText-1])
        return self._tempData
    

    def _hasNextSearchBrown(self):
        sizeOfBrownCorpus = len(brown.fileids())
        if self._countText < sizeOfBrownCorpus:
            self._isReady = True
            self._nameOfNextFile = brown.fileids()[self._countText]
            return True
        else: 
            self._isReady = False
            return False
        # <- выполнить проверку на то, что до этого не были выданы все 
        # тексты и дать разрешение на получение следующего
        
    
    def _getNextSearchBrown(self):
        if (self._isReady):
            self._isReady = False
        else:
            sys.exit("Error: End of text list or No permission to \
                     iterate text number")
        
        self._tempData['name'] = self._nameOfNextFile
        self._tempData['topicName'] = brown.categories(self._nameOfNextFile)[0]
        self._tempData['baseText'] = ' '.join(
            brown.words(self._nameOfNextFile))
        return self._tempData
        # <- запросить очередной текст
    
    
    def _hasNextSearchLenta(self):
        """
        Делаем некст(рекорд). если открылся, то сохраняем в параметр,
        если нет, то отправляем фолз
        """
        try:
            self._record = next(self._records)
            tagNotInList = not (self._record.tags in self._lentaListOfThemes)
            textIsEmpty = len(self._record.text) < 10
            
            while tagNotInList or textIsEmpty:
                self._record = next(self._records)
                tagNotInList = not (self._record.tags in self._lentaListOfThemes)
                textIsEmpty = len(self._record.text) < 10
        except StopIteration:
            return False
        
        self._isReady = True
        return True
    
    def _getNextSearchLenta(self):
        if (self._isReady):
            self._isReady = False
        else:
            sys.exit("Error: End of text list or No permission to \
                     iterate text number")
         
        self._tempData['name'] = self._parseLentaTitle(self._record.title)
        self._tempData['topicName'] = self._record.tags
        self._tempData['baseText'] = self._record.text.replace('"', '""') 
        return self._tempData
    
    def _parseLentaTitle(self, title):
        return title.replace("\xa0", " ").replace('"', '""') 
    
    
    # -> очень ненадёжный метод. нужно как следует его протестировать и
    # пофиксить
    def _getText(self, topic, text):
        path = self._path + "/" + topic + "/" + text
        # f = open(path, mode = "r", encoding = "ascii",)
        f = open(path, mode = "r", encoding = "utf-8")
        try:   
            # tempText = f.read().decode("utf-16")
            tempText = f.read()
            # <- прочитать текст
        except UnicodeError:
            f = open(path, mode = "r", encoding = "utf-16")
            try:
                tempText = f.read()
            except UnicodeError:
                f = open(path, mode = "r", encoding = "cp1251")
                try:
                    tempText = f.read()
                finally:
                    f.close()
            finally:
                f.close()
        finally:
            f.close()
        tempText = tempText.replace('"', '""') 
        # <- заменить символ " на "", для sqlite
        return tempText
        # склеивание пути, открытие текста, возврат текста
    
    
    
if __name__ == '__main__':
    path = '/mnt/hgfs/vmware D/topics'
    op = OpenTexts(path)
    op.searchFolder()
    while(op.hasNext()): 
        print(op.getNext())
