from typing import Tuple, List
import pygame

from numpy import sqrt, random, pi, cos, sin

from .constants import WHITE, BLUE
from .particle import Particle


class System:
    def __init__(
        self, resolution: Tuple[int, int], caption: str, n: int, *, boundaries: bool = False, seed: int = 42
    ):
        self.resolution = resolution
        self.caption = caption
        self.n = n
        self.boundaries = boundaries

        random.seed(seed)

        self.omega_0 = 0.2

        self.particles = []
        self.create_particles()

    def create_particles(self):
        r_0 = min(*self.resolution) // 2
        self.particles = []
        for i in range(self.n):
            mass = random.randint(1, 10_00) / 1_00
            r = r_0 * sqrt(random.randint(1, 1000) / 1000)
            alpha = 2 * pi * (random.randint(1, 1000) / 1000)
            x = r * cos(alpha)
            y = r * sin(alpha)
            # v_x = -1 * y * self.omega_0 * (power(r_0 / r, 3 / 2))
            # v_y =      x * self.omega_0 * (power(r_0 / r, 3 / 2))
            v_x = random.randint(-2000, 2000) / 1000
            v_y = random.randint(-2000, 2000) / 1000
            self.particles.append(Particle(color=BLUE, mass=mass, x=x, y=y, v_x=v_x, v_y=v_y))

    def __call__(self):
        screen = pygame.display.set_mode(self.resolution)
        clock = pygame.time.Clock()

        pygame.display.flip()
        clock.tick(1)

        pygame.display.set_caption(self.caption)

        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            screen.fill(WHITE)
            for p in self.particles:
                if p.absorbed:
                    continue
                p.interaction(self.particles)
                p.display(screen, bd_type=self.boundaries)

            pygame.display.update()

            print(len([p for p in self.particles if not p.absorbed]))


