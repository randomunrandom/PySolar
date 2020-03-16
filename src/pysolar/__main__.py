from typing import List, Tuple
import pygame

from .system import System
from .constants import CAPTION, N

if __name__ == "__main__":
    pygame.init()
    pygame.display.init()

    info = pygame.display.Info()

    sys = System((1300, 500), CAPTION, N)
    sys()

    pygame.quit()

