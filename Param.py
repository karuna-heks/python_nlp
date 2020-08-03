"""
v0.4.4
Param - класс, необходимый для работы с файлом параметров в формате json

#!!! Переработать класс под новый .json формат:
- организовать вложенность классов для удобного извлечения 
в соответствии с файлом
- реализовать один метод для извлечения, остальные - делают запрос к нему
- в списках реализовать итераторы для удобного доступа
- внести доп. исправления в param_example.json
- подробное описание списка параметров в readme файле сделать
- внутри класса Param.py сделать подробное описание каждого класса и метода 
для удобной справки по всему
- заменить read на get 
- перенести в Param из других классов и методов унификацию введённых 
пользователем параметров (Пример: "stem", "stemmer", "stemming" -> "stem")
"""

import json

class Param:
    
    def __init__(self, path=None):
        if path==None:
            f = open('param.json', 'r')
        else:
            f = open(path, 'r')
        self.json_param = f.read()
        f.close()
    
    def readString(self):
        return self.json_param
    
    def printParam(self):
        print("Полный список выбранных параметров программы:")
        print(self.json_param)

    def readName(self):
        return json.loads(self.json_param).get('name')

    def readLanguage(self):
        return json.loads(self.json_param).get('language')
    
    def readSource(self):
        return json.loads(self.json_param).get('source')
    
    def readStemType(self):
        return json.loads(self.json_param).get('stemType')
    
    def readStopWordsType(self):
        return json.loads(self.json_param).get('stopWordsType')
    

    
    def readDBCorpusPath(self):
        return json.loads(self.json_param).get('dbCorpusPath')
    
    def readDocCorpusPath(self):
        return json.loads(self.json_param).get('docCorpusPath')
    
    def saveDictionary(self):
        return json.loads(self.json_param).get('saveDictionary')
        
    def getPathToDBForReport(self):
        return json.loads(self.json_param).get('pathToDBForReport')
    
    
    
    def readMetric(self):
        return json.loads(self.json_param).get('metric')
    
    def readMaxFeatures(self):
        return json.loads(self.json_param).get('maxFeatures')
    
    
    
    #%% Neural Network Parameters
    def readEpochs(self):
        return json.loads(self.json_param).get('epochs')
    
    def getTrainPercentage(self):
        return json.loads(self.json_param).get('trainPercentage')
    
    def shuffleData(self):
        return json.loads(self.json_param).get('shuffleData')
    
    
        
if __name__ == '__main__':
    p = Param()
    p.printParam()
    # print(p.readString())
    # print(p.readName())
    # print(p.readDBCorpusPath())
    # print(p.saveDictionary())