import sqlite3
from sqlite3 import Error
from DbQuery import DbQuery

class DbInteraction:
    
    corpusID = '' #id корпуса, с которым идёт работа (номер актуальной строки файла corpuses.db)
    connectionMain = None #параметр для хранения объекта соединения с БД всех корпусов
    connectionData = None #параметр для хранения объекта соединения с БД по одному корпусу
    q = None #экземпляр объекта класса формирующего запросы к БД
    path = ''
    topicListTableName = ""
    textsTableName = ""
    dictionaryTableName = ""
    
    def __init__(self, path):
        print("dbInteraction init")
        self.path = path
        self.q = DbQuery()
        self.connectionMain = self.getConnect(path)
        self.corpusID = self.addCorpus()
        self.connectionData = self.addDbData(self.corpusID)
        self.addBaseDataTables(self.connectionData)
        #+инициализировать класс с командами для БД
        #создать соединение с главным файлом БД, сохранить его
        #создать файл бд для корпуса
        #создать соединение с файлом БД для корпуса, сохранить его
        #создать основные таблицы в файле БД для корпуса
        
        
    def addCorpus(self):
        print("dbAddCorpus")
        self.sendQuery(self.connectionMain, self.q.getNewStringMain())
        tempStr = self.readQuery(self.connectionMain, 
                                 self.q.getCountTableMain())[0][0]
        print("tempStr:")
        print(tempStr)
        return tempStr
        # <- метод добавляет новую строку в общую БД и возвращает айди строки
        # return self.readQuery(connection, self.q.getCountTableMain())
        #+ отправить команду на добавление строки пустой
        # считать id последней строки 
        # вернуть id
        
    
    def updateCorpus(self, strName, strVal, corpusID):
        print("dbUpdateCorpus: {0}, {1}, {2}".format(strName, strVal, corpusID))
        self.sendQuery(self.connectionMain, 
                       self.q.getUpdateMain(corpusID, strName, strVal))
        #+ вызов метода добавления данных в корпус, по actualCorpusID
        
        
    def getCorpusData(self, strName, corpusID):
        print("dbGetCorpusData: {0}, {1}".format(strName, corpusID))
        return self.readQuery(self.connectionMain, 
                              self.q.getDataTexts(corpusID, strName))
        #+ вызов метода получения данных из строки таблицы
        # вернуть strVal
        
    
    def addDbData(self, corpusID):
        print("dbAddDataDb: {0}".format(corpusID))
        return self.getConnect(self.newDataPath(self.path, str(corpusID)+'.db'))
        #+ вызов метода добавления файла базы данных с именем <corpusID>.db
        # сохранить объект соединения с новой бд
        
    
    def addBaseDataTables(self, connectionData):
        print("dbAddBaseDataTables: {0}".format(connectionData))
        self.addTableTopicList(self.connectionData)
        self.addTableTexts(self.connectionData)
        self.addTableDictionary(self.connectionData)
        self.addTableInfo(self.connectionData)
        #+вызов методов добавления таблиц в бд для полных данных корпуса (myData.bd)
        
        
    def addTopicList(self):
        print("dbTopicList")
        self.sendQuery(self.connectionData, 
                       self.q.getNewStringTopicList(self.corpusID))
        return self.readQuery(self.connectionData, 
                              self.q.getCountTableTopicList())[0][0]
        #+ отправить команду на добавление строки непустой
        # считать id последней строки 
        # вернуть id
        
    
    def addTexts(self):
        print("dbAddTexts")
        self.sendQuery(self.connectionData, 
                       self.q.getNewStringTexts(self.corpusID))
        return self.readQuery(self.connectionData, 
                              self.q.getCountTableTexts())[0][0]
        #+ отправить команду на добавление строки непустой
        # считать id последней строки 
        # вернуть id
        
    
    def addDictionary(self):
        print("bdAddTexts")
        self.sendQuery(self.connectionData, 
                       self.q.getNewStringDictionary(self.corpusID))
        return self.readQuery(self.connectionData, 
                              self.q.getCountTableDictionary())[0][0]
        #+ отправить команду на добавление строки непустой
        # считать id последней строки 
        # вернуть id
    
    def addInfo(self):
        print("bdAddTexts")
        self.sendQuery(self.connectionData, 
                       self.q.getNewStringInfo(self.corpusID))
        return self.readQuery(self.connectionData, 
                              self.q.getCountTableInfo())[0][0]
        #+ отправить команду на добавление строки непустой
        # считать id последней строки 
        # вернуть id
        
    
    def updateTopicList(self, strName, strVal, stringID):
        print("dbUpdateTopicList: {0}, {1}, {2}".format(strName, strVal, stringID))
        self.sendQuery(self.connectionData, 
                       self.q.getUpdateTopicList(stringID, strName, strVal))
        #+ вызов метода добавления данных в таблицу topicList, по stringID
        
        
    def updateTexts(self, strName, strVal, stringID):
        print("dbUpdataTexts: {0}, {1}, {2}".format(strName, strVal, stringID))
        self.sendQuery(self.connectionData, 
                       self.q.getUpdateTexts(stringID, strName, strVal))
        #+ вызов метода добавления данных в таблицу texts, по stringID
    
    
    def updateDictionary(self, strName, strVal, stringID):
        print("dbUpdateDictionary: {0}, {1}, {2}".format(strName, strVal, stringID))
        self.sendQuery(self.connectionData, 
                       self.q.getUpdateDictionary(stringID, strName, strVal))
        #+ вызов метода добавления данных в таблицу dictionary, по stringID
        
        
    def updateInfo(self, strName, strVal, stringID):
        print("dbupdateInfo: {0}, {1}, {2}".format(strName, strVal, stringID))
        self.sendQuery(self.connectionData, 
                       self.q.getUpdateInfo(stringID, strName, strVal))
        #+ вызов метода добавления данных в таблицу topicList, по stringID
    
    
    def getTopicListData(self, strName, stringID):
        print("dbGetTopicListData: {0}".format(strName))
        return self.readQuery(self.connectionData, 
                              self.q.getDataTopicList(stringID, strName))
        #+ вызов метода получения данных из строки таблицы listData
        # вернуть strVal
    
    
    def getTextsData(self, strName, stringID):
        print("dbGetTextsData: {0}".format(strName))
        return self.readQuery(self.connectionData, 
                              self.q.getDataTexts(stringID, strName))
        #+ вызов метода получения данных из строки таблицы textsData
        # вернуть strVal
        
    
    def getDictionaryData(self, strName, stringID):
        print("dbGetDictionaryData: {0}".format(strName))
        return self.readQuery(self.connectionData, 
                              self.q.getDataDictionary(stringID, strName))
        #+ вызов метода получения данных из строки таблицы dictionaryData
        # вернуть strVal
    
    def getInfoData(self, strName, stringID):
        print("dbGetTextsData: {0}".format(strName))
        return self.readQuery(self.connectionData, 
                              self.q.getDataInfo(stringID, strName))
        #+ вызов метода получения данных из строки таблицы textsData
        # вернуть strVal
    
    
    def addTableTopicList(self, connection):
        print("dbAddTopicListTable")
        self.sendQuery(connection, self.q.getNewTableTopicList())
        #++вызов метода добавления таблицы с соответствующими столбцами
        
        
    def addTableTexts(self, connection):
        print("dbAddTextsTable")
        self.sendQuery(connection, self.q.getNewTableTexts())
        #++вызов метода добавления таблицы с соответствующими столбцами
        
        
    def addTableDictionary(self, connection):
        print("dbAddDictionaryTable")
        self.sendQuery(connection, self.q.getNewTableDictionary())
        #++вызов метода добавления таблицы с соответствующими столбцами
        
    def addTableInfo(self, connection):
        print("dbAddTableInfo")
        self.sendQuery(connection, self.q.getNewTableInfo())
        # вызов метода добавления таблицы с общей инфой о входных данных
        
        
    def getConnect(self, path):
        #++метод, выполняющий подключение к БД и 
        # формирующий объект с соединением к этой БД
        print("dbConnectCorpus")
        connection = None
        try:
            connection = sqlite3.connect(path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occured")
        return connection
        
        
    def sendQuery(self, connection, q):
        #+метод выполняющий конкретный запрос в БД
        print("dbSendQuery")
        tempStr = q
        print("q:")
        print(tempStr)
        cursor = connection.cursor()
        try:
            cursor.execute(q)
            connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occured")
    
    
    def readQuery(self, connection, q):
        #+метод, выполняющий запрос на чтение в БД
        print("dbReadQuery")
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(q)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occured")
    
    
    def newDataPath(self, oldPath, corpusID):
        print("dbNewDataPath")
        #+метод подменяет в старом пути к бд имя бд на новое имя (без .db)
        oldPath = oldPath.rsplit('/', maxsplit=1)
        return oldPath[0]+r'/'+corpusID
        
    
    def getCorpusID(self):
        return self.corpusID
    
    def getTopicListSize(self):
        return self.readQuery(self.connectionData, 
                              self.q.getCountTableTopicList())[0][0]
    
    def getTextsSize(self):
        return self.readQuery(self.connectionData, 
                              self.q.getCountTableTexts())[0][0]
    
    def getDictionarySize(self):
        return self.readQuery(self.connectionData, 
                              self.q.getCountTableDictionary())[0][0]
    
    def getInfoSize(self):
        return self.readQuery(self.connectionData, 
                              self.q.getCountTableInfo())[0][0]

if __name__ == '__main__':
    db = DbInteraction()
    qTest = DbQuery()
    connect1 = db.getConnect(r"/mnt/hgfs/vmware D/myCorpusDB/myCorpuses11.db")
    connect2 = db.getConnect(r"/mnt/hgfs/vmware D/myCorpusDB/myCorpuses12.db")
    db.sendQuery1(connect1, qTest.getNewTableDictionary())
    db.sendQuery1(connect2, qTest.getNewTableTopicList())
    db.sendQuery1(connect1, qTest.getNewTableTexts())
    