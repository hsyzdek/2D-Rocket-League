from utilities.py import *

class wall:
    def __init__(self, pa, pb, isFloor):
        self.pa = pa
        self.pb = pb
        self.isFloor = isFloor
    def getEndPoints(self):
        return (self.pa, self.pb)
    def isFloor(self):
        return isFloor
    def getNormalVector(self, carCOM):
        a = -(pb[1] - pa[1])
        b = pb[0] - pa[0]
        c = -(a * pa[0] + b * pa[1])
        d = (a*carCorner[0] + b*carCorner[1] + c)
        
        v = (pa[1]  - pb[1], pb[0] - pa[0])
        
        return (-d*v[0], -d*v[1])
    def pointIsOnWall(self, point):
        return pointIsOnLine(self.pa, self.pb, point)

class Walls:
    
    def __init__(self):
        self.corners = set([])
        self.walls = []

    #Overloaded constructor, adds walls
    def __init__(self, walls):
        self.corners = set([])
        self.walls = []
        for w in walls:
            self.addWall(self, w)

    #Adds wall vectors
    def addWall(self, w):
        walls.append(w)
        corners.add(w.pa)
        corners.add(w.pb)

    
    def getCollisionTimes(self, corners, cornerSpeeds):
        maxTime = 0
        #First check for any intersections between point routes and walls 
        for i in range(len(corners)):
            #get the location of the corner before and after the tick.
            c1 = corners[i]
            cs = cornerSpeeds[i]
            c2 = (c1[0] - cs[0], c2[1] - cs[1])
            for w in walls:
                col = detectCollisionsBetweenLines(c1, c2, w.pa, w.pb)
                #if there is an intersection, figure out how long it would take
                #to go back to the point of collision. Find the longest such time
                if col[0] != -2 and col[0] != -1:
                    t = 1 - (col[0] - c2[0])/cs[0]
                    if t > maxTime:
                        maxTime = t
        #Next check if the wall vertexes are in the 
        s = self.corners.copy()
        while len(s) > 0:
            wallCorner = s.pop()
            
            
            if(pointIsInPolygon(wallCorner, corners)):
                pb = corners[len(corners) - 1]
                sb = cornerSpeeds[len(corners) - 1]
                for i in range(len(corners)):
                    pa = pb
                    sa = sb
                    pb = corners[i]
                    sb = cornerSpeeds[i]
                    t = linePassesThroughAPoint(pa, sa, pb, sb, wallCorner)
                    if t > maxTime:
                        maxTime = t
                            
        return maxTime

    def getWallCollisionPoints(self, corners, COM):
        #Return a list of collision coordinates with vectors for the normal force
        cols = []
        for c in corners:
            for w in self.walls:
                if w.pointIsOnWall(c):
                    cols.append(c, w.getNormalVector(COM))
        s = self.corners.copy()
        while len(s) > 0:
            wallCorner = s.pop()
            pb = corners[len(corners) - 1]
            for i in range(len(corners)):
                pa = pb
                pb = corners[i]
                if(pointIsOnLine(pa, pb, wallCorner)):
                    cols.append(wallCorner, getNormalVector(pa, pb, wallCorner))
        return cols
