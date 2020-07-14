# -*- coding: utf-8 -*-

import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers

import numpy as np

import matplotlib.pyplot as plt

#%%

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

ds = tf.data.Dataset.from_tensor_slices((inputArray, outputArray))
# dso = tf.data.Dataset.from_tensor_slices(outputArray)
# ds = tf.data.Dataset.zip((dsi, dso))



#%%



# fig, ax = plt.subplots()
# ax.stackplot(inputArray[:,0], inputArray[:,1])
# fig.tight_layout()
# plt.show()

#%%
plt.scatter(inputArray[:,0], inputArray[:,1], marker = 'o', s = 0.01)
plt.show()

     
#%%
# np.random.shuffle(array)
ds = ds.shuffle(buffer_size=10000,
                reshuffle_each_iteration=True)
ds = ds.batch(10)
ds

#%%
# n,line_batch = next(iter(ds))
# print(n.numpy())
        
#%%
model = tf.keras.Sequential()

model.add(layers.Dense(2, activation='relu'))
model.add(layers.Dense(10, activation='relu'))
model.add(layers.Dense(10, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))



model.compile(optimizer=tf.keras.optimizers.RMSprop(0.01),
              loss=tf.keras.losses.CategoricalCrossentropy(),
              metrics=[tf.keras.metrics.CategoricalAccuracy()])



results = model.fit(ds, epochs=20)


#%%

colour = model.predict_classes(inputArray[:,0:2])

#%%
plt.figure(figsize=(16, 10))
plt.scatter(inputArray[:,0], inputArray[:,1], marker = 'o', s = 0.5, c = colour, cmap = 'gist_rainbow_r')


