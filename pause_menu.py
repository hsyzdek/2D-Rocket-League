import pygame, sys, math
from pygame.locals import *

from game_loop_functions import *
from settings import *

def pauseMenu(car):

    paused = True
    toggleRot_key = False
    mainMenu_key = False
    clicked = False
    while paused:
        togRot = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    togRot = True
                elif event.key == pygame.K_ESCAPE:
                    mainMenu_key = True
        pygame.draw.rect(DISPLAYSURF, GREY, (displayWidth/2 - 100, displayHeight/2 - 40, 200, 80))
        toggleRot_button = workingButton("toggle rotation", 25, BLACK, displayWidth/2, displayHeight/2 - 20, 180, 30, CYAN, BLUE)
        mainMenu_button = workingButton("exit to main menu", 25, BLACK, displayWidth/2, displayHeight/2 + 20, 180, 30, CYAN, BLUE)
        if (mainMenu_button or mainMenu_key):
            paused = False
        if pygame.mouse.get_pressed()[0]:
            if toggleRot_button and (not clicked):
                togRot = True
            clicked = True
        else:
            clicked = False
        if togRot:
            if car["angV"] != 0:
                car["angV"] = 0
            else:
                car["angV"] = 60
        pygame.display.update()
        fpsClock.tick(FPS)
