from DbInteraction import DbInteraction
from Param import Param
from OpenTexts import OpenTexts
from CorpusParser import CorpusParser
from Dictionary import Dictionary
from Vectorizer import Vectorizer
from CorpusAnalyzer import CorpusAnalyzer
from utility import ProgressBar
from utility import Table
import time
import json
import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt
#%%


print('start')

t = time.localtime()
compilationTime = "{0}.{1}.{2} {3}:{4}".format(t.tm_year, t.tm_mon, 
                                               t.tm_mday, t.tm_hour, 
                                               t.tm_min)

p = Param() #инициализация класса с параметрами работы
p.printParam() #вывод списка параметров
db = DbInteraction() #иниц. класса для работы с БД
db.initFullAnalysis(p.readDBCorpusPath()) #иниц. класса для работы с БД
# отправка в него пути к БД
corpusID = db.getCorpusID() #сохранение актуального ID, который
# является индексом строки в БД
print("Добавление информации в базу данных...")
db.updateCorpus('name', p.readName(), corpusID) #добавление начальной инфо
# рмации о корпусе. данные считываются с параметров и отправляются
db.updateCorpus('language', p.readLanguage(), corpusID) #
db.updateCorpus('stemType', p.readStemType(), corpusID) #
db.updateCorpus('stopWordsType', p.readStopWordsType(), corpusID) #
db.updateCorpus('metric', p.readMetric(), corpusID) #
db.updateCorpus('compilationTime', compilationTime, corpusID)
db.updateCorpus('source', p.readSource(), corpusID)


db.addInfo()
db.updateInfo('name', p.readName(), 1) #добавление начальной инфо
# рмации о корпусе. данные считываются с параметров и отправляются
db.updateInfo('language', p.readLanguage(), 1)
db.updateInfo('stemType', p.readStemType(), 1)
db.updateInfo('stopWordsType', p.readStopWordsType(), 1)
db.updateInfo('metric', p.readMetric(), 1)
db.updateInfo('corpus_ID', corpusID, 1)
db.updateInfo('compilationTime', compilationTime, 1)
db.updateInfo('source', p.readSource(), 1)

   


analyzer = CorpusAnalyzer() # аналайзер дополняет БД оставшимися данными (на
# данный момент пока только списком категорий)
op = OpenTexts(p.readSource(), p.readDocCorpusPath()) # иниц. класса для 
# работы с исходными текстами

print("Открытие исходных текстов...")
while(op.hasNext()): # проверка на наличие следующего текста
    tempData = op.getNext() # извлечение базовой информации из 
    # файла, сохранение в словаре
    lastID = db.addTexts() # добавление новой строки в бд для 
    # информации по текстам и возврат её номера
    db.updateTexts('name', tempData['name'], lastID) # обновление 
    # данных в соответствующей строке
    db.updateTexts('topicName', tempData['topicName'], lastID) #
    db.updateTexts('baseText', tempData['baseText'], lastID) #
    
    analyzer.addTopicName(tempData['topicName'])
    db.updateTexts('topicNum', analyzer.getTopicNum(tempData['topicName']), lastID)
    # <- аналайзер необходим, для получения списка используемых топиков.
    # он запоминает имена топиков, присваивает им имена и, в данном месте,
    # отправляет имена в БД, для отчётности и для дальнейшего формирования
    # выходного вектора.


   
print("\nОбновление списка тем...")
for name, val, i in zip(analyzer.getList().keys(), 
                     analyzer.getList().values(),
                     range(analyzer.getNumOfTopics())):
    db.addTopicList() # добавление новой строки в бд для списка топиков
    db.updateTopicList('name', name, i+1)
    db.updateTopicList('topicNum', val, i+1)
    db.updateTopicList('numOfTexts', analyzer.getTopicCount(name), i+1)
    # <- обновление информации в таблице со списком топиков
    # общая информация, для отчетности
analyzer = None


print("Выполняется парсинг текстов...")
parser = CorpusParser(language = p.readLanguage(), 
                      stemType = p.readStemType(),
                      stopWordsType = p.readStopWordsType())
tempText = ''
pb = ProgressBar(maxValue=db.getTextsSize(),
                 suffix='обработано')
for i in range(db.getTextsSize()):
    tempText = db.getTextsData('baseText', i+1)[0][0]
    tempText = parser.parsing(tempText)
    db.updateTexts('formattedText', tempText, i+1)
    pb.inc()
# <- выполняется полный проход по всем сырым текстам в бд
# забираются сырые тексты, отправляются на очистку
# возвращаются тексты после фильтрации и отправляются в БД обратно
    
op = None
parser = None
# <- Очистка ненужных объектов (OpenTexts и CorpusParser)

print("Сохранение локальных словарей в базе данных...")
d = Dictionary(p.readMetric())
pb.new(maxValue=db.getTextsSize(), suffix='cохранено')
for i in range(db.getTextsSize()):
    d.addData(db.getTextsData('formattedText', i+1)[0][0])
    tempDict = d.getLastDictionary()
    tempStr = json.dumps(tempDict)
    tempStr = tempStr.replace('"', '""') 
    db.updateTexts('localDictionary', tempStr, i+1)
    pb.inc()
    # <- добавление в БД локальных словарей в виде json строки
d.idfGlobalCalc()

v = Vectorizer(p.readMetric())
v.addGlobDict(d.getGlobalDictionary())

if isinstance(p.readMaxFeatures(), int):
    d.reduceFeatures(p.readMaxFeatures())
    if (p.readMetric() == 'tfidf'):
        v.addIdfDict(d.getTfidfDict())

if p.saveDictionary() == True:
    print("Добавление глобального словаря в базу данных...")
    pb.new(maxValue=d.getGlobalSize(),
           suffix='добавлено')
    tempDict = d.getGlobalDictionary()
    idfTable = d.getAdditionalTable()
    for key, val in tempDict.items():
        lastID = db.addDictionary()
        db.updateDictionary('word', key, lastID)
        db.updateDictionary('value', val, lastID)
        db.updateDictionary('docCount', idfTable.getVal(key, "count"), lastID)
        pb.inc()
        # <- добавление глобального словаря в бд, целиком
        #!!! нужно пофиксить. работает слишком медленно
else:
    idfTable = d.getAdditionalTable()
  
inputSize = d.getGlobalSize()
outputSize = db.getTopicListSize()
corpusSize = db.getTextsSize()

db.updateCorpus('numOfTopics', outputSize, corpusID)
db.updateInfo('numOfTopics', outputSize, 1)
db.updateCorpus('numOfTexts', corpusSize, corpusID)
db.updateInfo('numOfTexts', corpusSize, 1)
db.updateCorpus('dictionarySize', inputSize, corpusID)
db.updateInfo('dictionarySize', inputSize, 1)
# <- обновление общей информации в БД (для отчетности)


print("Создание векторов текстов...")
pb.new(maxValue=corpusSize,
       suffix="обработано")
for i in range(corpusSize):
    tempStr = db.getTextsData('localDictionary', i+1)[0][0]
    tempDict = json.loads(tempStr)
    tempArray = v.getVecFromDict(tempDict)
    tempStr = json.dumps(tempArray)
    db.updateTexts('inputVector', tempStr, i+1)
    # <- инициализация векторизатора, отправка глобального словаря в 
    # него, извлечение из бд локального словаря, преобразование 
    # его из json-строки в стандартный словарь отправка словаря 
    # в векторизатор, получение массива преобразование массива 
    # в json-строку и отправка обратно в бд
    topicNum = db.getTextsData('topicNum', i+1)[0][0]
    db.updateTexts('outputVector', 
                   json.dumps(v.numToOutputVec(topicNum, outputSize)),
                   i+1)
    pb.inc()
    # <- извлечение номера топика для формирования входного вектора
    # и отправки этого вектора в БД
    
    
if p.saveDictionary() == True:
    print("Обновление глобального словаря...")
    tempDict = d.getGlobalDictionary()
    tfidfArray = d.getTfidfGlobal()
    idfArray = d.getIdfGlobal()
    pb.new(maxValue=d.getGlobalSize(),
           suffix='готово')
    for i in range(len(tfidfArray)):
        db.updateDictionary('tfidf', tfidfArray[i], i+1)
        db.updateDictionary('idf', idfArray[i], i+1)
        pb.inc()
        # <- добавление глобального словаря в бд, целиком
        #!!! нужно пофиксить. работает слишком медленно
d = None
v = None
# <- Очистка ненужных объектов (Dictionary и Vectorizer)

#%%
#!!! извлечение данных из генератора данных
print("Извлечение векторов из базы данных...")
c = db.getConnectionData()
ds = tf.data.Dataset.from_generator(
    db.generator(corpusSize, db.getDataCorpusName(), 'inputVector', 'outputVector'),
    output_types=(tf.float64, tf.float64),
    output_shapes=(tf.TensorShape((inputSize, )), tf.TensorShape((outputSize, ))))
    # <- использование генератора, который содержит весь набор данных и 
    # извлекает их, по необходимости

#%%
print("Фомирование данных для обучения...")
if p.shuffleData():
    ds = ds.shuffle(buffer_size=corpusSize,
                    reshuffle_each_iteration=False)
trainSize = int(corpusSize*p.getTrainPercentage()/100)
ds_train = ds.take(trainSize)
ds_val = ds.skip(trainSize)
ds = None
ds_train = ds_train.batch(30)
ds_val = ds_val.batch(30)

#%%
print("Создание нейросетевой модели...")
model = tf.keras.Sequential()

model.add(layers.Dense(inputSize, activation='relu'))
model.add(layers.Dense(100, activation='relu'))
model.add(layers.Dense(50, activation='relu'))
model.add(layers.Dense(outputSize, activation='softmax'))

model.compile(optimizer=tf.keras.optimizers.RMSprop(0.001),
              loss=tf.keras.losses.CategoricalCrossentropy(),
              metrics=[tf.keras.metrics.CategoricalAccuracy()])
#%%
print("Начало процесса обучения сети...")
startTime = time.time() 
history = model.fit(ds_train,
                    epochs=p.readEpochs(),
                    validation_data=ds_val)
endTime = time.time() 

#%%

print("Подготовка графиков...")
#summarize history for accuracy
plt.figure(figsize=(16, 10))
plt.plot(history.history['val_categorical_accuracy'])
plt.plot(history.history['categorical_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['val_categorical_accuracy', 'categorical_accuracy'], loc='upper left')
plt.grid(True)
plt.show()

#summarize history for loss
plt.figure(figsize=(16, 10))
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['loss', 'val_loss'], loc='upper left')
plt.grid(True)
plt.show()
print('Готово!')


#%% формируем выходные данные
print("Фомирование выходных данных...")
resultFull = json.dumps(history.history)
resultFull = resultFull.replace('"', '""') 
catAccArray = history.history['categorical_accuracy']
resultVal1 = json.dumps(catAccArray[len(catAccArray)-1]) 
valCatAccArray = history.history['val_categorical_accuracy']
resultVal2 = json.dumps(valCatAccArray[len(valCatAccArray)-1]) 
learningTime = json.dumps(endTime-startTime)
compilationTime2 = "{0}-{1}-{2} {3}-{4}".format(t.tm_year, t.tm_mon, 
                                               t.tm_mday, t.tm_hour, 
                                               t.tm_min)
nameOfSavedModel = "model_"+p.readName()+"_"+compilationTime2+".h5"
neuralNetworkStruct = json.dumps(nameOfSavedModel)
neuralNetworkStruct = neuralNetworkStruct.replace('"', '') 
model.save("savedModels/"+nameOfSavedModel)



#%% загружаем выходные данные в бд
print("Загрузка выходных данных в БД...")
db.updateCorpus('resultVal1', resultVal1, corpusID)
db.updateCorpus('resultVal2', resultVal2, corpusID)
db.updateCorpus('resultFull', resultFull, corpusID)
db.updateCorpus('learningTime', learningTime, corpusID)
db.updateCorpus('compilationTime', compilationTime, corpusID)
db.updateCorpus('neuralNetworkStruct', neuralNetworkStruct, corpusID)

print("Загрузка выходных данных в БД...")
db.updateInfo('resultVal1', resultVal1, 1)
db.updateInfo('resultVal2', resultVal2, 1)
db.updateInfo('resultFull', resultFull, 1)
db.updateInfo('learningTime', learningTime, 1)
db.updateInfo('compilationTime', compilationTime, 1)
db.updateInfo('neuralNetworkStruct', neuralNetworkStruct, 1)

