# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 12:40:17 2022

@author: David Goñi Burgos
TFE Inteligencia Artificial UNIR 2021-2022
"""

# IMPORT REQUIREMENTS


# MODULO PRINCIPAL

from Input_voice_module import escuchar
from Output_voice_module import hablar
from chatbot import inicio_chatbot
from Pregunta_Respuesta_Module import pregunta_respuesta
from KB_base_file_module import extraer_kb, extraer_contexto
from Dialog_flow_Module import siguiente_pregunta, calcular_acierto_pregunta, calcular_acierto_pregunta_fonetica, calcular_tfidf_doc

#Se deshabilitan los warnings
import logging
logging.basicConfig(level=logging.ERROR)
import random
import re

## INTRO APP
print ('Inicio de la APP')
print ('#####################################################################')
print ('######################   CHATBOT DE REPASO   ########################')
print ('#####################################################################')
print ('###  EL CHATBOT REALIZARA PREGUNTAS DE REPASO DEL TEMA DE CLASE  ####')
print ('#####################################################################')
print ('###         PUEDES PREGUNTALE COSAS AL CHATBOT DEL TEMA          ####')
print ('#####################################################################')
print ('###  DI ORACULO Y A CONTINUACION LA PREGUNTA QUE QUIERAS CONOCER  ###')
print ('#####################################################################')

## GESTION DEL DIALOGO
print('INTRO')
# Variable global del personaje y del oraculo??
oraculo = 'oráculo'
personaje = 'Ulises'
# Control del diálogo
dialogFlow = []

# Archivo de conocimiento
# TODO: Se importará de la documentación del profesor por el módulo de gestion del profesor
kb_file = './kb_files/grecia_training.json'
contextos, historys, historys_id, questions, answers =  extraer_contexto(extraer_kb(kb_file))
contextos_unicos = list(set(contextos))

def eliminar_digitos(respuesta_texto):
    texto_sin_digitos = re.sub(r'[0-9]+', '', respuesta_texto)
    print(texto_sin_digitos)
    return texto_sin_digitos
# Introducción del reto
introduccion = ['Hola aventurero de la historia, me llamo '+personaje+', tengo 12 años y vivo cerca de una bonita playa bañada por el mar mediterráneo en el mar Egeo',
                'Me he golpeado la cabeza cuando me zambullí en el agua, y ahora me duele mucho y no me acuerdo de casi nada.']
for intro in introduccion :
    print(intro)
    hablar(intro)

# Variable de 
usuario = ''
print('Para salir, di "salir"')
# Variable del nombre del jugador
name = ''

intro=True
# Identificador del flujo de preguntas
sig_pregunta_id = 0
preguntas_sin_responder = True

# Respuestas positivas:
opciones_acierto =['¡Enhorabuena!,','¡Genial!,','¡Así me gusta!, ','¡Muy bien!,']
# Respuestas erroneas
opciones_fallo = ['Casi, casi...','Huy..','Por poco...','La proxima seguro que aciertas...']
#Control de preguntas pendientes de responder por error
volver_a_realizar_pregunta_reto = True

# Flujo del chatbot
while usuario != 'salir':
    #Control de variables
    res = ''
    usuario = ''
    ints = []
    doc_id = -1

    
    if (preguntas_sin_responder):
        
        print('Pregunta reto: ',historys[historys_id.index(sig_pregunta_id)])
        hablar(historys[historys_id.index(sig_pregunta_id)])
        print('captura de audio')
        usuario = str(escuchar())
        
        # Identifia si hay dígitos en la respuesta para identificar mejor el intent
        usuario_sin_digitos = eliminar_digitos(usuario)
                
        # Flujo del Diálogo
        #res, ints , name  = inicio_chatbot(usuario, oraculo, name, dialogFlow)  
        res, ints , name  = inicio_chatbot(usuario_sin_digitos, oraculo, name, dialogFlow) 
        # Respuesta negativa del alumno a la pregunta
        if ints[0]['intent'] == 'negativo':
            #Se continua con el flujo respondiendo la respuesta.
            res = pregunta_respuesta(questions[historys_id.index(sig_pregunta_id)],contextos[historys_id.index(sig_pregunta_id)])
            #res , score = calcular_acierto_pregunta(answers,historys_id, sig_pregunta_id,usuario, pregunta_respuesta(questions[historys_id.index(sig_pregunta_id)],contextos[historys_id.index(sig_pregunta_id)]))
            dialogFlow.append({'intent':ints[0]['intent'],'entrada':usuario,'respuesta':res,'pregunta':{'id':sig_pregunta_id,'preg':'','res_preg':1}})
            res = "la respuesta es "+res
            #Se continua con el flujo de las preguntas
            sig_pregunta_id = siguiente_pregunta(dialogFlow)+1
            
        elif ints[0]['intent'] == 'ayuda':

            # Se elimina la palabra oraculo de la pregunta del usuario
            usuario = usuario.replace(oraculo, '')
            # Cuando se detecta la intención de solicitar información
            doc_id = calcular_tfidf_doc(usuario, contextos_unicos, oraculo)
            #print(doc_id)
            if(doc_id!= -1):
                #print(contextos_unicos[doc_id])
                res = pregunta_respuesta(usuario,contextos_unicos[doc_id])
            else:
                res = 'No he encontrado nada, lo siento no te puedo ayudar.'
            
        elif ints[0]['intent'] == 'norespuesta':
            # Se comprueba si es una respuesta a una de las preguntas            
            if usuario !='KO':
                #Se obtiene el score de la similitud del coseno entre 
                res , score = calcular_acierto_pregunta(answers,historys_id, sig_pregunta_id,usuario, pregunta_respuesta(questions[historys_id.index(sig_pregunta_id)],contextos[historys_id.index(sig_pregunta_id)]))
                if score > 0.3:
                    acierto = random.choice(opciones_acierto)
                    res = acierto+" la respuesta es "+res+"."
                    dialogFlow.append({'intent':ints[0]['intent'],'entrada':usuario,'respuesta':res,'pregunta':{'id':sig_pregunta_id,'preg':'','res_preg':1}})
                else:
                    #Se calcula el acierto por fonética
                    score_fonetico = calcular_acierto_pregunta_fonetica(usuario, res)
                    if score_fonetico > 0.3:
                        acierto = random.choice(opciones_acierto)
                        res = acierto+" la respuesta es "+res+"."
                    else:
                        fallo = random.choice(opciones_fallo)
                        res = fallo +" la respuesta es "+res+ "."
                    dialogFlow.append({'intent':ints[0]['intent'],'entrada':usuario,'respuesta':res,'pregunta':{'id':sig_pregunta_id,'preg':'','res_preg':1}})
                
                #Se continua con el flujo de las preguntas
                sig_pregunta_id = siguiente_pregunta(dialogFlow)+1
            else:
                hablar("¿Quires preguntar algo?, di Oráculo y la pregunta que quieras realizar.")
        
        # Si el alumno pregunta por la lección        
        elif ints[0]['intent'] == 'tema':
            # Se pregunta si quiere saber la lección
            print("¿Quieres que te diga la lección que vas a repasar?")
            hablar("¿Quieres que te diga la lección que vas a repasar?")
            usuario = str(escuchar())
            #res, ints , name  = inicio_chatbot(usuario, oraculo, name, dialogFlow)  
            res, ints , name  = inicio_chatbot(usuario_sin_digitos, oraculo, name, dialogFlow)  
            if ints[0]['intent'] == 'afirmativo':
                for tema in contextos_unicos:
                    for frase in tema.split('.'):
                        if frase != "":
                            hablar(frase)
            else:
                res ='¡Vale!'

        print(personaje, ':' , res)
        hablar(res)
        if usuario == 'salir':
            break
        
        #sig_pregunta_id = siguiente_pregunta(dialogFlow)+1

        if(sig_pregunta_id > max(historys_id)):
            preguntas_sin_responder = False
            print('Enhorabuena, has contestado a todas las preguntas.')
            print('Espero que te hayas divertido y hayas aprendido algo interesante.')
            print('Puedes seguir preguntándo al oráculo o salir.')
            hablar('Enhorabuena, has contestado a todas las preguntas.')
            hablar('Espero que te hayas divertido y hayas aprendido algo interesante.')
            hablar('Puedes seguir preguntándo al oráculo o salir.')
            
    else:

        #Se inicia conversación de chatbot o consultas
        print('captura de audio')
        usuario = str(escuchar())
        # Identifia si hay dígitos en la respuesta para identificar mejor el intent
        usuario_sin_digitos = eliminar_digitos(usuario)
        #res, ints, name  = inicio_chatbot(usuario, oraculo, name, dialogFlow)
        res, ints, name  = inicio_chatbot(usuario_sin_digitos, oraculo, name, dialogFlow)
        if ints[0]['intent'] == 'ayuda':
            # Se elimina la palabra oraculo de la pregunta del usuario
            usuario = usuario.replace(oraculo, '')
            # Cálculo del if-idf del doc más probable por consulta del usuario
            doc_id = calcular_tfidf_doc(usuario, contextos_unicos, oraculo)
            print(doc_id)
            if(doc_id!= -1):
                res = pregunta_respuesta(usuario,contextos_unicos[doc_id])
            else:
                res = 'No he encontrado nada, lo siento no te puedo ayudar.'
        # Si el alumno pregunta por la lección        
        elif ints[0]['intent'] == 'tema':
            # Se pregunta si quiere saber la lección
            print("¿Quieres que te diga la lección que vas a repasar?")
            hablar("¿Quieres que te diga la lección que vas a repasar?")
            usuario = str(escuchar())
            # Identifia si hay dígitos en la respuesta para identificar mejor el intent
            usuario_sin_digitos = eliminar_digitos(usuario)
            #res, ints , name  = inicio_chatbot(usuario, oraculo, name, dialogFlow)  
            res, ints , name  = inicio_chatbot(usuario_sin_digitos, oraculo, name, dialogFlow)  
            if ints[0]['intent'] == 'afirmativo':
                for tema in contextos_unicos:
                    for frase in tema.split('.'):
                        if frase != "":
                            hablar(frase)
            else:
                res ='¡Vale!'
        print(personaje,':' , res)
        hablar(res)
    