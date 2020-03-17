from typing import Tuple, List, Union
import time

import pygame
from numpy import sqrt, random, pi, cos, sin

from .constants import *
from .particle import Particle
from .presets import presets


class System:
    def __init__(
        self,
        resolution: Tuple[int, int],
        caption: str,
        n: int,
        *,
        seed: int = 42,
        preset: str = "random",
        folow: bool = False
    ):
        self.resolution = resolution
        self.caption = caption
        self.n = n
        self.folow = folow

        random.seed(seed)

        self.omega_0 = 0.2

        self.myfont = pygame.font.SysFont("Hack Nerd Font Mono", 12)

        if preset in [key for key in presets.keys()]:
            self.particles = presets[preset]
            self.folowing = lambda: max(self.particles, key=lambda el: el.radius)
        else:
            self.particles = self.create_particles(self.n)
            self.folowing = lambda: self.particles[0]

    def create_particles(self, n: int) -> List[Particle]:
        r_0 = min(*self.resolution) // 2
        particles = []
        for i in range(n):
            mass = random.randint(1_00, 100_00) / 1_00
            r = r_0 * sqrt(random.randint(1, 1000) / 1000)
            alpha = 2 * pi * (random.randint(1, 1000) / 1000)
            x = r * cos(alpha)
            y = r * sin(alpha)
            # v_x = -1 * y * self.omega_0 * (power(r_0 / r, 3 / 2))
            # v_y =      x * self.omega_0 * (power(r_0 / r, 3 / 2))
            v_x = random.randint(-2000, 2000) / 1000
            v_y = random.randint(-2000, 2000) / 1000
            rad = random.randint(0, 10_000) / 1_000
            particles.append(
                Particle(color=BLUE, mass=mass, radius=rad, x=x, y=y, v_x=v_x, v_y=v_y)
            )
        return particles

    def __call__(self):
        screen = pygame.display.set_mode(self.resolution)
        clock = pygame.time.Clock()

        pygame.display.flip()
        clock.tick(30)

        pygame.display.set_caption(self.caption)

        scale: float = 1
        x_offset: int = self.resolution[0] // 2
        y_offset: int = self.resolution[1] // 2

        iterations: int = 0
        start = time.time()

        done = False
        while not done:
            iterations += 1
            keys = pygame.key.get_pressed()
            if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
                scale = round(scale + 0.01, 2)
            if keys[pygame.K_MINUS] or keys[pygame.K_UNDERSCORE]:
                scale = round(scale - 0.01, 2)
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                y_offset += 1
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                y_offset -= 1
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                x_offset += 1
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                x_offset -= 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for p in self.create_particles(self.n):
                            self.particles.append(p)
                    elif event.button == 3:
                        self.particles = []
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True

            screen.fill(WHITE)

            for p_i in self.particles:
                for p_j in self.particles:
                    if p_i is p_j:
                        continue

                    dr = p_i.dr(p_j)
                    if dr < p_i.radius:
                        p_i.absorb(p_j)
                        self.particles.remove(p_j)
                    else:
                        p_i.add_interactable(p_j)

            for p in self.particles:
                p.update()

            if self.folow:
                follow = self.folowing()
                x_offset = (self.resolution[0] // 2) - int(round(follow.coordinates.x))
                y_offset = (self.resolution[1] // 2) - int(round(follow.coordinates.x))

            for p in self.particles:
                p.display(screen, scale, x_offset, y_offset)

            textsurface = self.myfont.render(
                f"scale: {scale} | x offset: {x_offset} | y offset: {y_offset} | n: {len(self.particles)} | iterations "
                f"{iterations} | time {time.time()-start}",
                True,
                (0, 0, 0),
            )
            screen.blit(textsurface, (0, 0))
            pygame.display.update()

            # print(len([p for p in self.particles if not p.absorbed]))
