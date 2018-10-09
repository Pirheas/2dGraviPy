import math
from src.constants import *
from src.globals import GL
from src.vector import Vector
from typing import Union, Tuple


class Body:

    def __init__(self, name: str, mass: float, posx: float, posy: float, velx: float, vely: float,
                 color: Union[str, Tuple[int, int , int], None]):
        self.name = name
        self.mass = mass
        self.posx = posx
        self.posy = posy
        self.velocity = Vector(velx, vely)
        self.color = color
        self._forces_applied = []
        self._previous_pos = []
        self.velocity_change = []
        self.radius = 2

    def __str__(self) -> str:
        return f"[{self.name}] position: ({self.posx / UA}, {self.posy / UA}), velocity: ({self.velocity.x} km/s, {self.velocity.y} km/s)"

    def _compute_distance(self, other: 'Body') -> float:
        x = (self.posx - other.posx) ** 2
        y = (self.posy - other.posy) ** 2
        return (x + y) ** 0.5

    def compute_gravity(self, other: 'Body') -> None:
        distance = self._compute_distance(other)
        force = G * (self.mass * other.mass) / (distance ** 2)
        theta = math.atan2(other.posy - self.posy, other.posx - self.posx)
        dx = (force * math.cos(theta))
        dy = force * math.sin(theta)
        if PRINT_DEBUG:
            print(f"'{other.name}' applies a force: [{force}]({dx}, {dy})  on '{self.name}'")
        self._forces_applied.append(Vector(dx, dy))

    def update_positon(self) -> None:
        if PRINT_DEBUG:
            print(f"UPDATE POSITION: {self.name}")
            print(str(self))
        self._previous_pos.append((self.posx, self.posy))
        if len(self._previous_pos) > MAX_PREV_POS:
            self._previous_pos.pop(0)
        self.velocity_change.clear()
        for f in self._forces_applied:
            vel_change = Vector(f.x * GL.TIMESCALE / self.mass, f.y * GL.TIMESCALE / self.mass)
            self.velocity_change.append(vel_change)
            self.velocity += vel_change
        self._forces_applied = []
        self.posx += self.velocity.x * GL.TIMESCALE
        self.posy += self.velocity.y * GL.TIMESCALE
        if PRINT_DEBUG:
            print("NEW POSITION:", str(self))


    @property
    def color(self) -> Tuple[int, int, int]:
        return self._color

    @color.setter
    def color(self, value: Union[str, Tuple[int, int , int], None]):
        default_value =  STRING_COLORS['WHITE']
        if value is None:
            self._color = default_value
        elif isinstance(value, str):
            if value.upper() in STRING_COLORS:
                self._color = STRING_COLORS[value.upper()]
            else:
                self._color = default_value
        elif isinstance(value, tuple):
            self.color = value
        else:
            self._color = default_value
