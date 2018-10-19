from typing import List
from body import Body
from gui import Gui
from globals import GL
from constants import *


def main():
    bodies = generate_solar_system()
    # bodies = generate_pluto_system()
    # bodies = generate_dual_stars_system()
    g = Gui(bodies)
    g.start()


def generate_solar_system() -> List[Body]:
    return [
        Body('Sun', 1.9885e30, 0, 0, -12.5, 0, 'YELLOW', 8),
        Body('Earth', 5.9736e24, UA, 0, 0, -29_763, 'LIGHT_BLUE', 3),
        Body('Mars', 641.85e21, -227_936_637_000, 0, 0, 24_077, 'RED'),
        Body('Jupiter', 1.8986e27, 0, 778_412_027_000, 13_057.2, 0, 'ORANGE', 6),
        Body('Venus', 4.8685e24, 0, -108_208_930_000, -35_020.0, 0, 'PINK', 3),
        Body('Mercury', 3.3011e23, 57_909_176_000, 0, 0, -47_360, 'LIGHT_GREEN'),
        Body('Moon', 7.3476731e22, UA, -384_400_000, -1_022, -29_763, 'LIGHT_GREY', 1),
        Body('Saturn', 5.6834e26, 0, -1_433_530_000_000, -9_068, 0, 'PURPLE', 4)
    ]


def generate_pluto_system() -> List[Body]:
    bodies = [
        Body('Pluto', 1.314e22, 0, 0, 0, 25.35, 'DARK_BLUE', 7),
        Body('Charon', 1.586e21, 17_536_000, 0, 0, -210, 'PURE_RED', 4),
        Body('Nix', 4.5e16, -48_694_000, 0, 0, 135, 'DARK_GREEN'),
        Body('Hydra', 4.8e16, 0, -64_738_000, -125, 0, 'ORANGE'),
        Body('Kerberos', 1.65e16, 0, 57_783_000, 128.5, 0, 'PINK')
    ]
    GL.SCALE = 110/17_536_000
    GL.CURRENT_SPEED = 3
    GL.update_speed()
    return bodies


def generate_dual_stars_system() -> List[Body]:
    bodies = [
        Body('Star 1', 1.5e30, 0.3 * UA, 0, 0, -15_800, 'PURE_BLUE', 6),
        Body('Star 2', 1.5e30, -0.3 * UA, 0, 0, 15_800, 'PURE_RED', 6),
        Body('planet', 5.78412e23, 0, 1.2 * UA, 33_800, 0, 'PURE_GREEN')
    ]
    GL.SCALE = 350 / UA
    return bodies


if __name__ == "__main__":
    if ENABLE_PROFILING:
        import cProfile
        pr = cProfile.Profile()
        pr.enable()
        main()
        pr.disable()
        pr.print_stats(sort='tottime')
    else:
        main()
