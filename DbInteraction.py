"""
v0.7.1
DbInteraction - файл, содержащий методы и классы для взаимодействия
с базой данных sqlite3. 
Набор методов класса заточен для работа с базами данных конкретного
типа, с определённым набором таблиц.
БД Main содержит одну таблицу, в которую записывается общая информация
о корпусе, методах обработки этого корпуса, количества тем, количества
текстов, параметрами обработки и т.д.
БД Data относится к каждому конкретному случаю анализа корпуса. В нём
содержится, как общая информация, повторяющая таблицу из Main, так и 
частные результаты: в таблице Texts - информация обо всех текстах, результаты
форматирования этих текстов, векторизации, информация о теме, имени, полный
словарь и др. TopicList - содержит список тем и количественную информацию
о них. Dictionary - содержит словарь со всеми словами, входящими в корпус

Для работы необходим объект класса DbQuery, формирующий команды для
БД sqlite 

#!!! - добавить класс DbQuery в класс DbInteraction, т.к. они неразрывны
#!!! - продумать способ сделать методы более универсальными с целью удаления
практически одинаковых частей кода и методов
#!!! - перенести глобальные переменные класса внутрь конструктора
#!!! - добавить описание итераторам либо удалить их, либо исправить их
#!!! - добавить/исправить комментарии с алгоритмами работы конкретных
методов
"""
import sqlite3
from sqlite3 import Error
from DbQuery import DbQuery
import numpy as np
import json


class DbInteraction:
    
    _corpusID = '' #id корпуса, с которым идёт работа (номер актуальной строки файла corpuses.db)
    _connectionMain = None #параметр для хранения объекта соединения с БД всех корпусов
    _connectionData = None #параметр для хранения объекта соединения с БД по одному корпусу
    _q = None #экземпляр объекта класса формирующего запросы к БД
    _path = '' # путь к БД
    _dataCorpusName = ""
        
    def initFullAnalysis(self, path: str):
        """
        public initFullAnalysis(self, path: str):
        Метод является инициализацией данного объекта при полном
        анализе корпуса данных. То есть для: открытия файлов и сохранения
        исходных данных о текстах в БД, фильтрации текстов, векторизации и 
        нейросетевого анализа. 
        Parameters
        ----------
        path : str
            Путь к файлу БД, хранящем общую информацию обо всех корпусах,
            которые идут на анализ.

        Returns
        -------
        None.
        """
        self._path = path
        self._q = DbQuery()
        self._connectionMain = self._getConnect(path)
        self._corpusID = self._addCorpus()
        self._connectionData = self._addDbData(self._corpusID)
        self._addBaseDataTables(self._connectionData)
        #инициализировать класс с командами для БД
        #создать соединение с главным файлом БД, сохранить его
        #создать файл бд для корпуса
        #создать соединение с файлом БД для корпуса, сохранить его
        #создать основные таблицы в файле БД для корпуса
        
    def initNNAnalysis(self, path: str):
        """
        public initNNAnalysis(self, path: str):
        Метод является инициализацией данного объекта при нейросетевом
        анализе корпуса данных, только на основе готовых БД, содержащих
        входные и выходные вектора с данными

        Parameters
        ----------
        path : str
            Путь к файлу БД, хранящем информацию о конкретном корпусе данных
            с готовыми входными и выходными векторами для каждого текста.

        Returns
        -------
        None.
        """
        self._dataCorpusName = path
        self._connectionData = self._getConnect(self._dataCorpusName)
        self._q = DbQuery()
        
        
    def _addCorpus(self):
        """
        private _addCorpus(self):
        Метод добавляет новую строку в таблицу Corpuses, общей БД и возвращает
        ID новой созданной строки
        Returns
        -------
        tempStr : int
            ID созданной строки.
        """
        self._sendQuery(self._connectionMain, self._q.getNewStringMain())
        tempStr = self._readQuery(self._connectionMain, 
                                 self._q.getCountTableMain())[0][0]
        return tempStr
        
    
    def updateCorpus(self, strName:str, strVal, corpusID:int):
        """
        public updateCorpus(self, strName:str, strVal, corpusID:int):
        Метод обновляет данные в таблице Corpuses, общей БД.
        Parameters
        ----------
        strName : str
            Имя поля таблицы, которое будет изменено.
        strVal : str or int
            Значение таблицы, которое будет отправлено. (Значение находится
            на пересечении имени поля и ID строки)
        corpusID : int
            Уникальное ID строки таблицы.
        Returns
        -------
        None.
        """
        self._sendQuery(self._connectionMain, 
                       self._q.getUpdateMain(corpusID, strName, strVal))
        
        
    def getCorpusData(self, strName:str, corpusID:int):
        """
        public getCorpusData(self, strName:str, corpusID:int):
        Метод считывает данные из таблицы Corpuses, общей БД.
        Parameters
        ----------
        strName : str
            Имя поля таблицы, с которого будут прочитаны данные.
        corpusID : int
            Уникальное ID строки таблицы.
        Returns
        -------
        TYPE
            Двумерный массив с одним элементом str.
        """
        return self._readQuery(self._connectionMain, 
                              self._q.getDataTexts(corpusID, strName))
        
    
    def _addDbData(self, corpusID:int):
        """
        private _addDbData(self, corpusID:int):
        Метод создаёт файл БД с именем <corpusID>.db, соединяется с новой БД
        и сохраняет объект соединения с новой БД
        Parameters
        ----------
        corpusID : int
            ID новой БД, которой соответствует строка с общей БД и её таблице
            Corpuses.
        Returns
        -------
        TYPE
            Объект соединения с новой БД.
        """
        return self._getConnect(self._newDataPath(self._path, str(corpusID)+'.db'))
        
    
    def _addBaseDataTables(self, connectionData):
        """
        private _addBaseDataTables(self, connectionData):
        Метод добавляет базовые таблицы в БД для подробных данных по каждому
        корпусу
        Parameters
        ----------
        connectionData : TYPE
            Объект соединения с БД.
        Returns
        -------
        None.
        """
        self._addTableTopicList(connectionData)
        self._addTableTexts(connectionData)
        self._addTableDictionary(connectionData)
        self._addTableInfo(connectionData)
        
        
    def addTopicList(self):
        """
        public addTopicList(self):
        Добавление новой строки в таблицу. Будет автоматически добавлен
        уникальный параметр ID в новую созданную строку
        Returns
        -------
        TYPE: int
            ID созданной строки.
        """
        self._sendQuery(self._connectionData, 
                       self._q.getNewStringTopicList())
        return self._readQuery(self._connectionData, 
                              self._q.getCountTableTopicList())[0][0]
        
    
    def addTexts(self):
        """
        public addTexts(self):
        Добавление новой строки в таблицу. Будет автоматически добавлен
        уникальный параметр ID в новую созданную строку
        Returns
        -------
        TYPE: int
            ID созданной строки.
        """
        self._sendQuery(self._connectionData, 
                       self._q.getNewStringTexts())
        return self._readQuery(self._connectionData, 
                              self._q.getCountTableTexts())[0][0]
        
    
    def addDictionary(self):
        """
        public addDictionary(self):
        Добавление новой строки в таблицу. Будет автоматически добавлен
        уникальный параметр ID в новую созданную строку
        Returns
        -------
        TYPE: int
            ID созданной строки.
        """
        self._sendQuery(self._connectionData, 
                       self._q.getNewStringDictionary())
        return self._readQuery(self._connectionData, 
                              self._q.getCountTableDictionary())[0][0]
    
    
    def addInfo(self):
        """
        public addInfo(self):
        Добавление новой строки в таблицу. Будет автоматически добавлен
        уникальный параметр ID в новую созданную строку
        Returns
        -------
        TYPE: int
            ID созданной строки.
        """
        self._sendQuery(self._connectionData, 
                       self._q.getNewStringInfo())
        return self._readQuery(self._connectionData, 
                              self._q.getCountTableInfo())[0][0]
        
    
    def updateTopicList(self, strName:str, strVal, stringID:int):
        """
        public updateTopicList(self, strName:str, strVal, stringID:int):
        Метод обновляет данные в таблице TopicList, находящейся в БД с
        данными по каждому корпусу.
        Parameters
        ----------
        strName : str
            Имя поля таблицы, которое будет изменено.
        strVal : str or int
            Значение таблицы, которое будет отправлено. (Значение находится
            на пересечении имени поля и ID строки)
        stringID : int
            Уникальное ID строки таблицы.
        Returns
        -------
        None.
        """
        self._sendQuery(self._connectionData, 
                       self._q.getUpdateTopicList(stringID, strName, strVal))
        
        
    def updateTexts(self, strName:str, strVal, stringID:int):
        """
        public updateTexts(self, strName:str, strVal, stringID:int):
        Метод обновляет данные в таблице Texts, находящейся в БД с
        данными по каждому корпусу.
        Parameters
        ----------
        strName : str
            Имя поля таблицы, которое будет изменено.
        strVal : str or int
            Значение таблицы, которое будет отправлено. (Значение находится
            на пересечении имени поля и ID строки)
        stringID : int
            Уникальное ID строки таблицы.
        Returns
        -------
        None.
        """
        self._sendQuery(self._connectionData, 
                       self._q.getUpdateTexts(stringID, strName, strVal))
    
    
    def updateDictionary(self, strName:str, strVal, stringID:int):
        """
        public updateDictionary(self, strName:str, strVal, stringID:int):
        Метод обновляет данные в таблице Dictionary, находящейся в БД с
        данными по каждому корпусу.
        Parameters
        ----------
        strName : str
            Имя поля таблицы, которое будет изменено.
        strVal : str or int or float
            Значение таблицы, которое будет отправлено. (Значение находится
            на пересечении имени поля и ID строки)
        stringID : int
            Уникальное ID строки таблицы.
        Returns
        -------
        None.
        """
        self._sendQuery(self._connectionData, 
                       self._q.getUpdateDictionary(stringID, strName, strVal))
        
        
    def updateInfo(self, strName:str, strVal, stringID:int):
        """
        public updateInfo(self, strName:str, strVal, stringID:int):
        Метод обновляет данные в таблице Info, находящейся в БД с
        данными по каждому корпусу.
        Parameters
        ----------
        strName : str
            Имя поля таблицы, которое будет изменено.
        strVal : str or int
            Значение таблицы, которое будет отправлено. (Значение находится
            на пересечении имени поля и ID строки)
        stringID : int
            Уникальное ID строки таблицы.
        Returns
        -------
        None.
        """
        self._sendQuery(self._connectionData, 
                       self._q.getUpdateInfo(stringID, strName, strVal))
    
    
    def getTopicListData(self, strName:str, stringID:int):
        """
        public getTopicListData(self, strName:str, stringID:int):
        Метод считывает данные из таблицы Info, находящейся в БД с
        данными по каждому корпусу.
        Parameters
        ----------
        strName : str
            Имя поля таблицы, с которого будут прочитаны данные.
        stringID : int
            Уникальное ID строки таблицы.
        Returns
        -------
        TYPE
            Двумерный массив с одним элементом str.
        """
        return self._readQuery(self._connectionData, 
                              self._q.getDataTopicList(stringID, strName))
    
    
    def getTextsData(self, strName:str, stringID:int):
        """
        public getTextsData(self, strName:str, stringID:int):
        Метод считывает данные из таблицы Texts, находящейся в БД с
        данными по каждому корпусу.
        Parameters
        ----------
        strName : str
            Имя поля таблицы, с которого будут прочитаны данные.
        stringID : int
            Уникальное ID строки таблицы.
        Returns
        -------
        TYPE
            Двумерный массив с одним элементом str.
        """
        return self._readQuery(self._connectionData, 
                              self._q.getDataTexts(stringID, strName))
        
    
    def getDictionaryData(self, strName:str, stringID:int):
        """
        public getDictionaryData(self, strName:str, stringID:int):
        Метод считывает данные из таблицы Dictionary, находящейся в БД с
        данными по каждому корпусу.
        Parameters
        ----------
        strName : str
            Имя поля таблицы, с которого будут прочитаны данные.
        stringID : int
            Уникальное ID строки таблицы.
        Returns
        -------
        TYPE
            Двумерный массив с одним элементом str.
        """
        return self._readQuery(self._connectionData, 
                              self._q.getDataDictionary(stringID, strName))
    
    
    def getInfoData(self, strName:str, stringID:int):
        """
        public getInfoData(self, strName:str, stringID:int):
        Метод считывает данные из таблицы Info, находящейся в БД с
        данными по каждому корпусу.
        Parameters
        ----------
        strName : str
            Имя поля таблицы, с которого будут прочитаны данные.
        stringID : int
            Уникальное ID строки таблицы.
        Returns
        -------
        TYPE
            Двумерный массив с одним элементом str.
        """
        return self._readQuery(self._connectionData, 
                              self._q.getDataInfo(stringID, strName))
    
    
    def _addTableTopicList(self, connection):
        """
        private _addTableTopicList(self, connection):
        Добавление таблицы в локальную БД с данными по конкретному корпусу
        Parameters
        ----------
        connection : TYPE
            Объект соединения с таблицей.
        Returns
        -------
        None.
        """
        self._sendQuery(connection, self._q.getNewTableTopicList())
        
        
    def _addTableTexts(self, connection):
        """
        private _addTableTexts(self, connection):
        Добавление таблицы в локальную БД с данными по конкретному корпусу
        Parameters
        ----------
        connection : TYPE
            Объект соединения с таблицей.
        Returns
        -------
        None.
        """
        self._sendQuery(connection, self._q.getNewTableTexts())
        
        
    def _addTableDictionary(self, connection):
        """
        private _addTableDictionary(self, connection):
        Добавление таблицы в локальную БД с данными по конкретному корпусу
        Parameters
        ----------
        connection : TYPE
            Объект соединения с таблицей.
        Returns
        -------
        None.
        """
        self._sendQuery(connection, self._q.getNewTableDictionary())
        
    def _addTableInfo(self, connection):
        """
        private _addTableInfo(self, connection):
        Добавление таблицы в локальную БД с данными по конкретному корпусу
        Parameters
        ----------
        connection : TYPE
            Объект соединения с таблицей.
        Returns
        -------
        None.
        """
        self._sendQuery(connection, self._q.getNewTableInfo())
        
        
    def _getConnect(self, path:str):
        """
        private _getConnect(self, path:str):
        Метод, выполняющий подключение к БД и формирующий объект 
        с соединением к этой БД
        Parameters
        ----------
        path : str
            Путь к файлу БД.
        Returns
        -------
        connection : TYPE
            Объект соединения с БД.
        """
        connection = None
        try:
            connection = sqlite3.connect(path, check_same_thread=False)
        except Error as e:
            print(f"The error '{e}' occurred")
        return connection
        
        
    def _sendQuery(self, connection, q:str):
        """
        private _sendQuery(self, connection, q:str):
        Метод, отправляющий команду к БД
        Parameters
        ----------
        connection : TYPE
            Объект соединения с конкретной БД.
        q : str
            Запрос.
        Returns
        -------
        None.
        """
        cursor = connection.cursor()
        try:
            cursor.execute(q)
            connection.commit()
        except Error as e:
            print(f"The error '{e}' occurred")
    
    
    def _readQuery(self, connection, q:str):
        """
        private _readQuery(self, connection, q:str):
        Метод, отправляющий команду на чтение данных из БД
        Parameters
        ----------
        connection : TYPE
            Объект соединения с конкретной БД..
        q : str
            Команда.
        Returns
        -------
        result : TYPE
            Результат операции.
        """
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(q)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")
    
    
    def _newDataPath(self, oldPath:str, corpusID:str):
        """
        private _newDataPath(self, oldPath, corpusID:str):
        Вспомогательный метод. Склеивает старый путь к БД с новым именем БД
        (без добавления .db к имени файла)
        Parameters
        ----------
        oldPath : str
            Старый путь к БД.
        corpusID : str
            Новое имя БД.
        Returns
        -------
        TYPE: str
            Новый путь к БД.
        """
        oldPath = oldPath.rsplit('/', maxsplit=1)
        self._dataCorpusName = oldPath[0]+r'/'+corpusID
        return self._dataCorpusName
        
    
    def getCorpusID(self):
        """
        public getCorpusID(self):
        Вернуть ID последней строки общей БД
        Returns
        -------
        TYPE: int
            ID.
        """
        return self._corpusID
    
    def getTopicListSize(self):
        """
        public getTopicListSize(self):
        Считывает размер таблицы TopicList и возвращает её размер
        Returns
        -------
        TYPE: int
            Размер таблицы.
        """
        return self._readQuery(self._connectionData, 
                              self._q.getCountTableTopicList())[0][0]
    
    def getTextsSize(self):
        """
        public getTextsSize(self):
        Считывает размер таблицы Texts и возвращает её размер
        Returns
        -------
        TYPE: int
            Размер таблицы.
        """
        return self._readQuery(self._connectionData, 
                              self._q.getCountTableTexts())[0][0]
    
    def getDictionarySize(self):
        """
        public getDictionarySize(self):
        Считывает размер таблицы Dictionary и возвращает её размер
        Returns
        -------
        TYPE: int
            Размер таблицы.
        """
        return self._readQuery(self._connectionData, 
                              self._q.getCountTableDictionary())[0][0]
    
    def getInfoSize(self):
        """
        public getInfoSize(self):
        Считывает размер таблицы Info и возвращает её размер
        Returns
        -------
        TYPE: int
            Размер таблицы.
        """
        return self._readQuery(self._connectionData, 
                              self._q.getCountTableInfo())[0][0]
    
    
    def iterTopicList(self, strName):
        """
        #!!! - test method
        итератор для перебора столбца strName элементов БД TopicList
        """
        tableSize = self.getTopicListSize()
        for i in range(tableSize):
            yield self._readQuery(self._connectionData, 
                              self._q.getDataTopicList(i+1, strName))[0][0]
            
     
    class generator:
        """
        #!!! - test method
        """
        def __init__(self, size, path, strName1, strName2, featureExtract):
            self.q = DbQuery()
            self.size = size
            self.db2 = DbInteraction()
            self.db2.initNNAnalysis(path)
            self.s1 = strName1
            self.s2 = strName2
            self.fe = featureExtract
            
        def __call__(self):
            if self.fe in ['tf', 'tfidf']:
                for i in range(self.size):
                    if (self.s2 == None):
                        yield self.db2.readQuery(self.db2.getConnectionData(),
                                           self.q.getDataTexts(i+1, self.s1))[0][0] #!!! доп
                    else:
                        yield (json.loads(self.db2.getTextsData(self.s1, i+1)[0][0]),
                           json.loads(self.db2.getTextsData(self.s2, i+1)[0][0]))
            elif self.fe in ['emb', 'embm']:
                for i in range(self.size):
                    if (self.s2 == None):
                        yield np.array(self.db2.readQuery(self.db2.getConnectionData(),
                                                 self.q.getDataTexts(i+1, self.s1))[0][0])
                    else:
                        par1 = json.loads(self.db2.getTextsData(self.s1, i+1)[0][0])
                        par2 = json.loads(self.db2.getTextsData(self.s2, i+1)[0][0])
                        yield (np.array(par1),
                               np.array(par2))
    #!!! test!!!
    # def iterTexts(self, strName1=None, strName2=None, tableSize=0, c=None):
        # return generator
        # <- итератор для перебора столбца strName элементов БД Texts
            

       
    def getConnectionData(self):
        """
        public getConnectionData(self):
        Метод возвращает объект соединения с БД
        Returns
        -------
        TYPE
            Объект соединения с БД.
        """
        return self._connectionData
        
    
    def iterDictionary(self, strName1=None, strName2=None):
        """
        #!!! - test
        итератор для перебора столбца strName элементов БД Dictionary
        """
        tableSize = self.getTextsSize()
        for i in range(tableSize):
            if (strName2 == None):
                yield self._readQuery(self._connectionData, 
                              self._q.getDataDictionary(i+1, strName1))[0][0]
            else:
                yield (self._readQuery(self._connectionData, 
                              self._q.getDataDictionary(i+1, strName1))[0][0],
                       self._readQuery(self._connectionData, 
                              self._q.getDataDictionary(i+1, strName2))[0][0])
                

    def getDataCorpusName(self):
        """
        public getDataCorpusName(self):
        Метод возвращает путь к БД с полными данными по корпусу
        Returns
        -------
        TYPE: str
            Путь к БД.
        """
        return self._dataCorpusName


if __name__ == '__main__':
    db = DbInteraction()
    qTest = DbQuery()
    connect1 = db.getConnect(r"/mnt/hgfs/vmware D/myCorpusDB/myCorpuses11.db")
    connect2 = db.getConnect(r"/mnt/hgfs/vmware D/myCorpusDB/myCorpuses12.db")
    db._sendQuery(connect1, qTest.getNewTableDictionary())
    db._sendQuery(connect2, qTest.getNewTableTopicList())
    db._sendQuery(connect1, qTest.getNewTableTexts())
    
