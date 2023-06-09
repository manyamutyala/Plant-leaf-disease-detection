# -*- coding: utf-8 -*-
"""Minor Project

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Oce3fsEIs7hU5bKsLfWCVKMdhPpHy7Jr
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator,img_to_array,load_img
from google.colab import drive

drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/MyDrive/Leaves Data

from keras.applications.vgg19 import VGG19,preprocess_input,decode_predictions
train_datagen = ImageDataGenerator(zoom_range = 0.5, shear_range = 0.3, horizontal_flip = True)
val_datagen = ImageDataGenerator(preprocessing_function = preprocess_input)

train=train_datagen.flow_from_directory(directory="/content/drive/MyDrive/Leaves Data/train",target_size=(256,256),batch_size=32)
val=val_datagen.flow_from_directory(directory="/content/drive/MyDrive/Leaves Data/valid",target_size=(256,256),batch_size=32)

t_img,label=train.next()

t_img.shape

def plotImage(img_arr,label):
  for im, l in zip(img_arr, label):
    plt.figure(figsize = (5, 5))
    plt.imshow(im)
    plt.show()

plotImage(t_img[:3],label[:3])

!pip install keras
from keras.layers import Dense,Flatten
from keras.models import Model
from tensorflow.keras.applications import VGG19

base_model = VGG19(input_shape = (256, 256, 3), include_top = False)

for layer in base_model.layers:
  layer.trainable = False

base_model.summary()

X=Flatten()(base_model.output)
X=Dense(units=8,activation='softmax')(X)

model=Model(base_model.input,X)

model.summary()

model.compile(optimizer='adam',loss = keras.losses.categorical_crossentropy, metrics = ['accuracy'])

from tensorflow.keras.callbacks import ModelCheckpoint,EarlyStopping
es=EarlyStopping(monitor='val_accuracy',min_delta=0.01,patience=3,verbose=1)
mc=ModelCheckpoint(filepath="/content/best_model.h5",
                   monitor='val_accuracy',
                   patience=3,
                   verbose=1,
                   save_best_only=True)
cb=[es,mc]

his = model.fit_generator(train,
                        steps_per_epoch=16,
                        epochs = 10,
                        verbose=1,
                        callbacks=cb,
                        validation_data=val,
                        validation_steps=16)

h = his.history
h.keys()

plt.plot(h['accuracy'])
plt.plot(h['val_accuracy'] , c = "red")
plt.title("acc vs v-acc")
plt.show()

plt.plot(h['loss'])
plt.plot(h['val_loss'], c = "red")
plt.title("loss vs v-loss")
plt.show()

#load best model
from keras.models import load_model
model = load_model("/content/best_model.h5")

acc = model.evaluate(val)[1]
print(f"The accuracy of your model is {acc*100} %")

def prediction(path):
  img = load_img(path, target_size = (256,256))
  i = img_to_array(img)
  im = preprocess_input(i)
  img = np.expand_dims(im, axis = 0)
  pred = np.argmax(model.predict(img))
  print(pred)

path = "/content/drive/MyDrive/Leaves Data/test/test/AppleCedarRust1.JPG"
prediction(path)

ref = dict(zip(list(train.class_indices.values()), list(train.class_indices.keys())))

def prediction(path):
  img = load_img(path, target_size = (256,256))
  i = img_to_array(img)
  im = preprocess_input(i)
  img = np.expand_dims(im, axis = 0)
  pred = np.argmax(model.predict(img))
  print("the image belongs to", ref[pred])

path = "/content/drive/MyDrive/Leaves Data/test/test/AppleScab1.JPG"
prediction(path)