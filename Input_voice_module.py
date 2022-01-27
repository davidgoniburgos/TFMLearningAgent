# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 12:11:03 2021

@author: David Goñi Burgos
@Module: Input voice from mic to text
"""
import speech_recognition as sr


def escuchar():
    r = sr.Recognizer() 
    text = ''
    audio = ''
    with sr.Microphone() as source:
        print('Di algo : ')
        audio = r.listen(source)
    
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            text = r.recognize_google(audio,language="es-ES")
            print('Has dicho: {}'.format(text))
            if text == 'salir':
                print('Se sale de la aplicación: {}'.format(text))
        except:
            text = 'KO'
            print('Perdona no te he entendido')

    return text
    
