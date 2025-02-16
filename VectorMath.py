from math import sqrt, atan2, sin, cos

class vec2:
    def __init__(self, *args):
        if len(args) == 2:
            self.x, self.y = float(args[0]), float(args[1])
        elif isinstance(args[0], (tuple, list)) and len(args[0]) == 2:
            self.x, self.y = float(args[0][0]), float(args[0][1])
        else:
            self.x, self.y = 0.0, 0.0

        # Pre-compute length and squared length
        self._length = None
        self._length_squared = None

    def __repr__(self):
        return f"vec2({self.x}, {self.y})"

    def _update_length(self):
        if self._length is None or self._length_squared is None:
            self._length_squared = self.x ** 2 + self.y ** 2
            self._length = sqrt(self._length_squared)

    def dot(self, other: 'vec2') -> float:
        return self.x * other.x + self.y * other.y

    __matmul__ = dot

    def __sub__(self, other: 'vec2') -> 'vec2':
        return vec2(self.x - other.x, self.y - other.y)

    def __add__(self, other: 'vec2') -> 'vec2':
        return vec2(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> 'vec2':
        return vec2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> 'vec2':
        return self.__mul__(scalar)

    def __neg__(self) -> 'vec2':
        return vec2(-self.x, -self.y)

    def __truediv__(self, scalar: float) -> 'vec2':
        return vec2(self.x / scalar, self.y / scalar)

    def __mod__(self, scalar: float) -> 'vec2':
        return vec2(self.x % scalar, self.y % scalar)

    def length(self) -> float:
        self._update_length()
        return self._length

    def __abs__(self) -> 'vec2':
        return vec2(abs(self.x), abs(self.y))

    def distance_to(self, other: 'vec2') -> float:
        return (self - other).length()

    def to_polar(self) -> (float, float):
        self._update_length()
        return self.length(), atan2(self.y, self.x)

    def get(self) -> (float, float):
        return self.x, self.y

    def normalize(self) -> 'vec2':
        length = self.length()
        if length == 0:
            return vec2(0, 0)  # Avoid division by zero
        return self / length
    
    def rotate(self, theta) -> 'vec2':
        self.x = self.x*cos(theta) + self.y*sin(theta)
        self.y = -self.x*sin(theta) + self.y*cos(theta)
        return self

class VectorZero(vec2):
    def __init__(self):
        super().__init__(0, 0)
