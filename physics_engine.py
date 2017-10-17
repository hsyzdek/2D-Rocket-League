import pygame, sys, math
from pygame.locals import *

from debug import *
from settings import *

MAX_SLOPE = 21600001 #max slope with this restriction and a 4k screen
MIN_ERROR = 0.0001   #min difference tolerated

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


#returns the coordinates of all collision instances
def getCollisionCoords(car, ball, r):#added displaySurface parameter for debug(find easier way to do this)
    ball = (ball[0] + r, ball[1] + r)
    hits=[]
    m1,m2,m3,m4 = 0,0,0,0
    c1,c2,c3,c4 = 0,0,0,0
    corners=[[car["trc"],m1,c1], [car["tlc"],m2,c2], [car["blc"],m3,c3], [car["brc"],m4,c4]]
    for i in range(4):
        j=i+1
        if j==4:
            j=0
        x1, x2, y1, y2 = corners[i][0][0], corners[j][0][0], corners[i][0][1], corners[j][0][1]
        a, b = ball[0], ball[1]
        if abs(x1 - x2) < MIN_ERROR:
            corners[i][1] = MAX_SLOPE 
            tosqrroot = r**2 - (x1 - a)**2
            if tosqrroot < 0:
                continue
            f1 = (tosqrroot**.5) + b
            f2 = -(tosqrroot**.5) + b
            if ( y2 >= f1 >= y1 ) or ( y2 <= f1 <= y1 ):
                hits.append((x1, f1))
            if ( y2 >= f2 >= y1 ) or ( y2 <= f2 <= y1 ):
                hits.append((x2, f2))
        else:
            m = (y1 - y2)/(x1-x2)
            c = y1 -(m*x1)
            corners[i][1] = m #add slope and intercept to corners list
            corners[i][2] = c
            tosqrroot = (m**2)*(r**2-a**2) + ((2*a*m)-(b-c))*(b-c) + r**2 #condensed original
            #-a**2 * m**2 + 2*a*b*m - 2*a*c*m - b**2 +2*b*c - c**2 + m**2 * r**2 + r**2
            if tosqrroot < 0: 
                continue
            f1 = ( tosqrroot**.5 + a + b*m - c*m )/(m**2 + 1)
            f2 = ( -(tosqrroot**.5) + a + b*m - c*m )/(m**2 + 1)
            if ( x2 >= f1 >= x1 ) or ( x2 <= f1 <= x1 ):
                hits.append((f1, m*f1 + c))
            if ( x2 >= f2 >= x1 ) or ( x2 <= f2 <= x1 ):
                hits.append((f2, m*f2 + c))
                
    if len(hits) == 0:
        return (-1,-1)
    else:
        collisionPoint = avgCarCollisionPoints(car, hits, corners)
        
    return hits

#averages collision points provided by getCollisionCoords(), returns location on car
#hitbox colinear with the center of mass and collision point average
def avgCarCollisionPoints(car, hits, corners):#added displaySurface parameter 
    avgColX, avgColY = 0,0
    colPointX, colPointY = -1,-1
    collisionPoint = []
    vertical = False
    for coords in hits:
        avgColX += coords[0]
        avgColY += coords[1]
    avgColX, avgColY = int(avgColX/len(hits)), int(avgColY/len(hits))
    
    debugDrawPointLocation((avgColX,avgColY), 3, RED)  #avg location debug
    
    if abs(avgColX - car["COM"][0]) < MIN_ERROR:
        centerSlope = MAX_SLOPE
        vertical = True
    else: 
        centerSlope = (avgColY - car["COM"][1])/(avgColX - car["COM"][0])
        centerIntercept = avgColY - (centerSlope*avgColX)
    for i in range(4):
        j=i+1
        if j==4:
            j=0
        m, c = corners[i][1], corners[i][2]
        x1, x2, y1, y2 = corners[i][0][0], corners[j][0][0], corners[i][0][1], corners[j][0][1]

        if abs(centerSlope - m) < MIN_ERROR:
            continue
        elif m >= MAX_SLOPE:
            colPointX = x1
            colPointY = centerSlope*colPointX + centerIntercept
            if ( y2 > colPointY >= y1 ) or ( y2 < colPointY <= y1 ):
                collisionPoint.append((int(colPointX), int(colPointY)))
        else:
            if not vertical:
                colPointX = (c - centerIntercept) / (centerSlope - m)
            else:
                colPointX = avgColX
            colPointY = int(m*colPointX + c)
            if ( x2 > colPointX >= x1 ) or ( x2 < colPointX <= x1 ):
                collisionPoint.append((int(colPointX), colPointY))
                
    if len(collisionPoint) != 2:
        print("noooo", len(collisionPoint)) #have this print an error and close window 

    foundPoint = False
    finalCollisionPoint = (-1, -1)
    for i in collisionPoint:
        distanceCOL_COM = pointDistance(i, car["COM"])
        distanceAVG_COL = pointDistance((avgColX,avgColY), i)
        if (distanceAVG_COL <= distanceCOL_COM) and not foundPoint:
            foundPoint = True
            finalCollisionPoint = i
        else:    
            debugDrawPointLocation(i, 3, PURPLE)
        debugDrawLine(car["COM"], i, BLUE)
    debugDrawPointLocation(finalCollisionPoint, 3, YELLOW)
    return finalCollisionPoint


        
#Takes two points as endpoints of a line segment, if there
#is an intersection, return the point of intersection in a tuple, otherwise
#return (-1,-1). If the lines are parallel, returns (-2, -2)
def detectCollision(p1, p2, pa, pb):
    x0 = p1[0]          
    dx1 = p2[0] - p1[0] 
    y0 = p1[1]          
    dy1 = p2[1] - p1[1] 
    xa = pa[0]          
    dxa = pb[0] - pa[0] 
    ya = pa[1]          
    dya = pb[1] - pa[1] 
    #Checks to see if the slopes are approximately equal, then return a seperate code
    #so it can test to see if the lines are close enough to count as touching out
    #of this function
    if (abs(dy1 * dxa - dx1 * dya) < MIN_ERROR):
        #If the line is horizontal
        if abs(dy1) < 1:
            return (-2, 0, ya - y0)
        elif abs(dx1) < 1:
            return (-2, xa - x0, 0)
        else:
            return (-2)
    #Uses hardcore algebra. Paramatarize two lines into the forms:
    #x0 + m * dx1 = x
    #y0 + m * dy1 = y
    #xa + n * dxa = x
    #ya + n * dya = y
    #Then, solve for x and y in terms of dx1, dy1, dxa, dya, x0, y0, xa, ya.
    #Solved equation has 16 components.
    else:
        x = (x0* dy1 * dxa - dx1 * (y0*dxa + xa*dya - dxa*ya)) / (dy1 * dxa - dx1 * dya)
        y = (x0 * dy1 * dya - dx1 * y0 * dya - dy1 * xa * dya + dy1 * dxa * ya) / (dy1 * dxa - dx1 * dya)
        #If the point is in the boundaries of the line segment
        if (p1[0] - MIN_ERROR <= x <= p2[0] + MIN_ERROR or p2[0] - MIN_ERROR <= x <= p1[0] + MIN_ERROR) and (pa[0] - MIN_ERROR <= x <= pb[0] or pb[0] - MIN_ERROR <= x <= pa[0] + MIN_ERROR) and (p1[1] - MIN_ERROR <= y <= p2[1] or p2[1] - MIN_ERROR <= y <= p1[1] + MIN_ERROR) and (pa[1] - MIN_ERROR <= y <= pb[1] or pb[1] <= y <= pa[1] + MIN_ERROR):
            return(x, y)
        else:
            return (-1, -1)

def pointDistance(point1, point2):
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5
def pointAngle(point1, point2): #initial, terminal
    if abs(point1[0] - point2[0]) < MIN_ERROR:
        if (point2[1] - point1[1]) > 0:
            return 270
        else:
            return 90
    aysmp = 0
    if (point2[0] - point1[0]) < 0:
        aysmp = 180
    if aysmp == 0 and (point2[1] - point1[1]) > 0:
        aysmp = 360
    return math.degrees(math.atan((point1[1] - point2[1]) / (point2[0] - point1[0]))) + aysmp

def isOnGround(car):
    if car["r"] == 0 and car["pos"][1] >= (displayHeight - (car["h"]/2)):
        return True
    return False


#change all [force, locations] to tuples

def normalForce(car):
    if car["pos"][1] >= (displayHeight - (car["h"]/2)):
        car["pos"] = (car["pos"][0],(displayHeight - (car["h"]/2)))
        car["vel"] = (car["vel"][0], 0) #will be (carElasticity * -car["vel"][1])
        car["forces"].append([(-gravity[0], -gravity[1]), car["pos"]]) #temporary until corners
    else:
        forces["normals"] = [0,0]

def drivingForce(car, direction): #true for forwards, false for backwards
    if direction:
        car["forces"].append([(1000,0), car["pos"]])
    else:
        car["forces"].append([(-1000,0), car["pos"]])

def boostForce(car):
    boost = ((boostStrength * math.cos(math.radians(car["r"]))),(-boostStrength * math.sin(math.radians(car["r"]))))
    car["forces"].append([boost, car["pos"]])
    #print(boostStrength)

#def carForce(car, cars):

def ballForce(car, ball):
    getCollisionCoords(car, ball)
    
def frictionForce(car):
    netVel = ((car["vel"][0])**2 + (car["vel"][1])**2)**0.5
    if isOnGround(car) and netVel >= MIN_VAL:
        car["forces"].append([(COF * math.cos(math.radians(car["r"])), COF * math.sin(math.radians(car["r"]))), car["pos"]])#* Normal force magnitide
        #^address issue about never being 0
        
def rotationDirection(car, rotation):
    theta = 0
    for torqueAngle in car["torqueAngles"]: #issue if ball hits corner from underside, rotates the wrong way
        if theta <= angle < (theta + 90):
            if angle < torqueAngle:
                return 1
            else:
                return -1
        theta += 90

def torques(car, force, distance, rotation):
    r = rotationDirection(car, rotation)
    leverArm = (force[1][0] - car["pos"][0], car["pos"][1] - force[1][1])
    forceMag = ((force[0][0]**2) + (force[0][1]**2))**0.5
    theta = math.acos(((leverArm[0] * force[0]) + (leverArm[1] * force[1])) / (distance * forceMag))
    netForce = math.son(theta)
    return (r * netForce) / distance
