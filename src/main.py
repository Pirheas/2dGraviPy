from src.body import Body
from src.gui import Gui
from src.constants import *


def main():
    bodies = []
    sun = Body('Sun', 1.9885e30, 0, 0, 0, 0, 'YELLOW')
    sun.radius = 8
    bodies.append(sun)
    bodies.append(Body('Earth', 5.9736e24, UA, 0, 0, -29_763, 'LIGHT_BLUE'))
    bodies.append(Body('Mars', 641.85e21, -227_936_637_000, 0, 0, 24_077, 'RED'))
    bodies.append(Body('Jupiter', 1.8986e27, 0, 778_412_027_000, 13_057.2, 0, 'ORANGE'))
    bodies[-1].radius = 4
    bodies.append(Body('Venus', 4.8685e24, 0, -108_208_930_000, -35_020.0, 0, 'PINK'))
    bodies.append(Body('Mercury', 3.3011e23, 57_909_176_000, 0, 0, -47_360, 'LIGHT_GREEN'))
    g = Gui(bodies)
    g.start()

if __name__ == "__main__":
    main()