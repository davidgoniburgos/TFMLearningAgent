# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 16:31:52 2022

@author: David Goñi Burgos
@Module: Interfaz App
TFE Inteligencia Artificial UNIR 2021-2022

https://github.com/Patataman/PythonBasic/tree/master/frameworks/pygame
"""

#Necesario para las teclas presionadas
from pygame.locals import *

#Import del paquete
import pygame
import sys

#Inicializamos pygame
pygame.init()

''' Se utiliza la clase display para todo
    lo relacionado con las ventanas.
    https://www.pygame.org/docs/ref/display.html
'''
#Establecemos el tamaño de la ventana.
ventana = pygame.display.set_mode((800,600))
#https://www.iconspng.com/image/79510/acropolis
bg = pygame.image.load("images/bg_acropolis.png")


FONT = pygame.font.Font(None, 32)
clock = pygame.time.Clock()
input_box = pygame.Rect(100, 100, 140, 32)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
color = COLOR_INACTIVE

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, ventana):
        # Blit the text.
        ventana.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(ventana, self.color, self.rect, 2)


    
#podemos ponerle titulo a nuestra ventana, entre otras cosas,
#icono, que sea redimensionable...
pygame.display.set_caption("Aventureros de la historia")

def main():
    
    clock = pygame.time.Clock()
    input_box1 = InputBox(20, 300, 140, 32,'Gestión de Documentos Profesor')
    input_box2 = InputBox(60, 400, 140, 32,'Entrenamiento Chatbot (press e)')
    input_box3 = InputBox(100, 500, 140, 32,'Iniciar Chatbot (press c)')
    input_boxes = [input_box1, input_box2, input_box3]
    #done = False
    
    #Bucle de "Juego"
    while True:

        for event in pygame.event.get():    #Cuando ocurre un evento...
            if event.type == pygame.QUIT:   #Si el evento es cerrar la ventana
                pygame.quit()               #Se cierra pygame
                sys.exit()                  #Se cierra el programa
                
            #Cuando el evento es presionar una tecla...
            if event.type == pygame.KEYDOWN:
                #Obtenemos el mapping de teclas presionadas
                keys = pygame.key.get_pressed()
                if keys[K_s]:
                    #Rellenamos la ventana con un color de Pygame
                    pygame.quit()               #Se cierra pygame
                    sys.exit()                  #Se cierra el programa
                if keys[K_e]:
                    fn='./Modelo_Chatbot.py'
                    exec(open(fn).read(), globals())  #Ejecutamos chatbot
                if keys[K_c]:
                    #execfile(r'./main.py')  #Ejecutamos chatbot
                    fn='./main.py'
                    exec(open(fn).read(), globals())
            
        for box in input_boxes:
            box.update()

        ventana.fill((30, 30, 30))
        # Imagen background
        ventana.blit(bg, (0,0))
        for box in input_boxes:
            box.draw(ventana)

        pygame.display.flip()               #Genera la ventana
        clock.tick(30)
        
        

if __name__ == '__main__':
    main()
    pygame.quit()