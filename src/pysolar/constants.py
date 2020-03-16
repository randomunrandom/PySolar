"""
configuration
"""
CAPTION = "Kireev Danil"
N = 100
T = 1

"""
colors
"""
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

"""
presets
"""
from .particle import Particle

presets = {
    "solar": [
        Particle(color=YELLOW, mass=4000, radius=15, x=0, y=0, v_x=0, v_y=0),
        Particle(color=BLUE, mass=10, radius=3, x=100, y=0, v_x=0, v_y=4.5),
    ]
}
