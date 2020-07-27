"""
27.07.2020 v0.1.3
Класс CorpusAnalyser является вспомогательным классом, который
содержит различные инструменты для работы программы, которые,
по функциональности, тяжело отнести к любому другому классу, 
а оставлять их в main.py было бы неразумно, так как это бы 
излишне нагружало основной алгоритм программы.

Метод содержит инструменты для анализа списка тем, которые
содержатся в корпусе.

#!!! - сделать более грамотное описание каждого метода
#!!! - удалить ненужные комментарии с описанием
#!!! - реализовать недостающие методы
#!!! - продумать способ удаления почти одинаковых массивов
#!!! - Продумать решение об объединении этого файла или даже класса)
с другим файлом (классом) с целью уменьшения количества файлом в древе проекта
"""

class CorpusAnalyzer:
    
    _topicNames = {} # словарь со списком имён тем (топиков) и их номерами
    _topicNumOfTexts = [] # список количества текстов для каждого топика
    _topicListOfNames = [] # список с именами текстов по их порядковым номерам
    #!!! <- не лучшее решение иметь 2 списка одинаковых, нужно как-то исправить
    
    
    def addTopicName(self, name):
        """
        метод addTopicName необходим для создания внутренних списков,
        в которых хранятся имена тем. При вызове в метод отправляется имя
        темы, которой соответствует очередной анализируемый текст.
        По мере прохождения всех текстов и вызовов данного метода при анализе
        каждого из них - формируются списки
        
        метод получает имя топика, 
        если в списке топиков (_topicNames) такого имени ещё нет, 
        то добавляет его (имя) и добавляет новые элементы (соответсвующие
        этому имени темы) в другие списки и обновляет их значения.
        если такой элемент уже есть, то просто обновляет значения других списков
        """
        if self._topicNames.get(name) == None:
            lastTopicNum = len(self._topicNames)
            self._topicNames[name] = lastTopicNum
            self._topicNumOfTexts.append(1)
            self._topicListOfNames.append(name)
        else:
            lastTopicNum = self._topicNames[name]
            self._topicNumOfTexts[lastTopicNum] = self._topicNumOfTexts[lastTopicNum] + 1
        return lastTopicNum
        
    
    def getTopicNum(self, name):
        """
        метод getTopicNum получает имя тема и возвращает порядковый номер
        этой темы в списке тем
        """
        return self._topicNames[name]
        #!!! добавить обработку ошибок. в случае если такого имени нет в списке, 
        # или в случае, если метод был вызван неправильно
    
    
    def getList(self):
        """
        метод getList возвращает полный список имён тем с их порядковыми
        номерами
        """
        return self._topicNames
    
    
    
    def getTopicCount(self, name):
        """
        метод getTopicCount получает название темы и возвращает число,
        обозначающее количество текстов на эту тему
        """
        return self._topicNumOfTexts[self._topicNames[name]]
    #!!! добавить обработку ошибок. в случае если такого имени нет в списке, 
    # или в случае, если метод был вызван неправильно
    
    
    
    def getNumOfTopics(self):
        """
        метод getNumOfTopics возвращает количество тем
        """
        return len(self._topicNumOfTexts)
    
    
    
    def getTopicName(self, number):
        """
        метод getTopicName получает порядковый номер темы и возвращает
        название этой темы
        """
        return self._topicListOfNames[number]
    #!!! добавить обработку ошибок. в случае если такого номера нет в списке, 
    # или в случае, если метод был вызван неправильно
        
    
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
    
    
    
    
    
    
    
    
    
    