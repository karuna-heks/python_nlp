from DbInteraction import DbInteraction
from Param import Param
from OpenTexts import OpenTexts


def main():
    print('start')
    
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
    
    
    
    
    op = OpenTexts(p.readDocCorpusPath()) # иниц. класса для работы с исходными
    # текстами
    op.searchFolder() # выбор метода для своего типа исходных данных 
    # (поиск папок с файлами, файлов с текстами или другой)  
    # searchFolder, searchTxt, searchAlt
    # !!! мб перенести выбор метода в json параметры. а внутри класса пусть
    # сам определяет, какой метод надо использовать, на основе параметров 
    while(op.hasNext()): # проверка на наличие следующего текста
        tempData = op.getNext() # извлечение базовой информации из 
        print("tempData: ")
        print(tempData)
        # файла, сохранение в словаре
        lastID = db.addTexts() # добавление новой строки в бд для 
        # информации по текстам и возврат её номера
        db.updateTexts('name', tempData['name'], lastID) # обновление 
        # данных в соответствующей строке
        db.updateTexts('topicName', tempData['topicName'], lastID) #
        db.updateTexts('baseText', tempData['baseText'], lastID) #
        
    


    



if __name__ == '__main__':
    main()