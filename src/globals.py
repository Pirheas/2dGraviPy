from constants import *

class Globals:
    def __init__(self):
        self.SCALE = 90 / UA  # (90px == 1 UA)
        self.SPEEDS = [
            (1_000, 2),
            (5_000, 4),
            (10_000, 8),
            (25_000, 16),
            (50_000, 24),
            (100_000, 32),
            (250_000, 40),
            (500_000, 48),
            (1_000_000, 56),
            (2_500_000, 64),
            (5_000_000, 82),
            (10_000_000, 96),
            (25_000_000, 124)
        ]
        self.CURRENT_SPEED = len(self.SPEEDS) // 2
        self.update_speed()

    def update_speed(self) -> None:
        self.TIMESCALE = self.SPEEDS[self.CURRENT_SPEED][0] / FRAME_RATE
        self.FRAME_COMPUTE = self.SPEEDS[self.CURRENT_SPEED][1]
        self.INNER_TIMESCALE = self.TIMESCALE / self.FRAME_COMPUTE

GL = Globals()