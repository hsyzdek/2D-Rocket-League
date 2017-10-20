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

