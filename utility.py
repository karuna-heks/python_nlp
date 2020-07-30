"""
v0.2.8

Доступные утилиты:
    - класс ProgressBar 
    - функция quickProgressBar
    - класс Table с удобной таблицей для добавления и извлечения данных по 
    паре ключей (ключ-строка, ключ-столбец)

Добавить:
    - функция для вывода данных со сдвигом каретки
    - описание классов, методов и функций
    - в таблице учесть:
        - количество столбцов (если их так много, что они не помещаются все
        на одном экране, то печатать больше одной таблицы)
        - длину слов (если хотя бы одно слово длиннее чем 20 символов, то
        увеличить доступную ширину стобца). в идеале сделать изменение ширины
        столбца в зависимости от ширины самого большого слова в столбце
        - добавить итератор, чтобы можно было её использовать в циклах,
        например for rowName, column1, column2 in Table:
"""
import sys

"""
ProgressBar 
"""
class ProgressBar:
    
    def __init__(self, maxValue:int, suffix:str='', barLen:int=40,
                 startCount:int=0):
        self._max = maxValue
        self._suffix = suffix
        self._count = startCount
        self._startCount = startCount
        self._barLen = barLen
    
    def inc(self, incVal:int=1):
        self._count += incVal
        filledLen = int(round(self._barLen*self._count/float(self._max)))
    
        percents = round(100.0*self._count/float(self._max), 1)
        bar = '=' * filledLen + '-' * (self._barLen - filledLen)
    
        sys.stdout.write('\r[%s] %s%s ...%s' % (bar, percents, '%', 
                                                self._suffix))
        sys.stdout.flush()
        if self._count == self._max:
            print("\n")
    
    def restart(self):
        self._count = self._startCount
        
    def new(self, maxValue:int, suffix:str='', barLen:int=40,
                 startCount:int=0):
        self._max = maxValue
        self._suffix = suffix
        self._count = startCount
        self._startCount = startCount
        self._barLen = barLen
        
        
def quickProgressBar(maxValue:int, suffix:str, count:int):
    barLen = 40
    count += 1
    filledLen = int(round(barLen * count / float(maxValue)))
    percents = round(100.0 * count / float(maxValue), 1)
    bar = '=' * filledLen + '-' * (barLen - filledLen)
    sys.stdout.write('\r[%s] %s%s ...%s' % (bar, percents, '%', suffix))
    sys.stdout.flush()



"""
Table
"""
class Table:
    # _dictionary = {}
    # _keysColumn = {}
    # _columnsCounter = 0
    
    def __init__(self, columnsList:list):
        self._dictionary = {}
        self._columnsCounter = 0
        self._keysColumn = {}
        for i in columnsList:
            if isinstance(i, str):
                self._keysColumn[i] = self._columnsCounter
                self._columnsCounter += 1
            else:
                sys.exit("Error: keys must be str")
            
    
    def setVal(self, keyRow:str, keyColumn:str, value):
        if self._dictionary.get(keyRow) == None:
            self._dictionary[keyRow] = [None]*self._columnsCounter
        self._dictionary[keyRow][self._keysColumn[keyColumn]] = value
    
    def getVal(self, keyRow:str, keyColumn:str):
        return self._dictionary[keyRow][self._keysColumn[keyColumn]]
    
    def getRow(self, keyRow:str):
        return self._dictionary.get(keyRow)
    
    def popRow(self, keyRow:str):
        return self._dictionary.pop(keyRow)
    
    def getRows(self):
        return self._dictionary.keys()
    
    def getColumns(self):
        return self._keysColumn.keys()
    
    def printTable(self):
        print("")
        for i in range(self._columnsCounter+1):
            print ("{:-<20}".format("-"), end = "--")
        print("")
        print("{:<20}".format("Result table"), end = "| ")
        for i in self._keysColumn.keys():
            print ("{:<20}".format(i), end = "| ")
        print("")
        for i in range(self._columnsCounter+1):
            print ("{:-<20}".format("-"), end = "+ ")
        print("")
        for i in self._dictionary.keys():
            print("{:<20}".format(i), end = "| ")
            for j in self._dictionary[i]:
                print("{:<20}".format(j), end = "| ")
            print("")
        
        
  


if __name__ == '__main__':
    import time
    pb = ProgressBar(20, suffix='completed')
    for i in range(20):
        pb.inc()
        time.sleep(0.01)
    print('\n')
    for i in range(20):
        quickProgressBar(20, 'завершено', i)
        time.sleep(0.01)
    print('\n')
        
    t = Table(["name", "age", "sex"])
    t.setVal("a", "name", "Karlomanochevikus")
    # t.setVal("a", "name", "Karlom")
    t.setVal("a", "age", 15)
    t.setVal("a", "sex", "male")
    t.setVal("b", "name", "Susan")
    t.setVal("b", "age", 35)
    t.setVal("b", "sex", "female")
    
    print(t.getVal("a", "age"))
    print(t.getVal("b", "name"))
    print(t.getVal("b", "age"))
    print(t.getVal("a", "sex"))
    print(t.getVal("b", "sex"))
    print(t.getVal("a", "name"))
    
    print(t.getRows())
    print(t.getColumns())
    
    t.printTable()
    
    
    # print(t.popRow("a"))
    # print(t.popRow("a"))
    
    
    
    
    