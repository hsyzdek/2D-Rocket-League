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
def miracleFunction(p1, p1speed, pa, paspeed, p0):
    # This function solves the problem of when the line between two parametric lines intersects a point.
    # Create two parametric lines with forms
    # ya = m*x + q
    # xa = o*x + a
    # and
    # yb = n*x + w
    # xb = p*x + r
    # Where x is the time.
    # Then, the equation for the line between the two lines is
    # (y - ya)*(xb - xa) = (x - xa)*(yb - ya)
    # Confusingly, this x is not the same as the previous x,
    # but this is how I solved it. The x and y are actual coordinates.
    # Subsitute
    # y = z
    # x = v
    # Where z is the y coordinate of the point we're search for
    # and v is the x coordinate of the point we're search for
    # Then, (z - m*x - q)*(p*x + r - (o*x + e)) = (v - (o*x + e))*(n*x + w - m*x - q)
    # Using a bit of quick mental arithmetic, solve for x.
    # The solution, of course, is
    # x = (sqrt((-a n + m r - m v + n v - o w + o z + p q - p z)^2 - 4 (m p - n o) (-a w + a z + q r - q v - r z + v w)) - a n + m r - m v + n v - o w + o z + p q - p z)/(2 (n o - m p))
    # when n o - m p!=0
    # Otherwise, the solution is
    # [insert solution here]
    m = p1speed[1]
    q = p1[1]
    o = p1speed[0]
    a = p1[0]
    n = paspeed[1]
    w = pa[1]
    p = paspeed[0]
    r = pa[0]
    z = p0[1]
    v = p0[0]

    denom = (2*(n*o-m*p))
    if abs(denom) < MIN_ERROR:
        print("cool, but unsolved")
    else:
        sqrt = pow(pow(-a*n+m*r-m*v+n*v-o*w+o*z+p*q-p*z, 2) -4*(m*p-n*o)*(-a*w+a*z+q*r-q*v-r*z+v*w), .5)
        t1 = (sqrt -a*n+m*r-m*v+n*v-o*w+o*z+p*q-p*z)/denom
        t2 = (-sqrt -a*n+m*r-m*v+n*v-o*w+o*z+p*q-p*z)/denom
        # There are two solutions. One is when the two lines intersect, the other is the one we want. Determine which is which.
        if(abs(o*t1 + a - p*t1 - r) < MIN_ERROR and abs(m*t1 + q - n*t1 - w) < MIN_ERROR):
            return t2
        else:
            return t1
def parallelWallCarCollision(car, walls, wallDirections):
    
    c1 = car["trc"]
    c2 = car["blc"]
    ca = car["tlc"]
    cb = car["brc"]
    #for all the vertical walls
    for i in range(0, len(walls) - 1, 2):
        if ((c1[0] - walls[i][0]) * wallDirections[i] > 0):
            if (abs(c1[0] - ca[0]) < MIN_ERROR):
                c3 = ca[1]
            else:
                c3 = cb[1]
            wa, wb = walls[i][1], walls[i + 1][1]
            c1v = c1[1]
            if (wa <= c3 <= wb or wb <= c3 <= wa or wa <= c1v <= wb or wb <= c1v <= wa):
                car["vel"] = (0, car["vel"][1])
                car["pos"] = (car["pos"][0] + walls[i][0] - c1[0], car["pos"][1])
                car["COM"] = (car["COM"][0] + walls[i][0] - c1[0], car["COM"][1])
        elif ((c2[0] - walls[i][0]) * wallDirections[i] > 0):
            if (abs(c2[0] - ca[0]) < MIN_ERROR):
                c3 = ca[1]
            else:
                c3 = cb[1]
            wa, wb = walls[i][1], walls[i + 1][1]
            c1v = c2[1]
            if (wa <= c3 <= wb or wb <= c3 <= wa or wa <= c1v <= wb or wb <= c1v <= wa):
                car["vel"] = (0, car["vel"][1])
                car["pos"] = (car["pos"][0] + walls[i][0] - c2[0], car["pos"][1])
                car["COM"] = (car["COM"][0] + walls[i][0] - c2[0], car["COM"][1])
    for i in range(1, len(walls), 2):
        if ((c1[1] - walls[i][1]) * wallDirections[i] > 0):
            if (abs(c1[1] - ca[1]) < MIN_ERROR):
                c3 = ca[0]
            else:
                c3 = cb[0]
            wa, wb = walls[i][0], walls[i + 1][0]
            c1v = c1[0]
            if (wa <= c3 <= wb or wb <= c3 <= wa or wa <= c1v <= wb or wb <= c1v <= wa):
                car["vel"] = (car["vel"][0], 0)
                car["pos"] = (car["pos"][0], car["pos"][1] + walls[i][1] - c1[1])
                car["COM"] = (car["COM"][0], car["COM"][1] + walls[i][1] - c1[1])
        elif ((c2[1] - walls[i][1]) * wallDirections[i] > 0):
            if (abs(c2[1] - ca[1]) < MIN_ERROR):
                c3 = ca[0]
            else:
                c3 = cb[0]
            wa, wb = walls[i][0], walls[i + 1][0]
            c1v = c2[0]
            if (wa <= c3 <= wb or wb <= c3 <= wa or wa <= c1v <= wb or wb <= c1v <= wa):
                car["vel"] = (car["vel"][0], 0)
                car["pos"] = (car["pos"][0], car["pos"][1] + walls[i][1] - c2[1])
                car["COM"] = (car["COM"][0], car["COM"][1] + walls[i][1] - c2[1])

def wallCarCollisions(cars, walls, wallDirections):
    collisions = []
    
    for car in cars:
        #First get all of the collision points
        corners = [car["trc"], car["tlc"], car["blc"], car["brc"], car["trc"]]
        for wc in range (len(walls) - 1):
            w1 = walls[wc]
            w2 = walls[wc+1]
            for cc in range(len(corners) - 1):
                c1 = corners[cc]
                c2 = corners[cc+1]
                col = detectCollision(c1, c2, w1, w2)
                #if the car is parallel to the walls
                if not ( col == (-1, -1) or col == -2):
                    if col[0] == -2:
                        parallelWallCarCollision(car, walls, wallDirections)
                    else:
                        collisions.append((wc, cc, col))
                        debugDrawPointLocation((int(col[0]), int(col[1])), 3, RED)
        #next determine what corners will actually collide with which walls
        toCollide = []
        lastWall, lastCar = -1, -1
        if len(collisions) > 0:
            for col in collisions:
                wallC = col[0]
                carC = col[1]
                #If there are two collision points on the same wall
                if wallC == lastWall:
                    #If the two car collision points are next to eachother, use the mutual corner
                    if lastCar == carC - 1:
                        toCollide.append((wallC, carC))
                    elif (lastCar == 0 and carC == 3):
                        toCollide.append((wallC, 0))
                    #If the two car collision points are not next to eachother, determine which corner to use
                    elif lastCar == carC - 2:
                        if wallC % 2 == 0:
                            index = 0
                        else:
                            index = 1
                        wallPos = walls[wallC][index]
                        for c in range(len(corners)):
                            if (corners[c][index] - wallPos) * wallDirections[wallC] > 0:
                                toCollide.append((wallC, c))
                        #Working code for only one corner marked
                        """carCorner, dif = -1, -1
                        for c in range(len(corners)):
                            if (corners[c][index] - wallPos) * wallDirections[wallC] > dif:
                                carCorner = c
                                dif = (corners[c][index] - wallPos) * wallDirections[wallC]
                        toCollide.append((wallC, carCorner))
                        """
                lastWall = wallC
                lastCar = carC
                            
        for i in toCollide:
            debugDrawPointLocation(corners[i[1]], 3, GREEN)

        if len(toCollide) > 0:
            cornerSpeeds = getLinearSpeed(car)
            maxTime, maxCorner  = -1, -1
            #set absolute boundaries
            index, pos = -1, -1
            for i in range(len(toCollide)):
                corner = toCollide[i][1]
                if corner > 3:
                    corner = 0
                cornerLocation = corners[corner]
                wall = toCollide[i][0]
                wallPos = walls[wall][wall % 2]
                cl = cornerLocation[wall % 2]
                cs = cornerSpeeds[corner]
                css = cs[wall % 2]
                time = getRollbackTime(cornerLocation[wall % 2], cornerSpeeds[corner][wall % 2], wallPos)
                if (time > maxTime):
                    maxTime = time
                    maxCorner = i
                    index = wall % 2
                    pos = wallPos
            rollback(car, maxTime, index, wallPos)
            vx, vy = car["vel"][0], car["vel"][1]
            if index == 0:
                car["vel"] = (0, vy)
            else:
                car["vel"] = (vx, 0)
            
                        
                        
def rollback(car, time, index, wallPos):
    px, py = updateCarPosition(car, car["vel"], -time)
    car["pos"] = (px, py)
    
    updateCarRotation(car, -time)
def getRollbackTime(cornerLocation, cornerSpeed, cornerEndpoint):
    if abs(cornerSpeed) < MIN_ERROR:
        return -1
    return (cornerLocation - cornerEndpoint) / cornerSpeed
def getLinearSpeed (car):
    corners = [car["trc"], car["tlc"], car["blc"], car["brc"]]
    lx, ly = car["vel"][0], car["vel"][1]
    cornerSpeeds = []
    for i in range(len(corners)):
        a = 2 * math.pi * getDistance(car["pos"], corners[i]) * car["angV"] / 360
        theta = math.radians(car["r"]) + car["cornerAngle"]
        ax = math.cos(90 - theta) * a
        ay = math.sin(90 - theta) * a
        cornerSpeeds.append((lx + ax, ly + ay))
    return cornerSpeeds 
        
def getDistance(p1, p2):
    return pow( pow(p1[0] - p2[0], 2) + pow(p1[1]-p2[1], 2), .5)

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
