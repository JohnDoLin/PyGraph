import math
class Vec2:
    def __init__(self, *args):
        if len(args) == 0:
            self.v = [0, 0]
        if len(args) == 1:
            self.v = args[0]
        if len(args) == 2:
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
        return str(self.v)
    def __repr__(self) -> str:
        return str(self.v)
    def to_int_array(self):
        return [int(self.v[0]), int(self.v[1])]
    def to_precision_array(self, digit = 100):
        return [round(self.v[0], digit), round(self.v[1], digit)]



