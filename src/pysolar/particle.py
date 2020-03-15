from dataclasses import dataclass, astuple
from typing import Tuple, NamedTuple, List, Any
from numpy import sqrt, pi
import pygame

from .constants import GRAVITY, MAX_SPEED

@dataclass()
class vector_2d:
    x: float
    y: float


class Particle:
    def __init__(
            self,
            color: Tuple[int, int, int],
            mass: float,
            coordinates: vector_2d = None,
            x: float = None,
            y: float = None,
            velocity: vector_2d = None,
            v_x: float = None,
            v_y: float = None,
    ):
        if (coordinates is None) and (x is not None) and (y is not None):
            self.coordinates: vector_2d = vector_2d(x, y)
        elif (x is None) and (y is None) and (coordinates is not None):
            self.coordinates: vector_2d = coordinates
        else:
            raise ValueError("Either `coordinates` or `x and y` should be present")

        if (velocity is None) and (v_x is not None) and (v_y is not None):
            self.velocity: vector_2d = vector_2d(v_x, v_y)
        elif (v_x is None) and (v_y is None) and (velocity is not None):
            self.velocity: vector_2d = velocity
        else:
            raise ValueError("Either `velocity` or `v_x and v_y` should be present")

        self.color: Tuple[int, int, int] = color
        self.mass: float = mass

        self.absorbed: bool = False

    @property
    def radius(self):
        return sqrt(self.mass / pi)

    @property
    def int_radius(self):
        return int(round(sqrt(self.mass / pi)))

    def position(self, resolution):
        x = int(round(self.coordinates.x + (resolution[0]/2)))
        y = int(round(self.coordinates.y + (resolution[1]/2)))
        return x, y

    def display(self, screen: pygame.display, bd_type: bool):
        w, h = screen.get_size()
        x, y = self.position((w, h))
        pygame.draw.circle(screen, self.color, (x, y), self.int_radius)
        if bd_type:
            r = self.radius
            if (x+r) >= (w - 10) or (x-r) <= 10:
                self.velocity.x *= -1
            if (y+r) >= (h - 10) or (y-r) <= 10:
                self.velocity.y *= -1
        else:
            if x > w or x < 0:
                self.absorbed = True
            if y > h or y < 0:
                self.absorbed = True

    def interaction(self, particles: List[Any]):
        ax: float = 0.0
        ay: float = 0.0
        for p in particles:
            if (p is self) or p.absorbed:
                continue
            dx: float = p.coordinates.x - self.coordinates.x
            dy: float = p.coordinates.y - self.coordinates.y
            dsq: float = (dx**2) + (dy**2)
            dr: float = sqrt(dsq)
            if (dr < self.radius) or (dr < p.radius):
                self.mass += p.mass
                p.absorbed = True
                self.velocity.x += p.velocity.x
                self.velocity.y += p.velocity.y
            else:
                force: float = 0.0 if dr < 1e-4 else GRAVITY*self.mass*p.mass/dsq
                ax += force * dx / dr
                ay += force * dy / dr
        self.velocity.x = min(self.velocity.x + ax, MAX_SPEED)
        self.velocity.y = min(self.velocity.y + ay, MAX_SPEED)
        self.coordinates.x += self.velocity.x
        self.coordinates.y += self.velocity.y

    def __repr__(self):
        return f"Particle(color={self.color}, mass={self.mass}, coordinates={self.coordinates})"

    def __str__(self):
        return f"Particle of color {self.color} at {self.coordinates} with mass {self.mass}"
