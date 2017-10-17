import pygame, sys, math
from pygame.locals import *


#COLORS
#Grayscale
WHITE = (255, 255, 255)
GREY = (192, 192, 192)
BLACK = (0,0,0)
#RGB
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)
#MIX
YELLOW = (255,255,0)
PURPLE = (255, 0, 255)
CYAN = (0,255,255)
ORANGE = (255, 165, 0)

#FPS initialization
FPS = 60 # frames per second setting
fpsClock = pygame.time.Clock()

displayWidth = 800
displayHeight = 600
def displayDimensions():
    return displayWidth, displayHeight

DISPLAYSURF = pygame.display.set_mode((displayWidth,displayHeight))#, pygame.FULLSCREEN)
pygame.display.set_caption('Driving Simluator')

gravity = [0,300]
forces = {}
forces["gravity"] = gravity
forces["normals"] = []
forces["ball"] = [0,0]
forces["cars"] = []
forces["driving"] = [0,0]
forces["boost"] = [0,0]
forces["friction"] = [0,0]
forces["airFriction"] = [0,0]
COF = 0.99 #coefficient of friction

torques = {}
#maxSpeed = ? for supersonic

#print(pygame.display.get_driver())
#if pygame.display.toggle_fullscreen():
    #print("yay")    

