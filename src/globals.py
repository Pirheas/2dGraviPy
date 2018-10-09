from src.constants import *

class Globals:
    def __init__(self):
        self.SCALE = 90 / UA  # (90px == 1 UA)
        self.SPEEDS = [
            166.66666667,
            416.66666667,
            833.33333334,
            1666.6666667,
            4166.6666667,
            8333.3333334,
            16666.666667,
            41666.666667,
            83333.333334,
            166666.66667,
            416666.66667,
            # 833333.33334,
            # 1666666.6667
        ]
        self.CURRENT_SPEED = len(self.SPEEDS) // 2
        self.TIMESCALE = self.SPEEDS[self.CURRENT_SPEED]

GL = Globals()