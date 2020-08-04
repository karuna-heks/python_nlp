"""
v1.0.4
Param - класс, необходимый для работы с файлом параметров в формате json

#!!! Переработать класс под новый .json формат:
- в списках реализовать итераторы для удобного доступа
- подробное описание списка параметров в readme файле сделать
- внутри класса Param.py сделать подробное описание каждого класса и метода 
для удобной справки по всему
"""

import json
import sys

class Param2:
    
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
    
    
    
    #% Neural Network Parameters
    def readEpochs(self):
        return json.loads(self.json_param).get('epochs')
    
    def getTrainPercentage(self):
        return json.loads(self.json_param).get('trainPercentage')
    
    def shuffleData(self):
        return json.loads(self.json_param).get('shuffleData')
    

class Param():
         
    def __init__(self, path=None):
        if path==None:
            f = open('param.json', 'r')
        else:
            f = open(path, 'r')
        self.json_param = f.read()
        f.close()
        self.source = SourceParam(self)
        self.parser = ParserParam(self)
        self.featureExtraction = FeatureExtractionParam(self)
        self.neuralNetwork = NeuralNetworkParam(self)
        self.database = Database(self)

    def getName(self):
        """
        Возвращает заданное имя файла отчета
        """
        return json.loads(self.json_param).get('name')
    
    def readParam(self):
        return self.json_param
    
    def printParam(self):
        print("Полный список выбранных параметров программы:")
        print(self.json_param)
     
        
class SourceParam:
    """
    Класс Source содержит методы для извлечения параметров источника данных
    (Корпуса)
    """
    
    def __init__(self, obj):
        self.obj = obj
    
    def getCorpusName(self):
        """
        Метод возвращает название текстового корпуса.
        lenta, file или brown

        Returns:
        str: Название текстового корпуса.
        """
        result = json.loads(self.obj.json_param).get('source')["corpusName"]
        result = result.lower()
        if (
                (result == "lenta") or (result == "lenta.ru") or 
                (result == "lentaru")
            ):
            return "lenta"
        
        elif (
                (result == "file") or (result == "files") or
                (result == "folder")
            ):
            return "file"
        
        elif (
                (result == "brown") or (result == "nltk-brown") or
                (result == "nltk") or (result == "nltkbrown")
            ):
            return "brown"
        
        else:
            sys.exit("Error: unknown CorpusName parameter: "+str(result))
            
            
    def getCorpusPath(self):
        """
        Метод возвращает путь к текстовому корпусу.
        Актуально только при использовании корпуса "file"

        Returns:
        str: Путь
        """
        return json.loads(self.obj.json_param).get('source')["corpusPath"]


class ParserParam:
    """
    Класс Parser содержит методы для извлечения параметров работы парсера
    """
    def __init__(self, obj):
        self.obj = obj
    
    def getLanguage(self):
        """
        Метод возвращает выбранный язык текстового корпуса.
        rus, eng или mul

        Returns:
        str: язык текстового корпуса.
        """
        result = json.loads(self.obj.json_param).get('parser')["language"]
        result = result.lower()
        if (
                (result == "russian") or (result == "rus") or 
                (result == "ru")
            ):
            return "rus"
        
        elif (
                (result == "english") or (result == "eng")
            ):
            return "eng"
        
        elif (
                (result == "multilanguage") or (result == "mul") or
                (result == "multi")
            ):
            return "mul"
        
        else:
            sys.exit("Error: unknown Language parameter: "+str(result))


    def getStemType(self):
        """
        Метод возвращает выбранный вид операции стемминга.
        Доступны варианты: "lemma", "stem", "none".

        Returns:
        str: Вид операции стемминга.
        """
        result = json.loads(self.obj.json_param).get('parser')["stemType"]
        result = result.lower()
        if (
                (result == "stemmer") or (result == "stem") or 
                (result == "stemming") or (result == "stemm")
            ):
            return "stem"
        
        elif (
                (result == "lemmatization") or (result == "lemma") or
                (result == "lemmatizing") or (result == "lemm") or
                (result == "lem") or (result == "lema")
            ):
            return "lemma"
        
        elif (
                (result == "none") or (result == "no") or
                (result == "not") or (result == "n")
            ):
            return "none"
        
        else:
            sys.exit("Error: unknown StemType parameter: "+str(result))
            
    def getStopWordsType(self):
        """
        Метод возвращает параметр , отвечающий за удаление стоп-слов
        Доступны варианты: "default", "none"

        Returns:
        str
        """
        return json.loads(self.obj.json_param).get('parser')["stopWordsType"]
     
        
class FeatureExtractionParam:
    """
    Класс FeatureExtractionParam содержит методы для извлечения 
    параметров работы подпрограммы извлечения векторов признаков из текстов
    """
    
    def __init__(self, obj):
        self.obj = obj
    
    def getNgrammType(self):
        """
        Метод возвращает название способа формирования н-грамм.
        Доступные варианты "unigram", "bigram", "trigram"

        Returns:
        str
        """
        result = json.loads(self.obj.json_param).get('featureExtraction')["ngrammType"]
        result = result.lower()
        if (
                (result == "unigram") or (result == "unigramma") or 
                (result == "unigrama") or (result == "unigramm") or
                (result == "1") or (result == "uni") or (result == "one")
            ):
            return "unigram"
        
        elif (
                (result == "bigram") or (result == "bigramma") or
                (result == "bigramm") or (result == "bigrama") or
                (result == "digram") or (result == "digramma") or
                (result == "digramm") or (result == "digrama") or
                (result == "2") or (result == "bi") or (result == "di") or
                (result == "two")
            ):
            return "bigram"
        
        elif (
                (result == "trigram") or (result == "trigramma") or 
                (result == "trigrama") or (result == "trigramm") or
                (result == "3") or (result == "tri") or (result == "three")
            ):
            return "trigram"
        
        else:
            sys.exit("Error: unknown NgrammType parameter: "+str(result))
    
    
    def getMetricType(self):
        """
        Выбор метрики для формирования векторов. 
        Доступны варианты: "tf" и "tfidf" 
        tf -- вектор строится на основе частоты появления слова в тексте. 
        tfidf -- вектор строится на основе величины TF-IDF.
        (word2Vec)

        Returns:
        str
        """
        result = json.loads(self.obj.json_param).get('featureExtraction')["metric"]
        result = result.lower()
        if (
                (result == "tf")
            ):
            return "tf"
        
        elif (
                (result == "tfidf") or (result == "tf-idf") 
            ):
            return "tfidf"
        
        elif (
                (result == "word2vec") 
            ):
            return "word2vec"
        
        else:
            sys.exit("Error: unknown MetricType parameter: "+str(result))
            
    
    def getMaxFeatures(self):
        """
        Максимальное число признаков для нейросетевого анализа. 
        Доступны варианты в диапазоне 100-10000 либо "none". 
        Из всех слов формируется набор признаков из которого и будет 
        формироваться выходной вектор для обучения. При слишком большом 
        количестве признаков может не хватить оперативной памяти 
        для обработки всех текстов, а, также скорость обучения будет 
        очень низкой из-за большого количества параметров. При слишком 
        низком количестве признаков высока вероятность потери ключевых 
        признаков для выполнения корректной операции обучения сети. 
        Если выбран параметр "none", то число признаков останется без 
        изменений и будет зависеть от размера корпуса.

        Returns:
        str
        """
        result = json.loads(self.obj.json_param).get('featureExtraction')["maxFeatures"]
        if (isinstance(result, int)):
            if result > 100:
                return result
        result = result.lower()
        if (
                (result == "none") or (result == "no")  or 
                (result == "not") 
            ):
            return "none"
        else:
            sys.exit("Error: unknown MaxFeatures parameter: "+str(result))
        
        
class NeuralNetworkParam:
    """
    Класс NeuralNetworkParam содержит методы для извлечения 
    параметров работы нейронной сети
    """
    
    def __init__(self, obj):
        self.obj = obj
    
    def getEpochs(self):
        """
        Получить количество эпох обучения

        Returns:
        int
        """
        result = json.loads(self.obj.json_param).get('neuralNetwork')["epochs"]
        return result
        
    def getShuffleStatus(self):
        """
        Получить информацию о необходимости сортировки входных данных

        Returns:
        bool
        """
        result = json.loads(self.obj.json_param).get('neuralNetwork')["shuffleData"]
        return result 
    
    def getTrainPercentage(self):
        """
        Количество (в процентах) тренировочных данных из всего 
        размера корпуса. Диапазон от 1 до 100. 
        Значение 70 означает, что 70% данных будет в обучающей 
        выборке, а 30% - в тестовой.
        
        Returns:
        int
        """
        result = json.loads(self.obj.json_param).get('neuralNetwork')["trainPercentage"]
        return result
    
class Database:
    """
    Класс NeuralNetworkParam содержит методы для извлечения 
    параметров работы нейронной сети
    """
    
    def __init__(self, obj):
        self.obj = obj
    
    def getDbCorpusPath(self):
        return json.loads(self.obj.json_param).get('database')["dbCorpusPath"]
        
    def getPathForReport(self):
        return json.loads(self.obj.json_param).get('database')["pathToDBForReport"]
        
    def getSaveDictionaryStatus(self):
        return json.loads(self.obj.json_param).get('database')["saveDictionary"]
        
        
if __name__ == '__main__':
    p = Param2()
    p.printParam()
    # print(p.readString())
    # print(p.readName())
    # print(p.readDBCorpusPath())
    # print(p.saveDictionary())
    
    p2 = Param()
    print(p2.source.getCorpusName())
    print(p2.source.getCorpusPath())
    
    print(p2.parser.getLanguage())
    print(p2.parser.getStemType())
    print(p2.parser.getStopWordsType())
    
    print(p2.featureExtraction.getNgrammType())
    print(p2.featureExtraction.getMetricType())
    print(p2.featureExtraction.getMaxFeatures())
    
    print(p2.neuralNetwork.getEpochs())
    print(p2.neuralNetwork.getShuffleStatus())
    print(p2.neuralNetwork.getTrainPercentage())
    
    print(p2.database.getDbCorpusPath())
    print(p2.database.getPathForReport())
    print(p2.database.getSaveDictionaryStatus())
    
    
    