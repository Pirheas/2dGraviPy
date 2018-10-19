from constants import *


class Globals:
    def __init__(self):
        self.SCALE = 90 / UA  # (90px == 1 UA)
        self.DRAW_SCALE = True
        self.TIMESCALE = 1.0
        self.FRAME_COMPUTE = 1.0
        self.INNER_TIMESCALE = 1.0
        self.SPEEDS = [
            (1, 1),
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
            (5_000_000, 72),
            (10_000_000, 86),
            (25_000_000, 96),
            (50_000_000, 116)
        ]
        self.CURRENT_SPEED = len(self.SPEEDS) // 2
        self.FOCUS_BODY = None
        self.PLAY_SOUND = False
        self.update_speed()

    def update_speed(self) -> None:
        self.TIMESCALE = self.SPEEDS[self.CURRENT_SPEED][0] / FRAME_RATE
        self.FRAME_COMPUTE = self.SPEEDS[self.CURRENT_SPEED][1]
        self.INNER_TIMESCALE = self.TIMESCALE / self.FRAME_COMPUTE


GL = Globals()
