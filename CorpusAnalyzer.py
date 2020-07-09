# -*- coding: utf-8 -*-

class CorpusAnalyzer:
    
    _topicNames = {} # словарь со списком имён тем (топиков) и их номерами
    _topicNumOfTexts = [] # список количества текстов для каждого топика
    
    def __init__(self):
        print("CA__init")
        
    
    def addTopicName(self, name):
        print("CAaddTopicName")
        if self._topicNames.get(name) == None:
            lastTopicNum = len(self._topicNames)
            self._topicNames[name] = lastTopicNum
            self._topicNumOfTexts.append(1)
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
    
    def getTopicCount(self, name):
        print("CAgetTopicCount")
        return self._topicNumOfTexts[self._topicNames[name]]
        # <- метод возвращает количество топиков на тему name
    
    
        
    
if __name__ == '__main__':
    analyzer = CorpusAnalyzer()
    analyzer.addTopicName('kek')
    analyzer.addTopicName('mek')
    analyzer.addTopicName('pek')
    analyzer.addTopicName('kek')
    analyzer.addTopicName('pekk')
    analyzer.addTopicName('pek')
    print("kek: {0}, {1}".format(analyzer.getTopicNum('kek'), 
                                 analyzer.getTopicCount('kek')))
    
    print("mek: {0}, {1}".format(analyzer.getTopicNum('mek'), 
                                 analyzer.getTopicCount('mek')))
    
    print("pek: {0}, {1}".format(analyzer.getTopicNum('pek'), 
                                 analyzer.getTopicCount('pek')))
    
    print("pekk: {0}, {1}".format(analyzer.getTopicNum('pekk'), 
                                 analyzer.getTopicCount('pekk')))
    
    
    
    
    
    
    
    
    
    
    
    