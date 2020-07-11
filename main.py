from DbInteraction import DbInteraction
from Param import Param
from OpenTexts import OpenTexts
from CorpusParser import CorpusParser
from Dictionary import Dictionary
from Vectorizer import Vectorizer
from CorpusAnalyzer import CorpusAnalyzer
import time
import json

# test comment 2

def main():
    print('start')
    
    t = time.localtime()
    compilationTime = "{0}.{1}.{2} {3}:{4}".format(t.tm_year, t.tm_mon, 
                                                   t.tm_mday, t.tm_hour, 
                                                   t.tm_min)
    
    p = Param() #инициализация класса с параметрами работы
    db = DbInteraction(p.readDBCorpusPath()) #иниц. класса для работы с БД
    # отправка в него пути к БД
    corpusID = db.getCorpusID() #сохранение актуального ID, который
    # является индексом строки в БД
    db.updateCorpus('name', p.readName(), corpusID) #добавление начальной инфо
    # рмации о корпусе. данные считываются с параметров и отправляются
    db.updateCorpus('language', p.readLanguage(), corpusID) #
    db.updateCorpus('stemType', p.readStemType(), corpusID) #
    db.updateCorpus('stopWordsType', p.readStopWordsType(), corpusID) #
    db.updateCorpus('metric', p.readMetric(), corpusID) #
    db.updateCorpus('compilationTime', compilationTime, corpusID)
    
    
    db.addInfo()
    db.updateInfo('name', p.readName(), 1) #добавление начальной инфо
    # рмации о корпусе. данные считываются с параметров и отправляются
    db.updateInfo('language', p.readLanguage(), 1)
    db.updateInfo('stemType', p.readStemType(), 1)
    db.updateInfo('stopWordsType', p.readStopWordsType(), 1)
    db.updateInfo('metric', p.readMetric(), 1)
    db.updateInfo('corpus_ID', corpusID, 1)
    db.updateInfo('compilationTime', compilationTime, 1)
    
    
    
    analyzer = CorpusAnalyzer() # аналайзер дополняет БД оставшимися данными
    
    op = OpenTexts(p.readDocCorpusPath()) # иниц. класса для работы с исходными
    # текстами
    op.searchFolder() # выбор метода для своего типа исходных данных 
    # (поиск папок с файлами, файлов с текстами или другой)  
    # searchFolder, searchTxt, searchAlt
    # !!! мб перенести выбор метода в json параметры. а внутри класса пусть
    # сам определяет, какой метод надо использовать, на основе параметров 
    while(op.hasNext()): # проверка на наличие следующего текста
        tempData = op.getNext() # извлечение базовой информации из 
        # файла, сохранение в словаре
        print("tempData: ")
        print(tempData)
        lastID = db.addTexts() # добавление новой строки в бд для 
        # информации по текстам и возврат её номера
        db.updateTexts('name', tempData['name'], lastID) # обновление 
        # данных в соответствующей строке
        db.updateTexts('topicName', tempData['topicName'], lastID) #
        db.updateTexts('baseText', tempData['baseText'], lastID) #
        
        analyzer.addTopicName(tempData['topicName'])
        db.updateTexts('topicNum', analyzer.getTopicNum(tempData['topicName']), lastID)
        # <- аналайзер необходим, для получения списка исползуемых топиков.
        # он запоминает имена топиков, присваивает им имена и, в данном месте,
        # отправляет имена в БД, для отчётности и для дальнейшего формирования
        # выходного вектора.
        
        
        
    for name, val, i in zip(analyzer.getList().keys(), 
                         analyzer.getList().values(),
                         range(analyzer.getNumOfTopics())):
        db.addTopicList() # добавление новой строки в бд для списка топиков
        db.updateTopicList('name', name, i+1)
        db.updateTopicList('topicNum', val, i+1)
        db.updateTopicList('numOfTexts', analyzer.getTopicCount(name), i+1)
        # <- обновление информации в таблице со списком топиков
        # общая информация, для отчетности
        
    
        
    parser = CorpusParser(language = p.readLanguage(), 
                          stemType = p.readStemType(),
                          stopWordsType = p.readStopWordsType)
    tempText = ''
    for i in range(db.getTextsSize()):
        tempText = db.getTextsData('baseText', i+1)[0][0]
        tempText = parser.parsing(tempText)
        db.updateTexts('formattedText', tempText, i+1)
    # <- выполняется полный проход по всем сырым текстам в бд
    # забираются сырые тексты, отправляются на очистку
    # возвращаются тексты после фильтрации и отправляются в БД обратно



    d = Dictionary()
    for i in range(db.getTextsSize()):
        d.addData(db.getTextsData('formattedText', i+1)[0][0])
        tempDict = d.getLastDictionary()
        tempStr = json.dumps(tempDict)
        tempStr = tempStr.replace('"', '""') 
        db.updateTexts('localDictionary', tempStr, i+1)
        # <- добавление в БД локальных словарей в виде json строки
    
    
    if p.saveDictionary == True:
        tempDict = d.getGlobalDictionary()
        for key, val in tempDict.items():
            lastID = db.addDictionary()
            db.updateDictionary('word', key, lastID)
            db.updateDictionary('value', val, lastID)
            # <- добавление глобального словаря в бд, целиком
            #!!! нужно пофиксить. работает слишком медленно
       
        
        
    numberOfTopics = db.getTopicListSize()
    numberOfTexts = db.getTextsSize()
    dictionarySize = d.getGlobalSize()
    db.updateCorpus('numOfTopics', numberOfTopics, corpusID)
    db.updateInfo('numOfTopics', numberOfTopics, 1)
    db.updateCorpus('numOfTexts', numberOfTexts, corpusID)
    db.updateInfo('numOfTexts', numberOfTexts, 1)
    db.updateCorpus('dictionarySize', dictionarySize, corpusID)
    db.updateInfo('dictionarySize', dictionarySize, 1)
    # <- обновление общей информации в БД (для отчетности)
    
    
    
    v = Vectorizer()
    v.addGlobDict(d.getGlobalDictionary())
    for i in range(db.getTextsSize()):
        tempStr = db.getTextsData('localDictionary', i+1)[0][0]
        tempDict = json.loads(tempStr)
        tempArray = v.getVecFromDict(tempDict)
        tempStr = json.dumps(tempArray)
        db.updateTexts('vector', tempStr, i+1)
        # <- инициализация векторизатора, отправка глобального словаря в 
        # него, извлечение из бд локального словаря, преобразование 
        # его из json-строки в стандартный словарь отправка словаря 
        # в векторизатор, получение массива преобразование массива 
        # в жсон-строку и отправка обратно в бд
    



if __name__ == '__main__':
    main()