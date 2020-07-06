import os
import sys


class OpenTexts:
    
    __path = ''
    __tempData = {'name': '', 
                'topicName': '',
                'baseText': ''}
    __topicNameList = None # список с именами топиков (тем)
    __textNameList = None # список с именами текстов конкретной темы
    
    __chooseMethod = 0 #0 - none, 1-searchFoler, 2-searchTxt, 3-searchAlt
    
    __iterTopic = 0 #iterator 1 - topics
    __iterText = 0 #iterator 2 - texts
    
    __isReady = False # статус прохождения проверки на наличие следующего 
    # текста
    __checkIncTopic = False # проверка разрешения на инкремент номера темы
    __checkIncText = False # проверка разрешения на инкремент номера текста
    
    
    def __init__(self, path):
        print("OT__init__")
        self.__path = path
    
    def searchFolder(self):
        print("OTsearchFolder")
        self.__topicNameList = os.listdir(self.__path)
        self.__chooseMethod = 1
        #!!!добавить: проверка на то, что кол-во списков папок больше 0
        
    def searchTxt(self):
        print("OTsearchTxt")
        #добавить: реализация метода
        
    def searchAlt(self):
        print("OTsearchAlt")
        #добавить: реализация метода
        
    def hasNext(self):
        print("OThasNext")
        if self.__chooseMethod == 1:
            return self.__hasNextSearchFolder()
        elif self.__chooseMethod == 2:
            return self.__hasNextSearchTxt()
        elif self.__chooseMethod == 3:
            return self.__hasNextSearchAlt()
        else: 
            return False
        
    def getNext(self):
        print("OTgetNext")
        if self.__chooseMethod == 1:
            return self.__getNextSearchFolder()
        elif self.__chooseMethod == 2:
            return self.__getNextSearchTxt()
        elif self.__chooseMethod == 3:
            return self.__getNextSearchAlt()
        else: 
            return False
  
  
    # @private methods
    def __hasNextSearchFolder(self):
        print("OT__hasNextSearchFolder")
        if (self.__iterTopic < 1):
            if (self.__iterText < 1):
                self.__textNameList = os.listdir(self.__path + "/" + 
                             self.__topicNameList[self.__iterTopic])
        # <- проверка на то, что счетчик пройденных топиков меньше 1
        # что означает, что отсчет только начинается
        # если проверка пройдена, то открыть 
        # папку с текстами, сохранить список текстов
        
        
        if (self.__iterText < len(self.__textNameList)):
            self.__isReady = True
            self.__checkIncText = True
            return True
        # <- если текущий счетчик количества пройденных текстов
        # всё ещё меньше количества текстов в папке, то
        # можно разрешать инкрементирование, для открытия этого
        # текста в методе __getNextSearchFoler
        
        else:
            if (self.__iterTopic+1 < len(self.__topicNameList)):
                self.__textNameList = os.listdir(self.__path + "/" +
                                 self.__topicNameList[self.__iterTopic+1])
                # <- если число пройденных топико ещё меньше чем кол-во
                # топиков общее, то строим путь к ещё одной папке с текстами
                # и открываем список файлов в этой папке
                if (len(self.__textNameList) < 1):
                    return False
                else:
                    self.__isReady = True
                    self.__checkIncTopic = True
                    return True
                # <- если в новом списке нет элементов (<1), то 
                # запрещаем считывать новые тексты
                # иначе устанавливаем флаги на разрешение инкрементирования
                # счетчика
            else:
                return False
        #!!! <- возникнет проблема, если одна из папок в середине 
        # списка окажется пустой, тогда он остановит сканирование на ней
        
    
    def __getNextSearchFolder(self):
        print("OT__getNextSearchFoler")
        if (self.__isReady):
            # инкремент счетчиков, если это разрешено
            if self.__checkIncTopic:
                self.__iterTopic+=1
                self.__checkIncTopic = False
                self.__isReady = False
                self.__iterText = 1
            elif self.__checkIncText:
                self.__iterText+=1
                self.__checkIncText = False
                self.__isReady = False
            else: 
                sys.exit("Error: No permission to iterate text number")
        else:
           sys.exit("Error: End of text list")
        # сохранение данных о имени, теме и самого текста 
        # во временной переменной и возврат её к вызываемой программе ->
        self.__tempData['name'] = self.__textNameList[self.__iterText-1]
        self.__tempData['topicName'] = self.__topicNameList[self.__iterTopic]
        self.__tempData['baseText'] = self.__getText(
            self.__topicNameList[self.__iterTopic],
            self.__textNameList[self.__iterText-1])
        return self.__tempData
    
    
    
    def __hasNextSearchTxt(self):
        print("OT__hasNextSearchTxt")
        #добавить: реализация метода
        return True
    
    def __getNextSearchTxt(self):
        print("OT__getNextSearchTxt")
        #добавить: реализация метода
        return 0
    
    
    def __hasNextSearchAlt(self):
        print("OT__hasNextSearchAlt")
        #добавить: реализация метода
        return True
    
    def __getNextSearchAlt(self):
        print("OT__getNextSearchAlt")
            
        #добавить: реализация метода
        return 0
    
    def __getText(self, topic, text):
        print("OT__getText")
        path = self.__path + "/" + topic + "/" + text
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
