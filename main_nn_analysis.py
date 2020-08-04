from DbInteraction import DbInteraction
from Param import Param
import time
import json
import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt

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





