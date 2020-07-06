
import sqlite3
from sqlite3 import Error
from DbQuery import DbQuery




def addTableTopicList(connection, query):
        print("dbAddTopicListTable")
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")
        #вызов метода добавления таблицы с соответствующими столбцами
            
            
            
def getQuery():
    return """INSERT INTO TopicList DEFAULT VALUES;"""
    
    
    
    
def connectCorpus(path):
    print("dbConnectCorpus")
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occured")
    return connection


def newDataPath(oldPath, corpusID):
    oldPath = oldPath.rsplit('/', maxsplit=1)
    return oldPath[0]+r'/'+corpusID


# c = connectCorpus(r"/mnt/hgfs/vmware D/myCorpusDB/myCorpuses12.db")
# q = DbQuery()
# addTableTopicList(c, getQuery())
        
str1 = """string "string" string"""
print(str1)
str2 = str1.replace('"', '""')
print(str2)




















