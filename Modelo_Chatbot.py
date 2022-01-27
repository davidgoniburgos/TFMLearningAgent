# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 19:04:19 2021

@author: David Goñi Burgos
@Module: Entrenamiento del chatbot
@Extracted from: https://github.com/hiteshmishra708/python-chatbot/blob/main/train_bot.py
@Requirements:
!pip install tensorflow 
!pip install keras 
!pip install pickle 
!pip install nltk
"""
import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

import json
import pickle

import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()
words = []
classes = []
documents = []
ignore_words = ['?', '!']
data_file = open('./chatbot/intents.json', 'r',encoding="utf-8").read()
intents = json.loads(data_file)

# Definición del personaje del chatbot para el entrenamiento
# TODO: Estas variables entrarán desde el módulo de gestión del profesor
oraculo = 'oráculo'
personaje = 'Ulises' 
# se remplaza el nombre definido por en la cadena <personaje>
# se remplaza el nombre definido por en la cadena <oraculo>
#Convert to string and replace
obj_str = json.dumps(intents).replace('<personaje>', personaje)
obj_str = obj_str.replace('<oraculo>', oraculo)

#Get obj back with replacement
intents = json.loads(obj_str)
# se guardan los intents personalizados
with open('./chatbot/intents_personalizado.json', 'w',encoding="utf-8") as outfile:
    json.dump(intents, outfile)
print(intents)

# intents: grupo de conversación tipo
# patterns: posibilidades de interacción del usuario
for intent in intents['intents']:
    for pattern in intent['patterns']:

        # tokenización de cada palabra
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        # se agrega a a matriz de documentos
        documents.append((w, intent['tag']))
        print(w,intent['tag'])
        # se añaden clases a nuestra lista de clases
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]

pickle.dump(words, open('./chatbot/words.pkl','wb'))
pickle.dump(classes, open('./chatbot/classes.pkl','wb'))

# Preparación del entrenamiento de la red
training = []
output_empty = [0] * len(classes)
for doc in documents:
    # bag of words
    bag = []
    # lista de tokens
    pattern_words = doc[0]
    # lemmatización de token
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    # se la palabra coincide se inserta 1 sino 0
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

training = np.array(training)
# creación de conjunto de pruebas y de test: X - patterns, Y - intents
train_x = list(training[:,0])
train_y = list(training[:,1])

# creación de la arquitectura de la red
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))#128
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))#64
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# entrenamiento y guardado del modelo
hist = model.fit(np.array(train_x), np.array(train_y), epochs=300, batch_size=15, verbose=1)#epochs =300 batch_size=5
model.save('./chatbot/chatbot_model.h5', hist)
print("model created")
from matplotlib import pyplot as plt

plt.plot(hist.history['accuracy'])
#plt.plot(hist.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

plt.plot(hist.history['loss'])
#plt.plot(hist.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

