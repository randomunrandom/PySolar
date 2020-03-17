from dataclasses import astuple, dataclass
from typing import List, NoReturn, Tuple

import pygame
from numpy import hypot, pi, sqrt

from .constants import *


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
        radius: float,
        x: float,
        y: float,
        v_x: float,
        v_y: float,
    ):
        self.coordinates: vector_2d = vector_2d(x, y)
        self.velocity: vector_2d = vector_2d(v_x, v_y)
        self.color: Tuple[int, int, int] = color
        self.mass: float = mass
        self.radius: float = radius

        self.acceleration: vector_2d = vector_2d(0.0, 0.0)
        self.interactable: List[Tuple[float, float, float]] = []

    def __repr__(self) -> str:
        return f"Particle(color={self.color}, mass={self.mass}, coordinates={self.coordinates})"

    def __str__(self) -> str:
        return f"Particle of color {self.color} at {self.coordinates} with mass {self.mass}"

    def add_interactable(self, p: "Particle") -> NoReturn:
        self.interactable.append((p.mass, p.coordinates.x, p.coordinates.y))

    def update(self) -> NoReturn:
        self.calc_x()
        self.calc_y()
        del self.interactable[:]

    def fx(self, this_x: float) -> float:
        res = 0.0
        for (mass, x, y) in self.interactable:
            r = hypot(x - this_x, y - self.coordinates.y)
            res += G * mass * (x - this_x) / (r ** 3)
        return res

    def fy(self, this_y: float) -> float:
        res = 0.0
        for (mass, x, y) in self.interactable:
            r = hypot(x - self.coordinates.x, y - this_y)
            res += G * mass * (y - this_y) / r ** 3
        return res

    def calc_x(self) -> NoReturn:
        k_1: float = self.fx(self.coordinates.x)
        q_1: float = self.velocity.x

        k_2: float = self.fx(self.coordinates.x + q_1 / 2)
        q_2: float = (self.velocity.x + k_1 / 2)
        
        k_3: float = self.fx(self.coordinates.x + q_2 / 2)
        q_3: float = (self.velocity.x + k_2 / 2)
        
        k_4: float = self.fx(self.coordinates.x + q_3)
        q_4: float = (self.velocity.x + k_3)

        self.velocity.x += T * (k_1 + 2 * k_2 + 2 * k_3 + k_4) / 6
        self.coordinates.x += T * (q_1 + 2 * q_2 + 2 * q_3 + q_4) / 6

    def calc_y(self):
        k_1: float = self.fy(self.coordinates.y)
        q_1: float = self.velocity.y

        q_2: float = (self.velocity.y + k_1 / 2)
        k_2: float = self.fy(self.coordinates.y + q_1 / 2)
        
        k_3: float = self.fy(self.coordinates.y + q_2 / 2)
        q_3: float = (self.velocity.y + k_2 / 2)
        
        k_4: float = self.fy(self.coordinates.y + q_3)
        q_4: float = (self.velocity.y + k_3)

        self.velocity.y += T * (k_1 + 2 * k_2 + 2 * k_3 + k_4) / 6
        self.coordinates.y += T * (q_1 + 2 * q_2 + 2 * q_3 + q_4) / 6

    def position(self, scale: float = 1, x_offset: int = 0, y_offset: int = 0):
        x = int(round(self.coordinates.x * scale)) + x_offset
        y = int(round(self.coordinates.y * scale)) + y_offset
        return x, y

    def dr(self, p: "Particle") -> float:
        return hypot(
            (self.coordinates.x - p.coordinates.x),
            (self.coordinates.y - p.coordinates.y),
        )

    def display(
        self,
        screen: pygame.display,
        scale: float = 1,
        x_offset: int = 0,
        y_offset: int = 0,
    ) -> NoReturn:
        x: int
        y: int
        x, y = self.position()
        pygame.draw.circle(
            screen,
            self.color,
            self.position(scale, x_offset, y_offset),
            int(round(self.radius * scale)),
        )

    def absorb(self, p: "Particle") -> NoReturn:
        new_mass = self.mass + p.mass
        self.coordinates.x = (
            self.coordinates.x * self.mass + p.coordinates.x * p.mass
        ) / new_mass
        self.coordinates.y = (
            self.coordinates.y * self.mass + p.coordinates.y * p.mass
        ) / new_mass

        self.velocity.x = (
            self.velocity.x * self.mass + p.velocity.x * p.mass
        ) / new_mass
        self.velocity.y = (
            self.velocity.y * self.mass + p.velocity.y * p.mass
        ) / new_mass

        if p.mass > self.mass:
            self.color = p.color

        self.mass = new_mass
        self.radius = sqrt((self.radius ** 2) + (p.radius ** 2))
