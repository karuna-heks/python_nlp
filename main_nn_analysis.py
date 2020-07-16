# -*- coding: utf-8 -*-
from DbInteraction import DbInteraction
from Param import Param
import time
import json
import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt

#%%


t = time.localtime()
compilationTime = "{0}.{1}.{2} {3}:{4}".format(t.tm_year, t.tm_mon, 
                                               t.tm_mday, t.tm_hour, 
                                               t.tm_min)

p = Param() #инициализация класса с параметрами работы

pathToDB = p.getPathToDBForReport()
db = DbInteraction() #иниц. класса для работы с БД
db.initNNAnalysis(pathToDB) # отправка в него пути к БД
db.addInfo() # добавить новую строку
actualNumberOfData = db.getInfoSize() # узнать номер последней строки


#%%
inputSize = db.getInfoData('dictionarySize', 1)[0][0]
outputSize = db.getInfoData('numOfTopics', 1)[0][0]
corpusSize = db.getInfoData('numOfTexts', 1)[0][0]


# цикличное извлечение данных из БД, добавление их в вектора    
inputArray = np.zeros((corpusSize, inputSize))
outputArray = np.zeros((corpusSize, outputSize))
for i in range(corpusSize):
    inputArray[i] = np.array(json.loads(
        db.getTextsData('inputVector', i+1)[0][0]))
    
    outputArray[i] = np.array(json.loads(
        db.getTextsData('outputVector', i+1)[0][0]))


ds = tf.data.Dataset.from_tensor_slices((inputArray, outputArray))

#%%

ds = ds.shuffle(buffer_size=corpusSize,
                reshuffle_each_iteration=True)
trainSize = int(corpusSize*p.getTrainPercentage()/100)
ds_train = ds.take(trainSize)
ds_val = ds.skip(trainSize)
ds = None

ds_train = ds_train.batch(30)
ds_val = ds_val.batch(30)

#%%

model = tf.keras.Sequential()

model.add(layers.Dense(inputSize, activation='relu'))
model.add(layers.Dense(20, activation='relu'))
model.add(layers.Dense(20, activation='relu'))
model.add(layers.Dense(outputSize, activation='softmax'))

model.compile(optimizer=tf.keras.optimizers.RMSprop(0.01),
              loss=tf.keras.losses.CategoricalCrossentropy(),
              metrics=[tf.keras.metrics.CategoricalAccuracy()])

startTime = time.time() 
history = model.fit(ds_train,
                    epochs=20,
                    validation_data=ds_val)
endTime = time.time() 
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


#%% формируем выходные данные
resultFull = json.dumps(history.history)
resultFull = resultFull.replace('"', '""') 
catAccArray = history.history['categorical_accuracy']
resultVal1 = json.dumps(catAccArray[len(catAccArray)-1]) 
# <- last model accuracy categorical_accuracy
valCatAccArray = history.history['val_categorical_accuracy']
resultVal2 = json.dumps(valCatAccArray[len(valCatAccArray)-1]) 
# <- last val accuracy val_categorical_accuracy
learningTime = json.dumps(endTime-startTime)
compilationTime2 = "{0}-{1}-{2} {3}-{4}".format(t.tm_year, t.tm_mon, 
                                               t.tm_mday, t.tm_hour, 
                                               t.tm_min)
nameOfSavedModel = "model_"+p.readName()+"_"+compilationTime2+".h5"
neuralNetworkStruct = json.dumps(nameOfSavedModel)
neuralNetworkStruct = neuralNetworkStruct.replace('"', '') 
model.save("savedModels/"+nameOfSavedModel)

#%% загружаем выходные данные в бд
db.updateInfo('resultVal1', resultVal1, actualNumberOfData)
db.updateInfo('resultVal2', resultVal2, actualNumberOfData)
db.updateInfo('resultFull', resultFull, actualNumberOfData)
db.updateInfo('learningTime', learningTime, actualNumberOfData)
db.updateInfo('compilationTime', compilationTime, actualNumberOfData)
db.updateInfo('neuralNetworkStruct', neuralNetworkStruct, actualNumberOfData)





