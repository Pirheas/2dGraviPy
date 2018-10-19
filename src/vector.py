
class Vector:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: 'Vector') -> 'Vector':
        self.x += other.x
        self.y += other.y
        return self
