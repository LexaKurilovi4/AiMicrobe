from math import sqrt, pow


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'x: {self.x}, y: {self.y}'

    def get_dist_to(self, other):
        return sqrt(pow(self.x - other.x, 2) + pow(self.y - other.y, 2))
