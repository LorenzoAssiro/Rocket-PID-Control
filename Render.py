from math import sin, cos, pi, radians, tan
from VectorMath import *

class Polygon:
    def __init__(self, pos, points, rotation=0, color="white", thickness=0, show_center=False):
        if len(points) < 3:
            raise ValueError('A polygon must have 3 or more sides')
        self.pos = vec2(pos)
        self.points_dists = points
        self.points = []
        self.rotation = radians(rotation)
        self.color = color
        self.outline_thickness = thickness
        self.show_center = show_center
        self.calculate_points_pos()

    def get_pos(self):
        return self.pos

    def get_rotation(self):
        return self.rotation

    def set_rotDeg(self, deg):
        self.rotation = radians(deg)

    def set_rotRad(self, rad):
        self.rotation = rad

    def rotateDeg(self, deg):
        self.rotation += radians(deg)

    def rotateRad(self, rad):
        self.rotation += rad

    def get_points_pos(self):
        return [point.get() for point in self.points]

    def calculate_points_pos(self):
        self.points = []

        for point in self.points_dists:
            x = point[0] * cos(self.rotation) - point[1] * sin(self.rotation)
            y = -(point[0] * sin(self.rotation) + point[1] * cos(self.rotation))
            self.points.append(vec2(x+self.pos.x, y+self.pos.y))

    def draw(self, pg, screen):
        self.calculate_points_pos()
        if self.show_center:
            pg.draw.circle(screen, "red", self.pos.get(), 2, 0)
        pg.draw.polygon(screen, self.color, [point.get() for point in self.points], self.outline_thickness)


class InscribedPolygon(Polygon):
    def __init__(self, pos, radius, sidesNum, rotation=0, color="white", thickness=0, show_center=False):
        if sidesNum % 2 == 1:
            start_angle = pi/2
        else:
            start_angle = pi/4
        super().__init__(pos, [(radius * cos(2*pi*i/sidesNum + start_angle), radius * sin(2*pi*i/sidesNum + start_angle)) for i in range(sidesNum)], rotation, color, thickness, show_center)

class CircumscribedPolygon(Polygon):
    def __init__(self, pos, apothem, sidesNum, rotation=0, color="white", thickness=0, show_center=False):
        radius = apothem/cos(pi/sidesNum)
        if sidesNum % 2 == 1:
            start_angle = pi/2
        else:
            start_angle = pi/4
        super().__init__(pos, [(radius * cos(2*pi*i/sidesNum + start_angle), radius * sin(2*pi*i/sidesNum + start_angle)) for i in range(sidesNum)], rotation, color, thickness, show_center)

class RegularPolygon(Polygon):
    def __init__(self, pos, side, sidesNum, rotation=0, color="white", thickness=0, show_center=False):
        f = 1/(2*tan(pi/sidesNum))   # apothem = fixed number * side
        radius = f*side/cos(pi/sidesNum)
        if sidesNum % 2 == 1:
            start_angle = pi/2
        else:
            start_angle = pi/4
        super().__init__(pos, [(radius * cos(2*pi*i/sidesNum + start_angle), radius * sin(2*pi*i/sidesNum + start_angle)) for i in range(sidesNum)], rotation, color, thickness, show_center)

class Triangle(Polygon):
    def __init__(self, pos, side, rotation=0, color="white", thickness=0, show_center=False):
        radius = 0.688*side/cos(pi/3)
        super().__init__(pos, [(0, radius), (radius * cos(-pi/6), radius * sin(-pi/6)), (radius * cos(-5/6*pi), radius * sin(-5/6*pi))], rotation, color, thickness, show_center)

class Pentagon(Polygon):
    def __init__(self, pos, side, rotation=0, color="white", thickness=0, show_center=False):
        radius = 0.688*side/cos(pi/5)
        super().__init__(pos, [(radius * cos(2*pi*i/5 + pi/2), radius * sin(2*pi*i/5 + pi/2)) for i in range(5)], rotation, color, thickness, show_center)

class Hexagon(Polygon):
    def __init__(self, pos, side, rotation=0, color="white", thickness=0, show_center=False):
        radius = 0.866*side/cos(pi/6)
        super().__init__(pos, [(radius * cos(pi*i/3), radius * sin(pi*i/3)) for i in range(6)], rotation, color, thickness, show_center)

class Rectangle(Polygon):
    def __init__(self, pos, width, height, rotation=0, color="white", thickness=0, show_center=False):
        super().__init__(pos, ((-width/2, height/2), (width/2, height/2), (width/2, -height/2), (-width/2, -height/2)), rotation, color, thickness, show_center)

class Square(Rectangle):
    def __init__(self, pos, side, rotation=0, color="white", thickness=0, show_center=False):
        super().__init__(pos, side, side, rotation, color, thickness, show_center)

class Circle:
    def __init__(self, pos, radius, color="white", thickness=0, show_center=False):
        self.pos = vec2(pos)
        self.color = color
        self.radius = radius
        self.thickness = thickness
        self.show_center = show_center

    def draw(self, pg, screen):
        if self.show_center:
            pg.draw.circle(screen, "red", self.pos.get(), 2)
        pg.draw.circle(screen, self.color, self.pos.get(), self.radius, self.thickness)
