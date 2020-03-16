from typing import Tuple, List
import pygame

from numpy import sqrt, random, pi, cos, sin

from .constants import WHITE, BLUE, YELLOW
from .particle import Particle


class System:
    def __init__(
        self, resolution: Tuple[int, int], caption: str, n: int, * , seed: int = 42
    ):
        self.resolution = resolution
        self.caption = caption
        self.n = n

        random.seed(seed)

        self.omega_0 = 0.2

        self.particles = self.create_particles(self.n)

        self.sun: Particle = self.create_sun()

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
            particles.append(Particle(color=BLUE, mass=mass, x=x, y=y, v_x=v_x, v_y=v_y))
        return particles

    def create_sun(self):
        sun: Particle = self.create_particles(1)[0]
        sun.color = YELLOW
        sun.mass = 30
        sun.coordinates.x = 0
        sun.coordinates.y = 0
        return sun

    def __call__(self):
        screen = pygame.display.set_mode(self.resolution)
        clock = pygame.time.Clock()

        pygame.display.flip()
        clock.tick(3)

        pygame.display.set_caption(self.caption)

        scale: float = 1
        x_offset: int = self.resolution[0] // 2
        y_offset: int = self.resolution[1] // 2

        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for p in self.create_particles(self.n):
                            self.particles.append(p)
                    elif event.button == 3:
                        self.particles = []
                        self.sun = self.create_sun()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_PLUS) or (event.key == pygame.K_EQUALS):
                        scale += 0.1
                    elif (event.key == pygame.K_MINUS) or (event.key == pygame.K_UNDERSCORE):
                        scale -= 0.1
                    elif (event.key == pygame.K_w) or (event.key == pygame.K_UP):
                        y_offset -= 1
                    elif (event.key == pygame.K_s) or (event.key == pygame.K_DOWN):
                        y_offset += 1
                    elif (event.key == pygame.K_a) or (event.key == pygame.K_LEFT):
                        x_offset -= 1
                    elif (event.key == pygame.K_d) or (event.key == pygame.K_RIGHT):
                        x_offset += 1

            screen.fill(WHITE)
            # print(scale)
            self.sun.display(screen, scale, x_offset, y_offset)

            for p in self.particles:
                if p.absorbed:
                    continue
                p.display(screen, scale, x_offset, y_offset)
                # p.interaction([*self.particles, self.sun])
            # self.sun.interaction(self.particles)
            pygame.display.update()

            # print(len([p for p in self.particles if not p.absorbed]))


