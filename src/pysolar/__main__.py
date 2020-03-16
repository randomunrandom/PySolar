from typing import List, Tuple
import pygame

from .system import System
from .constants import CAPTION, N

if __name__ == "__main__":
    pygame.init()
    pygame.display.init()
    pygame.font.init()

    info = pygame.display.Info()

    sys = System((1300, 700), CAPTION, N, preset="solar")
    sys()

    pygame.quit()
