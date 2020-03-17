#!/usr/bin/env python3.8

from typing import List, Tuple

import pygame

from .constants import CAPTION, N
from .system import System

if __name__ == "__main__":
    pygame.init()
    pygame.display.init()
    pygame.font.init()

    info = pygame.display.Info()

    sys = System(CAPTION, N, preset="asdasd", follow=False)
    sys()

    pygame.quit()
