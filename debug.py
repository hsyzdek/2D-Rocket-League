import pygame, sys, math
from pygame.locals import *

from settings import *

def debugCornerLocations(car, color = BLACK, thickness = 1): #draws hitbox
    pygame.draw.lines(DISPLAYSURF, color, True, [car["trc"], car["tlc"], car["blc"], car["brc"]], thickness)

def debugCollisionLocations(hits, radius, color = BLACK, thickness = 0): #draws collision locations
    for coords in hits:
        pygame.draw.circle(DISPLAYSURF, color, (int(coords[0]), int(coords[1])), radius, thickness)

def debugDrawLine(startPos, endPos, color = BLACK, thickness = 1): #draws line between two points
    pygame.draw.line(DISPLAYSURF, color, startPos, endPos, thickness)

def debugDrawPointLocation(location, radius, color = BLACK, thickness = 0): #draws location of point
    newLocation = (int(location[0]), int(location[1]))
    pygame.draw.circle(DISPLAYSURF, color, newLocation, radius, thickness)
