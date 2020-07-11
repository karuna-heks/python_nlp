# -*- coding: utf-8 -*-

#!!! добавить описание класса

 #!!! удалить лишние методы и объекты, привести код класса в порядок 


class CorpusAnalyzer:
    
    _topicNames = {} # словарь со списком имён тем (топиков) и их номерами
    _topicNumOfTexts = [] # список количества текстов для каждого топика
    _topicListOfNames = [] # список с именами текстов по их порядковым номерам
    #!!! <- не лучшее решение иметь 2 списка одинаковых, нужно как-то исправить
    
    def __init__(self):
        print("CA__init")
        
    
    def addTopicName(self, name):
        print("CAaddTopicName")
        if self._topicNames.get(name) == None:
            lastTopicNum = len(self._topicNames)
            self._topicNames[name] = lastTopicNum
            self._topicNumOfTexts.append(1)
            self._topicListOfNames.append(name)
        else:
            lastTopicNum = self._topicNames[name]
            self._topicNumOfTexts[lastTopicNum] = self._topicNumOfTexts[lastTopicNum] + 1
        return lastTopicNum
        # <- метод получает имя топика, если в списке топиков
        # _topicNames такого ещё нет, то добавляет его и добавляет
        # новые элементы в другие списки и обновляет из значения
        # если такой элемент уже есть, то просто обновляет их значения
        
    def getTopicNum(self, name):
        print("CAgetTopicNum")
        return self._topicNames[name]
        # <- метод возвращает порядковый номер имени топика
    
    def getList(self):
        print("CAgetList")
        return self._topicNames
    
    def getTopicCount(self, name):
        print("CAgetTopicCount")
        return self._topicNumOfTexts[self._topicNames[name]]
        # <- метод возвращает количество топиков на тему name
    
    def getNumOfTopics(self):
        print("CAgetNumOfTopics")
        return len(self._topicNumOfTexts)
    
    def getTopicName(self, number):
        print("CAgetTopicName")
        return self._topicListOfNames[number]
        
    
if __name__ == '__main__':
    analyzer = CorpusAnalyzer()
    analyzer.addTopicName('kek')
    analyzer.addTopicName('mek')
    analyzer.addTopicName('pek')
    analyzer.addTopicName('kek')
    analyzer.addTopicName('pekk')
    analyzer.addTopicName('pek')
    print("\nkek: {0}, {1}".format(analyzer.getTopicNum('kek'), 
                                 analyzer.getTopicCount('kek')))
    
    print("\nmek: {0}, {1}".format(analyzer.getTopicNum('mek'), 
                                 analyzer.getTopicCount('mek')))
    
    print("\npek: {0}, {1}".format(analyzer.getTopicNum('pek'), 
                                 analyzer.getTopicCount('pek')))
    
    print("\npekk: {0}, {1}".format(analyzer.getTopicNum('pekk'), 
                                 analyzer.getTopicCount('pekk')))
    
    print("\nname1: {0}".format(analyzer.getTopicName(0)))
    print("\nname2: {0}".format(analyzer.getTopicName(1)))
    print("\nname3: {0}".format(analyzer.getTopicName(2)))
    print("\nname4: {0}".format(analyzer.getTopicName(3)))
    
    
    
    
    
    
    
    
    
    