import pygame, sys, math, random
from pygame.locals import *

from debug import *
from settings import *
from physics_engine import *

#Updates the 4 locations of the corners of the car and the "drawing corner"
#based on the rotation of the car, the center position of the car, and the
#car side lengths
def updateCorners(car):
    w, h = car["w"], car["h"]
    x, y = car["pos"]
    cornerAngle = car["cornerAngle"]
    theta = math.radians(car["r"])
    d = math.pow( math.pow(w / 2, 2) + math.pow(h / 2, 2), 0.5)
    dispx = math.cos(theta + cornerAngle) * d
    dispy = math.sin(theta + cornerAngle) * d
    minx = dispx + x
    miny = dispy + y
    car["trc"] = (dispx + x, -dispy + y)
    dispx = math.cos(math.pi + theta - cornerAngle) * d
    dispy = math.sin(math.pi + theta - cornerAngle) * d
    minx = min(dispx + x, minx)
    miny = min(dispy + y, miny)
    car["tlc"] = (dispx + x, -dispy + y)
    dispx = math.cos(math.pi + theta + cornerAngle) * d
    dispy = math.sin(math.pi + theta + cornerAngle) * d
    minx = min(dispx + x, minx)
    miny = min(dispy + y, miny)
    car["blc"] = (dispx + x, -dispy + y)
    dispx = math.cos(theta - cornerAngle) * d
    dispy = math.sin(theta - cornerAngle) * d
    minx = min(dispx + x, minx)
    miny = min(dispy + y, miny)
    car["brc"] = (dispx + x, -dispy + y)
    car["dc"] = (minx, miny)

#updates center of mass location
def updateCOM(car): #added displaySurface for debug
    theta = math.radians(car["r"])
    comX = int(car["COMInfo"][1] * (math.cos(math.radians(car["COMInfo"][0]) + theta)) + car["pos"][0])
    comY = int(car["COMInfo"][1] * -(math.sin(math.radians(car["COMInfo"][0]) + theta)) + car["pos"][1])
    car["COM"] = (comX, comY)
    debugDrawPointLocation(car["COM"], 3, CYAN) #COM debug

#updates the drawing inside the hitbox
#def updateCarSprite

def updateCarPosition(car, netVel):
    pX = car["pos"][0] + (netVel[0] / FPS)
    pY = car["pos"][1] + (netVel[1] / FPS)
    return (pX,pY)
    
def updateCarVelocity(car, netAccel):
    vX = car["vel"][0] + (netAccel[0] / FPS)
    vY = car["vel"][1] + (netAccel[1] / FPS)
    #print(car["vel"])
    return (vX,vY)


def calculateCarNetAccel(car):
    #netAccel = gravity()
    netAccel = [0, 0]
    for inputs in car["forceInputs"]:
        if inputs == "forward":
            drivingForce(car, True)
            print("forward")
        if inputs == "backward":
            drivingForce(car, False)
            print("backward")
        if inputs == "boost":
            boostForce(car)
            print("boost")
            
##    normalForce(car)
##    drivingForce(car)
##    boostForce(car)
##    carForce(car)
##    ballForce(car)
##    frictionForce(car)
    
    for force in car["forces"]:
        netAccel[0] += force[0][0]
        netAccel[1] += force[0][1]
    car["forces"] = []
    return netAccel

'''
def calculateCarNetAccel(car, forces):
    netAccel = [0,0]
    boundaryNormalForce(car)
    frictionForce(car)
    
##    for force in forces:
##        if len(force) == 0:
##            continue
##        elif len(force) > 1:
##            for obj in force:
##                netAccel[0] += obj[0]
##                netAccel[1] += obj[1]   
##        else:
##            netAccel[0] += force[0]
##            netAccel[1] += force[1]
    
    netAccel[0] = forces["gravity"][0] + forces["normals"][0] + forces["driving"][0] + forces["boost"][0] + forces["friction"][0]
    netAccel[1] = forces["gravity"][1] + forces["normals"][1] + forces["driving"][1] + forces["boost"][1] + forces["friction"][1]
    return netAccel
'''
def updateCarRotation(car, netAngVel):
    rotation = car["r"] + (netAngVel / FPS)
    return rotation

def updateCarAngVel(car, netAngAccel):
    angVel = car["angV"] + (netAngAccel / FPS)
    #print(car["vel"])
    return angVel

def calculateCarNetAngAccel(car):
    r = car["r"]
    while r > 360 or r < 0:
        if r > 0:
            r -= 360
        else:
            r += 360
    alpha = 0
    for force in car["forces"]:
        distance = pointDistance(car["pos"], force[1])
        if distance < MIN_ERROR:
            continue
        else:
            angle = pointAngle(car["pos"], force[1]) - r
        alpha += torques(car,force,distance,angle)
    return alpha   
    
def boostAnimation(car, toggle = False):
    if toggle:
        for i in range(random.randint(5,10)):
            pass

def setBoostStrength(num):
    boostStrength = -num
