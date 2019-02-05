import pygame as pg
import colors
from enum import Enum
from typing import Tuple
from constants import *
from globals import GL


class MenuChoice(Enum):
    NOTHING = 0
    SOLAR_SYSTEM = 1
    PLUTO_SYSTEM = 2
    BINARY_SYSTEM = 3
    CHANGE_MUSIC = -1


def show_menu(screen) -> MenuChoice:
    btns = [
        MenuButton(colors.MENU_FOREGROUND, colors.MENU_FOREGROUND_HOVER, 120, 60, 50, 'Solar System',
                   colors.DEFAULT_FONT_COLOR, MenuChoice.SOLAR_SYSTEM),
        MenuButton((173, 20, 87), (227, 81, 131), 200, 60, 50, 'Pluto System',
                   colors.DEFAULT_FONT_COLOR, MenuChoice.PLUTO_SYSTEM),
        MenuButton((0, 105, 92), (67, 152, 137), 280, 60, 50, 'Binary Star System',
                   colors.DEFAULT_FONT_COLOR, MenuChoice.BINARY_SYSTEM),
        MenuButton((239, 108, 0), (255, 157, 63), 365, 60, 40, 'Music: On',
                   colors.DEFAULT_FONT_COLOR, MenuChoice.CHANGE_MUSIC, half=True),
    ]
    ftitle = pg.font.Font(str(ROBOTO_BOLD_FONT_PATH), 34, bold=True).render("2dGraviPy", True, colors.WHITE)
    pg.mixer.music.load(str(MENU_MUSIC))
    pg.mixer.music.set_volume(0.85)
    if GL.PLAY_SOUND:
        pg.mixer.music.play(-1)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return MenuChoice.NOTHING
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    clickpos = pg.mouse.get_pos()
                    for btn in btns:
                        if btn.value is not None and btn.value != MenuChoice.NOTHING:
                            if btn.coordinate_in_button(clickpos[0], clickpos[1]):
                                if btn.value == MenuChoice.CHANGE_MUSIC:
                                    GL.PLAY_SOUND = not GL.PLAY_SOUND
                                    if GL.PLAY_SOUND:
                                        btn.text = 'Music: On'
                                        pg.mixer.music.play(-1)
                                    else:
                                        btn.text = 'Music: Off'
                                        pg.mixer.music.stop()
                                else:
                                    return btn.value
            elif event.type == pg.VIDEORESIZE:
                width, height = event.size
                width = max(380, width)
                height = max(415, height)
                screen = pg.display.set_mode((width, height), pg.RESIZABLE | pg.DOUBLEBUF)
        screen.fill(colors.MENU_BACKGROUND)
        for btn in btns:
            btn.draw(screen)
        title_rect = ftitle.get_rect()
        titleposx = round(screen.get_width() / 2 - title_rect.width / 2)
        screen.blit(ftitle, (titleposx, 30))
        pg.display.flip()


class MenuButton:

    def __init__(self, color: Tuple[int, int, int], hover_color: Tuple[int, int, int],
                 vertical_position: int, horizontal_margin: int, height: int,
                 text: str, text_color: Tuple[int, int, int], value: MenuChoice, font_size: int=25, half: bool=False):
        self.color = color
        self.text_colot = text_color
        self.hover_color = hover_color
        self.vposition = vertical_position
        self.height = height
        self.horizontal_margin = horizontal_margin
        self.text = text
        self.value = value
        self.pos_rect = None
        self.half = half
        self.font = pg.font.Font(str(ROBOTO_BOLD_FONT_PATH), font_size, bold=True)

    def draw(self, screen):
        if self.half:
            bwidth = (screen.get_width() - (self.horizontal_margin * 2)) // 2
            margin_left = self.horizontal_margin + bwidth
        else:
            bwidth = screen.get_width() - (self.horizontal_margin * 2)
            margin_left = self.horizontal_margin
        self.pos_rect = pg.Rect(margin_left, self.vposition, bwidth, self.height)
        mouse_posx, mouse_posy = pg.mouse.get_pos()
        bcolor = self.color
        if self.coordinate_in_button(mouse_posx, mouse_posy):
            bcolor = self.hover_color
        pg.draw.rect(screen, bcolor, self.pos_rect)
        if self.text:
            rtext = self.font.render(self.text, True, colors.DEFAULT_FONT_COLOR)
            text_rect = rtext.get_rect()
            tposx = round((self.pos_rect.width / 2) - (text_rect.width / 2) + self.pos_rect.x)
            tposy = round((self.pos_rect.height / 2) - (text_rect.height / 2) + self.pos_rect.y)
            screen.blit(rtext, (tposx, tposy,))

    def coordinate_in_button(self, posx, posy) -> bool:
        if self.pos_rect is None:
            return False
        return self.pos_rect.collidepoint(posx, posy)
