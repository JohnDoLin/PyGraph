import math
class Vec2:
    def __init__(self, *args):
        if len(args) == 0:
            self.v = [0, 0]
        elif len(args) == 1 and type(args[0]) == Vec2:
            self.v = args[0].v
        elif len(args) == 1 and type(args[0]) == list: 
            self.v = args[0]
        elif len(args) == 2:
            self.v = [args[0], args[1]]
    def __add__(self, other):
        return Vec2(self.v[0] + other.v[0],self.v[1] + other.v[1])
    def __mul__(self, other):
        return Vec2(self.v[0]*other, self.v[1]*other)
    def __sub__(self, other):
        return Vec2(self.v[0] - other.v[0],self.v[1] - other.v[1])
    def __truediv__(self, other):
        return Vec2(self.v[0] / other, self.v[1] / other)
    def norm(self):
        return math.sqrt(self.v[0]**2 + self.v[1]**2)
    def normalized(self):
        if self.norm() == 0:
            return Vec2(0, 0)
        return self / self.norm()
    def __getitem__(self, key):
        return self.v[key]
    def __str__(self) -> str:
        return 'Vec2(' + str(self.v) + ')'
    def __repr__(self) -> str:
        return 'Vec2(' + str(self.v) + ')'
    def to_int_array(self):
        return [int(self.v[0]), int(self.v[1])]
    def to_precision_array(self, digit = 100):
        return [round(self.v[0], digit), round(self.v[1], digit)]

    def dot(self, other):
        return sum([self.v[i]*other.v[i] for i in range(2)])

    def det(self, other):
        return self.v[0] * other.v[1] - self.v[1] * other.v[0]

    def dist_to_two_dots(self, vec1, vec2):
        if (vec2 - vec1).norm() == 0:
            return math.inf
        return abs((vec2 - vec1).det(self - vec1)) / (vec2 - vec1).norm()
    
    @staticmethod
    def dist(vec1, vec2):
        return math.sqrt((vec1.v[0] - vec2.v[0])**2 + (vec1.v[1] - vec2.v[1])**2)

        

