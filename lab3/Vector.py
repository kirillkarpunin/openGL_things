from Point import Point
import math


class Vector:
    def __init__(self, angle):
        angleRad = angle * math.pi / 180
        self.x = math.cos(angleRad)
        self.y = math.sin(angleRad)

    def multiply(self, multiplier):
        self.x *= multiplier
        self.y *= multiplier

    def use(self, point):
        return Point(
            point.x + self.x,
            point.y + self.y)
