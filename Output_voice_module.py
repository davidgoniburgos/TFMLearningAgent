# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 21:11:08 2021

@author: David Goñi Burgos
@Module: output text to voice
"""
from gtts import gTTS
from  pygame import mixer
import os


# It's just a text to speech function.
def hablar(somethingToSay):
    file ='audio/somethingToSay.mp3'
    if(os.path.exists(file)):
        os.remove(file)
    if somethingToSay != '':    
        myobj = gTTS(text=somethingToSay, lang="es", slow=False)
        myobj.save(file)
        mixer.init()
        mixer.music.load(file)
        mixer.music.set_volume(1)
        mixer.music.play()
        mixer.music.get_endevent()
        while mixer.music.get_busy():
            continue   
        mixer.music.unload()
        mixer.stop()
        os.remove(file)
    return True

