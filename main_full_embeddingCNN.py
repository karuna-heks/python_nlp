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
import sys
#%%


print('start')

t = time.localtime()
compilationTime = "{0}.{1}.{2} {3}:{4}".format(t.tm_year, t.tm_mon, 
                                               t.tm_mday, t.tm_hour, 
                                               t.tm_min)

p = Param() #инициализация класса с параметрами работы
p.printParam() #вывод списка параметров
db = DbInteraction() #иниц. класса для работы с БД
db.initFullAnalysis(p.database.getDbCorpusPath()) #иниц. класса для работы с БД
# отправка в него пути к БД
corpusID = db.getCorpusID() #сохранение актуального ID, который
# является индексом строки в БД
print("Добавление информации в базу данных...")
db.updateCorpus('name', p.getName(), corpusID) #добавление начальной инфо
# рмации о корпусе. данные считываются с параметров и отправляются
db.updateCorpus('language', p.parser.getLanguage(), corpusID) #
db.updateCorpus('stemType', p.parser.getStemType(), corpusID) #
db.updateCorpus('stopWordsType', p.parser.getStopWordsType(), corpusID) #
db.updateCorpus('metric', p.featureExtraction.getMetricType(), corpusID) #
db.updateCorpus('compilationTime', compilationTime, corpusID)
db.updateCorpus('source', p.source.getCorpusName(), corpusID)


db.addInfo()
db.updateInfo('name', p.getName(), 1) #добавление начальной инфо
# рмации о корпусе. данные считываются с параметров и отправляются
db.updateInfo('language', p.parser.getLanguage(), 1)
db.updateInfo('stemType', p.parser.getStemType(), 1)
db.updateInfo('stopWordsType', p.parser.getStopWordsType(), 1)
db.updateInfo('metric', p.featureExtraction.getMetricType(), 1)
db.updateInfo('corpus_ID', corpusID, 1)
db.updateInfo('compilationTime', compilationTime, 1)
db.updateInfo('source', p.source.getCorpusName(), 1)




analyzer = CorpusAnalyzer() # аналайзер дополняет БД оставшимися данными (на
# данный момент пока только списком категорий)
op = OpenTexts(p.source.getCorpusName(), p.source.getCorpusPath()) 
# <- иниц. класса для работы с исходными текстами

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

#%%
print("Выполняется парсинг текстов...")
parser = CorpusParser(language = p.parser.getLanguage(), 
                      stemType = 'lemma',
                      stopWordsType = p.parser.getStopWordsType(),
                      ngram = 'unigram')
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
    
# op = None
# parser = None
# <- Очистка ненужных объектов (OpenTexts и CorpusParser)



if p.featureExtraction.getMetricType() == 'emb':
    sys.exit("Error: This source file only supports emb")

#%%
    
print("Создание векторов текстов...")

outputSize = db.getTopicListSize()
corpusSize = db.getTextsSize()
v = Vectorizer('embm')

pb.new(maxValue=db.getTextsSize(),
         suffix='создано')
for i in range(corpusSize):
    tempText = db.getTextsData('formattedText', i+1)[0][0]
    tempVector = v.embPreprocess(p.featureExtraction.getMaxSequence(), 
                                 tempText.split(' '))
    db.updateTexts('inputVector', json.dumps(tempVector.tolist()), i+1)
# <- выполняется открытие исходных текстов, представление его в виде
# вектора, преобразование в json-список. отправка в БД
    topicNum = db.getTextsData('topicNum', i+1)[0][0]
    db.updateTexts('outputVector', 
               json.dumps(v.numToOutputVec(topicNum, outputSize)),
               i+1)
    pb.inc()




#%%
#!!! извлечение данных из генератора данных
print("Извлечение векторов из базы данных...")
c = db.getConnectionData()
ds = tf.data.Dataset.from_generator(
    db.generator(corpusSize, db.getDataCorpusName(), 
                 'inputVector', 'outputVector', 'emb'),
    output_types=(tf.float64, tf.float64),
    output_shapes=(tf.TensorShape((p.featureExtraction.getMaxSequence(),300,1)), 
                   tf.TensorShape((outputSize))))
    # <- использование генератора, который содержит весь набор данных и 
    # извлекает их, по необходимости
    # (1, seqLen, embDimension), (seqLen, embDimension)
    # tf.TensorShape((seqLen*embDimension, ))
    # 
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
# model = tf.keras.Sequential()
# model.add(layers.Conv2D(128, 
#                         (3,300), 
#                         input_shape=(p.featureExtraction.getMaxSequence(), 300, 1)))

# l1 = layers.Conv2D(32,
#                     (3,300),
#                     input_shape=(p.featureExtraction.getMaxSequence(), 300, 1))
# l2 = layers.Conv2D(32,
#                     (4,300),
#                     input_shape=(p.featureExtraction.getMaxSequence(), 300, 1))
# l3 = layers.Conv2D(32,
#                     (5,300),
#                     input_shape=(p.featureExtraction.getMaxSequence(), 300, 1))
# l = layers.Concatenate()([l1, l2, l3])
# model.add(l)


# model.add(layers.Activation("relu"))
# # model.add(layers.MaxPooling2D(pool_size=(2,1)))

# # model.add(layers.Conv2D(32, (5,5)))
# # model.add(layers.Activation("relu"))
# # model.add(layers.MaxPooling2D(pool_size=(2,2)))

# model.add(layers.Flatten())
# model.add(layers.Dense(128, activation='relu'))
# model.add(layers.Dense(128, activation='relu'))

# model.add(layers.Dense(outputSize, 'softmax'))

# inputFlow = layers.Input(shape=(p.featureExtraction.getMaxSequence(), 300, 1))
# x = layers.Conv2D(64,
#                   (3,300),
#                   input_shape=(p.featureExtraction.getMaxSequence(), 300, 1)
#                   )(inputFlow)
# x = layers.Activation("relu")(x)
# x = layers.Flatten()(x)
# x = layers.Dense(64, activation='relu')(x)
# x = layers.Dense(outputSize, 'softmax')(x)
# model = tf.keras.Model(inputs=inputFlow, outputs=x)

inputFlow = layers.Input(shape=(p.featureExtraction.getMaxSequence(), 300, 1))
l1 = layers.Conv2D(
                    8,
                    (1,300),
                    input_shape=(p.featureExtraction.getMaxSequence(), 300, 1)
                    )(inputFlow)
l1 = layers.Activation('relu')(l1)
l1 = layers.Flatten()(l1)

l2 = layers.Conv2D(
                    8,
                    (2,300),
                    input_shape=(p.featureExtraction.getMaxSequence(), 300, 1)
                    )(inputFlow)
l2 = layers.Activation('relu')(l2)
l2 = layers.Flatten()(l2)

l3 = layers.Conv2D(
                    8,
                    (3,300),
                    input_shape=(p.featureExtraction.getMaxSequence(), 300, 1)
                    )(inputFlow)
l3 = layers.Activation('relu')(l3)
l3 = layers.Flatten()(l3)

l4 = layers.Conv2D(
                    8,
                    (4,300),
                    input_shape=(p.featureExtraction.getMaxSequence(), 300, 1)
                    )(inputFlow)
l4 = layers.Activation('relu')(l4)
l4 = layers.Flatten()(l4)

l5 = layers.Conv2D(
                    8,
                    (5,300),
                    input_shape=(p.featureExtraction.getMaxSequence(), 300, 1)
                    )(inputFlow)
l5 = layers.Activation('relu')(l5)
l5 = layers.Flatten()(l5)

x = layers.concatenate([l1, l2, l3, l4, l5])
x = layers.Dense(96, activation='relu')(x)
x = layers.Dense(outputSize, 'softmax')(x)

model = tf.keras.Model(inputs=inputFlow, outputs=x)
model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=[tf.keras.metrics.CategoricalAccuracy()])


#%%
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
nameOfSavedModel = "model_"+p.getName()+"_"+compilationTime2+".h5"
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

