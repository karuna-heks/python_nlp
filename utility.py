"""
v0.1.4

Доступные утилиты:
    - класс ProgressBar 
    - функция quickProgressBar

Добавить:
    - функция для вывода данных со сдвигом каретки
    - описание методов и функций
"""
import sys

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


if __name__ == '__main__':
    import time
    pb = ProgressBar(500, suffix='completed')
    for i in range(500):
        pb.inc()
        time.sleep(0.01)
    print('\n')
    for i in range(500):
        quickProgressBar(500, 'завершено', i)
        time.sleep(0.01)
    
    
    
    