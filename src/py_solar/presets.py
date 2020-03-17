from .constants import *
from .particle import Particle

presets = {
    "simple": [
        Particle(color=YELLOW, mass=4000, radius=15, x=0, y=0, v_x=0, v_y=0),
        Particle(color=BLUE, mass=10, radius=3, x=100, y=0, v_x=0, v_y=4.5),
    ],
    "earth": [
        Particle(color=YELLOW, mass=10000, radius=20, x=0, y=0, v_x=0, v_y=0.1),
        Particle(color=BLUE, mass=170, radius=6, x=300, y=0, v_x=0, v_y=5),
        Particle(color=GREY, mass=10, radius=3, x=320, y=0, v_x=0, v_y=8),
    ],
    "simple_solar": [
        Particle(color=YELLOW, mass=4000, radius=15, x=0, y=0, v_x=0, v_y=0),
        Particle(color=BLUE, mass=10, radius=3, x=100, y=0, v_x=0, v_y=4.5),
    ],
    "solar": [
        Particle(color=YELLOW, mass=20_000, radius=15, x=0, y=0, v_x=0, v_y=0),
        Particle(color=WHITE, mass=10, radius=3, x=100, y=0, v_x=0, v_y=13),
        Particle(color=BLUE, mass=15, radius=4, x=200, y=0, v_x=0, v_y=10),
        Particle(color=LIGHT_BLUE, mass=250, radius=6, x=300, y=0, v_x=0, v_y=8),
        Particle(color=GREY, mass=2, radius=3, x=315, y=0, v_x=0, v_y=12),
        Particle(color=RED, mass=250, radius=5, x=450, y=0, v_x=0, v_y=7),
    ],
}
