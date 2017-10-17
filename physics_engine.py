import pygame, sys, math
from pygame.locals import *

from debug import *
from settings import *

MAX_SLOPE = 21600001 #max slope with this restriction and a 4k screen
MIN_ERROR = 0.0001   #min difference tolerated

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

def changeGravity(yGravity, xGravity = 0):
    forces["gravity"] = (xGravity, yGravity)
    
def boundaryNormalForce(car):
    if car["pos"][1] >= (displayHeight - (car["h"]/2)):
        forces["normals"][0], forces["normals"][1] = -gravity[0], -gravity[1]
        car["pos"] = (car["pos"][0],(displayHeight - (car["h"]/2)))
        car["vel"] = (car["vel"][0], 0) #will be (carElasticity * -car["vel"][1])
    else:
        forces["normals"] = [0,0]

def isOnGround(car):
    if car["r"] == 0 and car["pos"][1] >= (displayHeight - (car["h"]/2)):
        return True
    return False

def frictionForce(car):
    if isOnGround(car):   
        forces["friction"][0] = COF * -car["vel"][0]
        forces["friction"][1] = COF * -car["vel"][1] 
        #^address issue about never being 0
