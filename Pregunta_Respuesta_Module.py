# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 13:28:37 2021

@author: David Goñi Burgos
@Module: Módulo de búsqueda de preguntas y respuestas.
"""

from transformers import pipeline
import sys

### Modelo en Español
#https://huggingface.co/mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es

model_name = "./model/mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es"
classifier = pipeline('question-answering', model=model_name)

## Modelo de preguntas y respuestas basado en un contexto
def Model_analizer (question_, paragrahp_):
    
    result = classifier({'question': question_,'context': paragrahp_ },top_k=2,max_answer_len=50)

    # Si el modelo devuelve mas de una posibilidad se concatenan
    #if (len(result) > 1):
    #    result = result[0]['answer']+' o '+result[1]['answer']
    #else:
    #    result = result[0]['answer']
        
    return result[0]['answer']

def pregunta_respuesta(pregunta, contexto):
    model_response='No he encontrado nada'

    if contexto == '':
        model_response='No he encontrado nada'
    else:
        try:
            model_response = Model_analizer(pregunta, contexto)
            print(f"Respuesta del modelo sobre el contexto: {model_response}")
        except:
            print("Unexpected error:", sys.exc_info()[0]) 
    return model_response
