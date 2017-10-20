import pygame, sys, math
from pygame.locals import *

from physics_engine import pointDistance, pointAngle
from settings import *

#initializes properties of a car with given paramaters
def createCar (cars, team, cX, cY, img, w, h, mass, ku, kd, kl, kr, kb, comX, comY, rotation = 0, angVel = 0, angAcc = 0):
    car = {}
    car["pos"] = (cX, cY)
    car["team"] = team
    car["img"] = img
    car["w"] = w
    car["h"] = h
    car["mass"] = mass
    car["trc"] = (cX + w/2, cY - h/2)
    car["tlc"] = (cX - w/2, cY - h/2)
    car["blc"] = (cX - w/2, cY + h/2)
    car["brc"] = (cX + w/2, cY + h/2)
    car["dc"] = car["tlc"]
    car["vel"] = (0, 0)
    car["r"] = rotation
    car["angV"] = angVel
    car["angA"] = angAcc
    car["ku"] = ku
    car["kd"] = kd
    car["kr"] = kr
    car["kl"] = kl
    car["kb"] = kb
    car["cornerAngle"] = math.atan(h/w)
    car["COM"] = (comX, comY) #COM = center of mass
    car["COMInfo"] = (pointAngle(car["pos"], car["COM"]), pointDistance(car["pos"], car["COM"]))
    car["forceInputs"] = []
    car["forces"] = []
    car["torqueAngles"] = [pointAngle(car["COM"],car["trc"]),
                           pointAngle(car["COM"],car["tlc"]),
                           pointAngle(car["COM"],car["blc"]),
                           pointAngle(car["COM"],car["brc"])]
    car["torques"] = []
    cars.append(car)

#initalizes ball
def createBall(ball):
    ball["img"] = pygame.image.load('ball.png')
    w, h = ball["img"].get_rect().size
    ball["r"] = w / 2
    ball["pos"] = (400, 200)
    ball["angV"] = 0

#def createCarControls(player, up, down, left, right, boost):

#Returns corners of walls, starting and ending with the ceiling/left wall corner
#and going counter-clockwise
def createWalls(wallW, goalW, goalH, w, h):
    c = []
    c.append(wall(wallW + goalW, wallW))
    c.append(wall(wallW + goalW, h - (wallW + goalH)))
    c.append(wall(wallW,  h - (wallW + goalH)))
    c.append(wall(wallW, h - wallW))
    c.append(wall(w - wallW, h - wallW))
    c.append(wall(w - wallW, h - (wallW + goalH)))
    c.append(wall(w - (wallW + goalW), h - (wallW + goalH)))
    c.append(wall(w - (wallW + goalW), wallW))
    c.append(wall(wallW + goalW, wallW) )
    
    return Walls(c) 
