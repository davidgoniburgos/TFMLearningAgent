# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 19:04:36 2021

@author: David Goñi Burgos
@Extracted from: https://github.com/hiteshmishra708/python-chatbot/blob/main/train_bot.py
@Requirements: 
!pip install transformers
@Module: Modulo chatbot
"""
import nltk, json, random, pickle
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import numpy as np
from tensorflow.keras.models import load_model
from transformers import pipeline

#Added David
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
import re
#END Added

## Modelo NER
ner_model="./model/mrm8488/bert-spanish-cased-finetuned-ner"
nlp = pipeline("ner", model=ner_model)

model = load_model('./chatbot/chatbot_model.h5')
intents = json.loads(open('./chatbot/intents_personalizado.json',encoding="utf-8").read())
words = pickle.load(open('./chatbot/words.pkl','rb'))
classes = pickle.load(open('./chatbot/classes.pkl','rb'))

# Preprocesamiento input user
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# creación de bag of words
def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def calcula_prediccion(sentence, model):
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    #ERROR_THRESHOLD = 0.25
    #Se elimina el threshold para ver toda la matriz de posibilidades de los intents
    ERROR_THRESHOLD = 0
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        print("intent:", classes[r[0]], " probability:", str(r[1]))
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getRespuesta(ints, intents_json, entrada, oraculo, name, dialogFlow):
    result = ''
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    
    # Control de intents de ayuda con el nombre del oráculo al principio
    if(re.match(rf"^{re.escape(oraculo.lower())}\b(?!\w)",str(entrada).lower())):
      tag = 'ayuda'
    elif(tag == 'ayuda'):
      del ints[0]
      tag = ints[0]['intent']
    for i in list_of_intents:
        if(i['tag'] == tag):
          # Added David
          # Control del diálogo
          if (tag == 'minombre'):
            # Se extraen los NER
            # Extracción de NER por modelo preentrenado
            # B-PER denotes the beginning
            ner = nlp(entrada)
            print('NER:',ner)
            for entity in ner :
              if entity['entity'] == 'B-PER':
                name += re.sub('##', '', entity.get('word'))
            print('Nombre', name)
            result = random.choice(i['responses'])
            if name :
              result = re.sub('<name>', str(name).strip(), result)
            else:
              result = re.sub('<name>', '', result)
            print(result)
            break   
            # END Added
          
          if (tag == 'ayuda'):
              print('Modulo de búsqueda')    
              break
          result = random.choice(i['responses'])
          ##RESPUESTA CON EL NOMBRE DEL JUGADOR
          if name :
              result = re.sub('<name>', str(name).strip(), result)
          else:
              result = re.sub('<name>', '', result)
          break
    
    return result, name

def inicio_chatbot(msg, oraculo, name, dialogFlow):
    ints = calcula_prediccion(msg, model)
    res , name = getRespuesta(ints, intents, msg, oraculo, name, dialogFlow)
    return res, ints, name
