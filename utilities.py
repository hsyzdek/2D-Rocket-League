def pointIsOnLine(pa, pb, point):
    if abs( (point[0] - pa[0]) * (pb[1] - pa[1]) - (point[1] - pa[1]) * (pb[0] - pa[0]) ) < MIN_ERROR:
            if pa[0] - MIN_ERROR <= point[0] <= pb[0] + MIN_ERROR or pb[0] - MIN_ERROR <= point[0] <= pa[0] + MIN_ERROR:
                return True
    return False

def pointIsInPolygon(point, polygon):
    #Assumes counterclockwise orientation of car corners.
    #In order for the point to be inside the car, the point must be on the
    #left side of the wall, orientated towards point b from point a.

    #Because python is a dumb language, we don't (and can't) declare our variables
    #outside the loop as scope doesn't really exist
    pb = polygon[len(polygon) - 1]
    for i in range(len(polygon)):
        pa = pb
        pb = polygon[i]

        a = -(pb[1] - pa[1])
        b = pb[0] - pa[0]
        c = -(a * pa[0] + b * pa[1])

        if (a * point[0] + b * point[1] + c) >= -MIN_ERROR:
            return False
            break
    return True
def getNormalVector(self, pa, pb, point):
        a = -(pb[1] - pa[1])
        b = pb[0] - pa[0]
        c = -(a * pa[0] + b * pa[1])
        d = (a*point[0] + b*point[1] + c)
        
        v = (pa[1]  - pb[1], pb[0] - pa[0])
        
        return (-d*v[0], -d*v[1])
