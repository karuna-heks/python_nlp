import DbInteraction
from Param import Param



class MyCorpusInit:
    

    def __init__(self):
        p = Param() #читаем параметры для работы с json файла
        db = DbInteraction() #класс для взаимодействия с БД
        db.connectCorpus(p.readDBCorpusPath()) #
        
        corpusID = db.fillingCorpus(p.sebdToDB())
        #создать новую строчку в бд, заполнить её параметрами, извлечь id, 
        #создать новые таблицы для данных topicList, dictionary, texts
        
        
        
        
    
    def getParam(self):
        return self.p
    
    
    def stop(self):
        print("myCorpusInit - stop")
        #остановить соединение с бд
        