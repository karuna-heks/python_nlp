from DbInteraction import DbInteraction
from Param import Param
from Dictionary import Dictionary
from Vectorizer import Vectorizer
import time
import json
import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt
from utility import ProgressBar
from utility import Table

#%%




p = Param() #инициализация класса с параметрами работы
p.printParam() #вывод списка параметров

print('Инициализация...')
pathToDB = p.database.getPathForReport()
db = DbInteraction() #иниц. класса для работы с БД
db.initNNAnalysis(pathToDB) # отправка в него пути к БД
db.addInfo() # добавить новую строку
actualNumberOfData = db.getInfoSize() # узнать номер последней строки


#%%
t = time.localtime()
compilationTime = "{0}.{1}.{2} {3}:{4}".format(t.tm_year, t.tm_mon, 
                                               t.tm_mday, t.tm_hour, 
                                               t.tm_min)

#%%



print("Сохранение локальных словарей в базе данных...")
pb = ProgressBar(maxValue=db.getTextsSize(),
                 suffix='сохранено')
d = Dictionary(p.featureExtraction.getMetricType(),
               p.featureExtraction.getNgrammType(),
               p.featureExtraction.getIgnoreWordOrderStatus())
for i in range(db.getTextsSize()):
    d.addData(db.getTextsData('formattedText', i+1)[0][0])
    tempDict = d.getLastDictionary()
    tempStr = json.dumps(tempDict)
    tempStr = tempStr.replace('"', '""') 
    db.updateTexts('localDictionary', tempStr, i+1)
    pb.inc()
    # <- добавление в БД локальных словарей в виде json строки
d.idfGlobalCalc()

v = Vectorizer(p.featureExtraction.getMetricType())
v.addGlobDict(d.getGlobalDictionary())

if isinstance(p.featureExtraction.getMaxFeatures(), int):
    d.reduceFeatures(p.featureExtraction.getMaxFeatures())
    if (p.featureExtraction.getMetricType() == 'tfidf'):
        v.addIdfDict(d.getTfidfDict())

if p.database.getSaveDictionaryStatus() == True:
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

db.updateInfo('numOfTopics', outputSize, actualNumberOfData)
db.updateInfo('numOfTexts', corpusSize, actualNumberOfData)
db.updateInfo('dictionarySize', inputSize, actualNumberOfData)
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
    
    
if p.database.getSaveDictionaryStatus() == True:
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
# d = None
# v = None
# <- Очистка ненужных объектов (Dictionary и Vectorizer)












inputSize = db.getInfoData('dictionarySize', 1)[0][0]
outputSize = db.getInfoData('numOfTopics', 1)[0][0]
corpusSize = db.getInfoData('numOfTexts', 1)[0][0]

#%% 
print("Извлечение векторов из базы данных...")
c = db.getConnectionData()
ds = tf.data.Dataset.from_generator(
    db.generator(corpusSize, db.getDataCorpusName(), 'inputVector', 'outputVector'),
    output_types=(tf.float64, tf.float64),
    output_shapes=(tf.TensorShape((inputSize, )), tf.TensorShape((outputSize, ))))

#%%
print("Фомирование данных для обучения...")
if p.neuralNetwork.getShuffleStatus():
    ds = ds.shuffle(buffer_size=corpusSize,
                    reshuffle_each_iteration=False)
trainSize = int(corpusSize*p.neuralNetwork.getTrainPercentage()/100)
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

model.compile(optimizer=tf.keras.optimizers.Adam(0.001),
              loss=tf.keras.losses.CategoricalCrossentropy(),
              metrics=[tf.keras.metrics.CategoricalAccuracy()])

print("Начало процесса обучения сети...")
startTime = time.time() 
history = model.fit(ds_train,
                    epochs=p.neuralNetwork.getEpochs(),
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
nameOfSavedModel = "model_"+p.getName()+"_"+compilationTime2+".h5"
neuralNetworkStruct = json.dumps(nameOfSavedModel)
neuralNetworkStruct = neuralNetworkStruct.replace('"', '') 
model.save("savedModels/"+nameOfSavedModel)

#%% загружаем выходные данные в бд
print("Загрузка выходных данных в БД...")
db.updateInfo('resultVal1', resultVal1, actualNumberOfData)
db.updateInfo('resultVal2', resultVal2, actualNumberOfData)
db.updateInfo('resultFull', resultFull, actualNumberOfData)
db.updateInfo('learningTime', learningTime, actualNumberOfData)
db.updateInfo('compilationTime', compilationTime, actualNumberOfData)
db.updateInfo('neuralNetworkStruct', neuralNetworkStruct, actualNumberOfData)





