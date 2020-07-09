
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
        
# str1 = """string "string" string"""
# print(str1)
# str2 = str1.replace('"', '""')
# print(str2)

# path1 = "/mnt/hgfs/vmware D/topics/medicine/Medicine.txt"
# path2 = "/mnt/hgfs/vmware D/topics/animals/Worm.txt"
# path3 = "/mnt/hgfs/vmware D/topics/politic/coalition.txt"
# path4 = "/mnt/hgfs/vmware D/topics/politic/bureaucracy.txt"
# enc1 = "utf-16"
# enc2 = "utf-16le"
# enc3 = "utf-8"
# enc4 = "us-ascii"
# enc5 = "cp1251"
# f = open(path4, mode = "r", encoding = enc5)
# try: 
        
#     # tempText = f.read().decode("utf-16")
#     tempText = f.read()
#     tempText = tempText.replace('"', '""')
#     # <- прочитать текст, заменить символ " на "", для sqlite
# finally:
#     f.close()
# print(tempText)
    

d = {'a': 2, 'b': 43, 'c': 332}

for key, val, i in zip(d.keys(), d.values(), range(len(d))):
    print("key = {0}".format(key))
    print("val = {0}".format(val))
    print("i = {0}".format(i))



















