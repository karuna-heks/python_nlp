# -*- coding: utf-8 -*-

import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers

import numpy as np

import matplotlib.pyplot as plt
#%%



inputArray = np.zeros((10000, 2))
outputArray = np.zeros((10000, 10))
for i in range(10):
    num1 = np.random.random()*2-1
    num2 = np.random.random()*2-1
    for j in range(i*1000, i*1000+1000):
        inputArray[j][0] = num1 + (np.random.random()-1)*0.3
        inputArray[j][1] = num2 + (np.random.random()-1)*0.3
        outputArray[j][i] = 1
array = np.column_stack([inputArray, outputArray])

# fig, ax = plt.subplots()
# ax.stackplot(inputArray[:,0], inputArray[:,1])
# fig.tight_layout()
# plt.show()

#%%
plt.scatter(array[:,0], array[:,1], marker = 'o', s = 0.01)
plt.show()

     
#%%
np.random.shuffle(array)
        
#%%
model = tf.keras.Sequential()

model.add(layers.Dense(2, activation='relu'))

model.add(layers.Dense(2, activation='relu'))

model.add(layers.Dense(10, activation='softmax'))



model.compile(optimizer=tf.keras.optimizers.RMSprop(0.01),
              loss=tf.keras.losses.CategoricalCrossentropy(),
              metrics=[tf.keras.metrics.CategoricalAccuracy()])



results = model.fit(
    array[0:7000,:][:,0:2], 
    array[0:7000,:][:,2:12], 
    epochs=10, 
    batch_size=32,
    validation_data = (array[7000:10000,:][:,0:2],
                       array[7000:10000,:][:,2:12]))


#%%

colour = model.predict_classes(array[:,0:2])

#%%
plt.figure(figsize=(16, 10))
plt.scatter(array[:,0], array[:,1], marker = 'o', s = 0.1, c = colour)


