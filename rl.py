import pygame, sys, math
from pygame.locals import *

from object_init import *
from physics_engine import *
from debug import *
from pause_menu import *
from game_loop_updates import *
from game_loop_functions import *
from settings import *

pygame.init()

#Instantiate car/ball/walls
cars = []
ball = {}
originalcarImg = pygame.image.load('car.jpg')
rotation = 0
angularVelocity = 0
carw, carh = originalcarImg.get_rect().size
goalW, goalH = 200, 400
wallW = 10
w, h = pygame.display.get_surface().get_size()
walls, wallDirections = createWalls(wallW, goalW, goalH, w, h)
mass = 1500
carx = 400 #carx = 10
cary = 200 #cary = h - carh - 10
comx, comy = carx + 25, cary + 12 #edit COM relative to center position of car (completely arbitrary right now)
team = ORANGE
#createCarControls()
createCar(cars, team, carx, cary, originalcarImg, carw, carh, mass, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE, comx, comy, rotation, angularVelocity)
createBall(ball)

clicked = False
physics = False
physicsClicked = False

rotating = False

gameLoop = True
while gameLoop: # the main game loop
    DISPLAYSURF.fill(GREY)
    pygame.draw.lines(DISPLAYSURF, BLACK, False, walls, 2)
    pygame.draw.rect(DISPLAYSURF, BLUE, (wallW, h - (wallW + goalH), goalW, goalH))
    pygame.draw.rect(DISPLAYSURF, WHITE, (walls[0][0], walls[0][1], w - 2 * (wallW + goalW), h - 2*wallW))
    pygame.draw.rect(DISPLAYSURF, ORANGE, (walls[6][0], walls[6][1], goalW, goalH))
    pygame.draw.lines(DISPLAYSURF, BLACK, False, walls, 2)

    for event in pygame.event.get():
        if event.type == QUIT:
            gameLoop = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("OK")
                pauseMenu(car)
            if event.key == car["ku"]:
                car["angV"] -= 200
            if event.key == car["kd"]:
                car["angV"] += 200
        if physics:
            if event.type == pygame.KEYDOWN:
                if event.key == car["kr"] and isOnGround(car):
                    forces["driving"][0] += 1000 #will be based on car rotation later
                    forces["driving"][1] += 0
                if event.key == car["kl"] and isOnGround(car):
                    forces["driving"][0] += -1000 
                    forces["driving"][1] += 0
                if event.key == car["kb"]:
                    forces["boost"][0] = -800 * math.cos(math.radians(car["r"]))
                    forces["boost"][1] = 800 * math.sin(math.radians(car["r"]))
                    boostAnimation(car, True)
            if event.type == pygame.KEYUP:
                if event.key == car["ku"]:
                    car["angV"] += 200
                if event.key == car["kd"]:
                    car["angV"] += -200
                if event.key == car["kr"] and isOnGround(car):
                    forces["driving"][0] += -1000
                    forces["driving"][1] += 0
                if event.key == car["kl"] and isOnGround(car):
                    forces["driving"][0] += 1000
                    forces["driving"][1] += 0
                if event.key == car["kb"]:
                    forces["boost"] = [0,0]
                    boostAnimation(car, False)
        

    ####################
    # TEMPORARY SOLUTION
    # FOR DEBUGGING ONLY
    ####################
    if not physics:
        if pygame.key.get_focused():
            press = pygame.key.get_pressed()
            #release = pygame.key.get_released()
            #change velocity of cars based on directions pushed        
            for car in cars:
                if press[car["kd"]]:
                    car["pos"] = (car["pos"][0], car["pos"][1] + 2)
                if press[car["ku"]]:
                    car["pos"] = (car["pos"][0], car["pos"][1] - 2)
                if press[car["kr"]]:
                    car["pos"] = (car["pos"][0] + 2, car["pos"][1])
                if press[car["kl"]]:
                    car["pos"] = (car["pos"][0] - 2, car["pos"][1])

    
        
    #draw every car on the frame
    for car in cars:
        carImg = pygame.transform.rotate(car["img"], car["r"])
        DISPLAYSURF.blit(carImg, car["dc"])
        debugCornerLocations(car, BLUE)
    #DISPLAYSURF.blit(ball["img"], ball["pos"])
                
    #change position and rotation of car based on velocity and angular velocity
    for car in cars:
        #ideally should just have updateCar() in this for loop and that's it
        vx, vy = car["vel"]
        #px = car["pos"][0] + vx / FPS
        #py = car["pos"][1] + vy / FPS
        #car["pos"] = (px, py)
        car["r"] += car["angV"] / FPS
        updateCarRotation(car, FPS)
        updateCorners(car)
        updateCOM(car)
        #print(netAccel)
        if physics:
            netAccel = calculateCarNetAccel(car, forces)
            car["vel"] = updateCarVelocity(car, netAccel)
            car["pos"] = updateCarPosition(car, car["vel"], 1 / FPS)
        debugDrawPointLocation((int(car["pos"][0]), int(car["pos"][1])), 3, ORANGE)
            #^position debug
    for car in cars:
        coords = getCollisionCoords(car, ball["pos"], ball["r"])
        if(coords != (-1, -1)):
            debugCollisionLocations(coords, 3, GREEN)

    testButton = workingButton("test button", 25, BLACK, 100, 50, 100, 80, CYAN, BLUE)
    if testButton:
        if not clicked:
            if rotating:
                car["angV"] = 0
                rotating = False
            else:
                car["angV"] = 60
                rotating = True
        clicked = True
    else:
        clicked = False
    phsyiscsButton = workingButton("physics button", 25, BLACK, 100, 135, 100, 80, CYAN, BLUE)
    if phsyiscsButton:
        if not physicsClicked:
            physics = not physics
        physicsClicked = True
    else:
        physicsClicked = False
    wallCarCollisions(cars, walls, wallDirections)
##    messageToScreen("Watch what the shell prints.  If there's an error it'll print \"noooo\" followed by a number.  Let me know what happens."
##                    ,[500,660]
##                    ,25)
##    messageToScreen("Please try to break it in any way you can think of (without editing the code cuz I know you'll claim that that still breaks it)."
##                    ,[500,680]
##                    ,25)
    pygame.display.update()
    #waits until the car is done
    fpsClock.tick(FPS)
pygame.quit()
sys.exit()
