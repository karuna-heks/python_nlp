from DbInteraction import DbInteraction
from Param import Param
from OpenTexts import OpenTexts
from CorpusParser import CorpusParser
from Dictionary import Dictionary
from Vectorizer import Vectorizer
from CorpusAnalyzer import CorpusAnalyzer
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
db = DbInteraction() #иниц. класса для работы с БД
db.initFullAnalysis(p.readDBCorpusPath()) #иниц. класса для работы с БД
# отправка в него пути к БД
corpusID = db.getCorpusID() #сохранение актуального ID, который
# является индексом строки в БД
db.updateCorpus('name', p.readName(), corpusID) #добавление начальной инфо
# рмации о корпусе. данные считываются с параметров и отправляются
db.updateCorpus('language', p.readLanguage(), corpusID) #
db.updateCorpus('stemType', p.readStemType(), corpusID) #
db.updateCorpus('stopWordsType', p.readStopWordsType(), corpusID) #
db.updateCorpus('metric', p.readMetric(), corpusID) #
db.updateCorpus('compilationTime', compilationTime, corpusID)


db.addInfo()
db.updateInfo('name', p.readName(), 1) #добавление начальной инфо
# рмации о корпусе. данные считываются с параметров и отправляются
db.updateInfo('language', p.readLanguage(), 1)
db.updateInfo('stemType', p.readStemType(), 1)
db.updateInfo('stopWordsType', p.readStopWordsType(), 1)
db.updateInfo('metric', p.readMetric(), 1)
db.updateInfo('corpus_ID', corpusID, 1)
db.updateInfo('compilationTime', compilationTime, 1)

   

analyzer = CorpusAnalyzer() # аналайзер дополняет БД оставшимися данными

op = OpenTexts(p.readDocCorpusPath()) # иниц. класса для работы с исходными
# текстами
op.searchFolder() # выбор метода для своего типа исходных данных 
# (поиск папок с файлами, файлов с текстами или другой)  
# searchFolder, searchTxt, searchAlt
# !!! мб перенести выбор метода в json параметры. а внутри класса пусть
# сам определяет, какой метод надо использовать, на основе параметров 
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
    
   
    
for name, val, i in zip(analyzer.getList().keys(), 
                     analyzer.getList().values(),
                     range(analyzer.getNumOfTopics())):
    db.addTopicList() # добавление новой строки в бд для списка топиков
    db.updateTopicList('name', name, i+1)
    db.updateTopicList('topicNum', val, i+1)
    db.updateTopicList('numOfTexts', analyzer.getTopicCount(name), i+1)
    # <- обновление информации в таблице со списком топиков
    # общая информация, для отчетности
    

    
parser = CorpusParser(language = p.readLanguage(), 
                      stemType = p.readStemType(),
                      stopWordsType = p.readStopWordsType)
tempText = ''
for i in range(db.getTextsSize()):
    tempText = db.getTextsData('baseText', i+1)[0][0]
    tempText = parser.parsing(tempText)
    db.updateTexts('formattedText', tempText, i+1)
# <- выполняется полный проход по всем сырым текстам в бд
# забираются сырые тексты, отправляются на очистку
# возвращаются тексты после фильтрации и отправляются в БД обратно



d = Dictionary()
for i in range(db.getTextsSize()):
    d.addData(db.getTextsData('formattedText', i+1)[0][0])
    tempDict = d.getLastDictionary()
    tempStr = json.dumps(tempDict)
    tempStr = tempStr.replace('"', '""') 
    db.updateTexts('localDictionary', tempStr, i+1)
    # <- добавление в БД локальных словарей в виде json строки


if p.saveDictionary == True:
    tempDict = d.getGlobalDictionary()
    for key, val in tempDict.items():
        lastID = db.addDictionary()
        db.updateDictionary('word', key, lastID)
        db.updateDictionary('value', val, lastID)
        # <- добавление глобального словаря в бд, целиком
        #!!! нужно пофиксить. работает слишком медленно
   
    
  
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



v = Vectorizer()
v.addGlobDict(d.getGlobalDictionary())
for i in range(db.getTextsSize()):
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
    # <- извлечение номера топика для формирования входного вектора
    # и отправки этого вектора в БД
#%%
#!!! извлечение данных из генератора данных
c = db.getConnectionData()
ds = tf.data.Dataset.from_generator(
    db.generator(corpusSize, db.getDataCorpusName(), 'inputVector', 'outputVector'),
    output_types=(tf.float64, tf.float64),
    output_shapes=(tf.TensorShape((inputSize, )), tf.TensorShape((outputSize, ))))
    # <- использование генератора, который содержит весь набор данных и 
    # извлекает их, по необходимости

# def calculation(inputVector, outputVector):
#     print(inputVector)
#     print(outputVector)
#     print(len(inputVector))
#     data1 = np.array([json.loads(inputVector.eval()[0])])
#     data2 = np.array([json.loads(outputVector.eval()[0])])
#     print(data1)
#     print(data2)
#     return (inputVector, outputVector)
# ds = ds.shuffle(buffer_size=30, reshuffle_each_iteration=True)
# ds = ds.batch(32)
# ds = ds.map(calculation)
# for next_el in ds:
#     tf.print(next_el)
# a1 = aaa.numpy()

# a1 = aaa.numpy()[0]
# a2 = json.loads(a1)
# tf.dtypes.as_string    Tensor("args_0:0", dtype=float64)
    
#%%
# цикличное извлечение данных из БД, добавление их в вектора    
# inputArray = np.zeros((corpusSize, inputSize))
# outputArray = np.zeros((corpusSize, outputSize))
# for i in range(db.getTextsSize()):
#     inputArray[i] = np.array(json.loads(
#         db.getTextsData('inputVector', i+1)[0][0]))
    
#     outputArray[i] = np.array(json.loads(
#         db.getTextsData('outputVector', i+1)[0][0]))


# ds = tf.data.Dataset.from_tensor_slices((inputArray, outputArray))
# del inputArray
# del outputArray

#%%

ds = ds.shuffle(buffer_size=corpusSize,
                reshuffle_each_iteration=True)
trainSize = int(corpusSize*p.getTrainPercentage()/100)
ds_train = ds.take(trainSize)
ds_val = ds.skip(trainSize)
ds = None
ds_train = ds_train.batch(30)
ds_val = ds_val.batch(30)

# heh = 1
# for next_el in ds_train:
#     tf.print(next_el)
#     heh = next_el
# for next_el in ds_val:
#     tf.print(next_el)
#%%

model = tf.keras.Sequential()

model.add(layers.Dense(inputSize, activation='relu'))
model.add(layers.Dense(20, activation='relu'))
model.add(layers.Dense(20, activation='relu'))
model.add(layers.Dense(outputSize, activation='softmax'))

model.compile(optimizer=tf.keras.optimizers.RMSprop(0.01),
              loss=tf.keras.losses.CategoricalCrossentropy(),
              metrics=[tf.keras.metrics.CategoricalAccuracy()])
#%%
history = model.fit(ds_train,
                    epochs=20,
                    validation_data=ds_val)

#%%


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



