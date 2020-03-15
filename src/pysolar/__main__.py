from typing import List, Tuple
import pygame

from .system import System
from .constants import CAPTION, N

if __name__ == "__main__":
    pygame.init()
    pygame.display.init()

    info = pygame.display.Info()

    sys = System((int(round(info.current_w * 0.9)), int(round(info.current_h * 0.9))), CAPTION, N, boundaries=True)
    sys()

    pygame.quit()

