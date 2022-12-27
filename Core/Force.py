import math
from Structure.Vec2 import Vec2 
class Force:
    constants = [0, 1, 100, 10000, 3, 0, 0, 0, 0]
    # c1 = 1
    # c2 = 100
    # c3 = 10000
    # c4 = 3
    # m = 100

    # c1 = 0
    # c2 = 1
    # c3 = 0
    # c4 = 0
    # m = 100

    def fast_force(pos1, pos2):
        pass

    def attraction(pos1, pos2):
        if Vec2.dist(pos1, pos2) == 0:
            return 0
        return Force.constants[1]*math.log(Vec2.dist(pos1, pos2)/Force.constants[2])
    def repulsion(pos1, pos2):
        if Vec2.dist(pos1, pos2) == 0:
            return 0
        return Force.constants[3]/Vec2.dist(pos1, pos2)**2

    def edge_attraction(pos1, pos2):
        if Vec2.dist(pos1, pos2) == 0:
            return 0
        return Force.constants[4]*math.log(Vec2.dist(pos1, pos2)/Force.constants[2])