from src.constants import *

class Globals:
    def __init__(self):
        self.SCALE = 90 / UA  # (90px == 1 UA)
        self.SPEEDS = [
            10_000,
            25_000,
            50_000,
            100_000,
            250_000,
            500_000,
            1_000_000,
            2_500_000,
            5_000_000,
            10_000_000,
            25_000_000
        ]
        self.CURRENT_SPEED = len(self.SPEEDS) // 2
        self.TIMESCALE = self.get_speed()

    def get_speed(self) -> float:
        return self.SPEEDS[self.CURRENT_SPEED] / FRAME_RATE

GL = Globals()