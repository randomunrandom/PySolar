from dataclasses import dataclass, astuple
from typing import Tuple, NamedTuple, List, Any
from numpy import sqrt, pi, hypot
import pygame

from .constants import YELLOW, T


@dataclass()
class vector_2d:
    x: float
    y: float


class Particle:
    cls_id: int = 1

    def __init__(
            self,
            color: Tuple[int, int, int],
            mass: float,
            x: float,
            y: float,
            v_x: float,
            v_y: float,
    ):
        self.coordinates: vector_2d = vector_2d(x, y)
        self.velocity: vector_2d = vector_2d(v_x, v_y)
        self.color: Tuple[int, int, int] = color
        self.mass: float = mass

        self.acceleration: vector_2d = vector_2d(0.0, 0.0)
        self.absorbed: bool = False
        self.interactable: List[Tuple[float, float, float]] = []
        self.id = Particle.cls_id
        Particle.cls_id += 1

    def __repr__(self) -> str:
        return f"Particle(color={self.color}, mass={self.mass}, coordinates={self.coordinates})"

    def __str__(self) -> str:
        return f"Particle of color {self.color} at {self.coordinates} with mass {self.mass}"

    def add_interactable(self, other: Any):
        # add object with which particle can interact
        self.interactable.append((other.mass, other.coordinates.x, other.coordinates.y))

    def update(self):
        self.calc_x()
        self.calc_y()
        del self.interactable[:]

    def fx(self, this_x: float):
        res = 0
        for (mass, x, y) in self.interactable:
            r = hypot(x - this_x, y - self.coordinates.y)
            res += mass * (x - this_x) / (r ** 3)
        return res

    def fy(self, this_y: float):
        res = 0
        for (mass, x, y) in self.interactable:
            r = hypot(x - self.coordinates.x, y - this_y)
            res += mass * (y - this_y) / r ** 3
        return res

    def calc_x(self):
        k_1 = T * self.fx(self.coordinates.x)
        q_1 = T * self.velocity.x

        k_2 = T * self.fx(self.coordinates.x + q_1 / 2)
        q_2 = T * (self.velocity.x + k_1 / 2)

        k_3 = T * self.fx(self.coordinates.x + q_2 / 2)
        q_3 = T * (self.velocity.x + k_2 / 2)

        k_4 = T * self.fx(self.coordinates.x + q_3)
        q_4 = T * (self.velocity.x + k_3)

        self.velocity.x += (k_1 + 2 * k_2 + 2 * k_3 + k_4) / 6
        self.coordinates.x += (q_1 + 2 * q_2 + 2 * q_3 + q_4) / 6

    def calc_y(self):
        k_1: float = T * self.fy(self.coordinates.y)
        q_1: float = T * self.velocity.y

        k_2: float = T * self.fy(self.coordinates.y + q_1 / 2)
        q_2: float = T * (self.velocity.y + k_1 / 2)

        k_3: float = T * self.fy(self.coordinates.y + q_2 / 2)
        q_3: float = T * (self.velocity.y + k_2 / 2)

        k_4: float = T * self.fy(self.coordinates.y + q_3)
        q_4: float = T * (self.velocity.y + k_3)

        self.velocity.y += (k_1 + 2 * k_2 + 2 * k_3 + k_4) / 6
        self.coordinates.y += (q_1 + 2 * q_2 + 2 * q_3 + q_4) / 6

    def position(self, scale: float = 1, x_offset: int = 0, y_offset: int = 0):
        x = int(round(self.coordinates.x * scale)) + x_offset
        y = int(round(self.coordinates.y * scale)) + y_offset
        return x, y

    def radius(self, scale: float = 1):
        return sqrt(self.mass * scale / pi)

    def int_radius(self, scale: float = 1):
        return int(round(sqrt(self.mass * scale / pi)))

    def display(self, screen: pygame.display, scale: float = 1, x_offset: int = 0, y_offset: int = 0):
        x, y = self.position()
        pygame.draw.circle(screen, self.color, self.position(scale, x_offset, y_offset), self.int_radius(scale))

