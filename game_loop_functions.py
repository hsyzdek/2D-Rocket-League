import pygame, sys, math
from pygame.locals import *

from settings import *

#displays message to screen
def messageToScreen(message, location, size, color = BLACK):
    font = pygame.font.SysFont(None, size)
    text = font.render(message, True, color)
    #changes the location to be the center of the text rather than the top left corner
    location = [location[0] - int(text.get_width()/2),location[1] - int(text.get_height()/2)]
    DISPLAYSURF.blit(text, location)

#def configureSurface(

#def toggleFullscreen
    
def button(msg, size, color, buttonX, buttonY, buttonWidth, buttonHeight, activeColor, inactiveColor):
    cursor = pygame.mouse.get_pos()
    clicked, pressed = False, False
    dc = [0,0]
    dc[0] = int(buttonX - (buttonWidth/2))
    dc[1] = int(buttonY - (buttonHeight/2))
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                clicked = True
                print("YES")
    if (dc[0] <= cursor[0] <= dc[0]+buttonWidth) and (dc[1] <= cursor[1] <= dc[1]+buttonHeight):
        pygame.draw.rect(DISPLAYSURF, activeColor, (dc[0],dc[1],buttonWidth,buttonHeight))
        if clicked:
            pressed = True
            print("clicked solved")
    else:
        pygame.draw.rect(DISPLAYSURF, inactiveColor, (dc[0],dc[1],buttonWidth,buttonHeight))
    messageToScreen(msg, (buttonX, buttonY), size, color)
    return pressed

#kinda works
def workingButton(msg, size, color, buttonX, buttonY, buttonWidth, buttonHeight, activeColor, inactiveColor):
    cursor = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    dc = [0,0]
    dc[0] = int(buttonX - (buttonWidth/2))
    dc[1] = int(buttonY - (buttonHeight/2))
    pressed = False
    if (dc[0] <= cursor[0] <= dc[0]+buttonWidth) and (dc[1] <= cursor[1] <= dc[1]+buttonHeight):
        pygame.draw.rect(DISPLAYSURF, activeColor, (dc[0],dc[1],buttonWidth,buttonHeight))
        if click[0] == 1:
            pressed = True
            print("clicked")
    else:
        pygame.draw.rect(DISPLAYSURF, inactiveColor, (dc[0],dc[1],buttonWidth,buttonHeight))
    messageToScreen(msg, (buttonX, buttonY), size, color)    
    return pressed


def haydenButton(msg, size, color, buttonX, buttonY, buttonWidth, buttonHeight, activeColor, inactiveColor):
    pressed = False
    clickLocation = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]
    xDif = abs(buttonX - clickLocation[0])
    yDif = abs(buttonY - clickLocation[1])
    dc = [0,0]
    dc[0] = int(buttonX - (buttonWidth/2))
    dc[1] = int(buttonY - (buttonHeight/2))

    if (xDif < buttonWidth/2 and yDif < buttonHeight/2):
        pygame.draw.rect(DISPLAYSURF, activeColor, (dc[0],dc[1],buttonWidth,buttonHeight))
        if click:
            pressed = True
            print("clicked")
    else:
        pygame.draw.rect(DISPLAYSURF, inactiveColor, (dc[0],dc[1],buttonWidth,buttonHeight))
    messageToScreen(msg, (buttonX, buttonY), size, color)    
    return pressed

        
