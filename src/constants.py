from pathlib import Path

# The gravitational constant G
G = 6.67408e-11
# Astronomical unit (in meter)
UA = 149_597_870_700

ENABLE_PROFILING = False  # Make the program much slower when enabled
DEFAULT_WINDOW_SIZE = (1300, 800,)
DEFAULT_WINDOW_MENU_SIZE = (500, 450,)

MAX_PREV_POS = 1000
FRAME_RATE = 60.0

FONT_PATH = Path(__file__).parent.parent / 'fonts'
ROBOTO_FONT_PATH = FONT_PATH / 'Roboto-Regular.ttf'
ROBOTO_BOLD_FONT_PATH = FONT_PATH / 'Roboto-Bold.ttf'

MUSIC_PATH = Path(__file__).parent.parent / 'music'
MAIN_MUSIC = MUSIC_PATH / 'AmbiantSpace.ogg'
MENU_MUSIC = MUSIC_PATH / 'EarthPrelude.ogg'
