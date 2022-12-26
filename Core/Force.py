import math
from Structure.Vec2 import Vec2 
c1 = 1
c2 = 1
c3 = 100000
c4 = 1
# m = 100

# c1 = 0
# c2 = 1
# c3 = 0
# c4 = 0
# m = 100


def attraction(pos1, pos2):
    # if Vec2.dist(pos1, pos2) == 0:
        # return 100
    return c1*math.log(Vec2.dist(pos1, pos2)/c2)
def repulsion(pos1, pos2):
    # if Vec2.dist(pos1, pos2) == 0:
        # return 100
    return c3/Vec2.dist(pos1, pos2)**2

def edge_attraction(pos1, pos2):
    return c4*math.log(Vec2.dist(pos1, pos2)/c2)