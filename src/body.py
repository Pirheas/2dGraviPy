import math
import colors
from constants import *
from globals import GL
from vector import Vector
from typing import Union, Tuple


class Body:

    def __init__(self, name: str, mass: float, posx: float, posy: float, velx: float, vely: float,
                 color: Union[str, Tuple[int, int, int], None], radius: int=2):
        self.name = name
        self.mass = mass
        self.posx = posx
        self.posy = posy
        self.velocity = Vector(velx, vely)
        self.color = color
        self._forces_applied = []
        self._previous_pos = []
        self.velocity_change = []
        self.radius = radius
        self.selected = False
        self.Gmass = G * self.mass

    def __str__(self) -> str:
        return f"[{self.name}] position: ({self.posx / UA}, {self.posy / UA}), " \
               f"velocity: ({self.velocity.x} km/s, {self.velocity.y} km/s)"

    def _compute_distance(self, other: 'Body') -> float:
        x = (self.posx - other.posx) ** 2
        y = (self.posy - other.posy) ** 2
        return (x + y) ** 0.5

    def _compute_square_distance(self, other: 'Body') -> float:
        return (self.posx - other.posx) ** 2 + (self.posy - other.posy) ** 2

    def compute_gravity(self, other: 'Body') -> None:
        sq_distance = self._compute_square_distance(other)
        force = (self.Gmass * other.mass) / sq_distance
        theta = math.atan2(other.posy - self.posy, other.posx - self.posx)
        dx = (force * math.cos(theta))
        dy = force * math.sin(theta)
        self._forces_applied.append(Vector(dx, dy))
        other._forces_applied.append(Vector(-1 * dx, -1 * dy))

    def update_positon(self, save_prev_pos: bool=False) -> None:
        if save_prev_pos:
            self._previous_pos.append((self.posx, self.posy))
            if len(self._previous_pos) > MAX_PREV_POS:
                self._previous_pos.pop(0)
        self.velocity_change.clear()
        for f in self._forces_applied:
            vel_change = Vector(f.x * GL.INNER_TIMESCALE / self.mass, f.y * GL.INNER_TIMESCALE / self.mass)
            self.velocity_change.append(vel_change)
            self.velocity += vel_change
        self._forces_applied = []
        self.posx += self.velocity.x * GL.INNER_TIMESCALE
        self.posy += self.velocity.y * GL.INNER_TIMESCALE

    @property
    def color(self) -> Tuple[int, int, int]:
        return self._color

    @color.setter
    def color(self, value: Union[str, Tuple[int, int, int], None]):
        default_value = colors.WHITE
        if value is None:
            self._color = default_value
        elif isinstance(value, str):
            self._color = getattr(colors, value.upper(), default_value)
        elif isinstance(value, tuple):
            self.color = value
        else:
            self._color = default_value
