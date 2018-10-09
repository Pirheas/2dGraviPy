import pygame as pg
from src.constants import *
from src.globals import GL
from src.body import Body
from typing import  List, Tuple

if not PYGAME_INIT:
    PYGAME_INIT = True
    pg.init()

WINDOW_SIZE = (1300, 1000,)
DRAW_GHOST_LINE = False


class Gui:

    def __init__(self, bodies: List[Body]):
        self.exit = False
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        self.clock = pg.time.Clock()
        self.bodies = bodies
        self.bcolor = STRING_COLORS['BLACK']
        self.cfont = pg.font.SysFont("calibri", 12)
        self.speed_text = self._compute_speed_text()

    def start(self) -> None:
        global DRAW_GHOST_LINE
        global DRAW_GRAVITATIONAL_FORCES
        while not self.exit:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit = True
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        for body in self.bodies:
                            print(str(body))
                    elif event.key == pg.K_g:
                        DRAW_GHOST_LINE = not DRAW_GHOST_LINE
                    elif event.key == pg.K_f:
                        DRAW_GRAVITATIONAL_FORCES = not DRAW_GRAVITATIONAL_FORCES
                    elif event.key == pg.K_PLUS or event.key == pg.K_KP_PLUS:
                        self.timescale_faster()
                    elif event.key == pg.K_MINUS or event.key == pg.K_KP_MINUS:
                        self.timescale_slower()

            for i in range(0, len(self.bodies)):
                for j in range(0, len(self.bodies)):
                    if i != j:
                        self.bodies[i].compute_gravity(self.bodies[j])
            for body in self.bodies:
                body.update_positon()
            self.screen.fill(self.bcolor)
            if DRAW_GHOST_LINE:
                self._draw_ghost()
            if DRAW_GRAVITATIONAL_FORCES:
                self._draw_gravitational_forces()
            self._draw_bodies()
            self._draw_speed_text()
            pg.display.flip()
            self.clock.tick(FRAME_RATE)
        pg.quit()

    def _draw_bodies(self):
        for body in self.bodies:
            pos = self._get_screen_position(body.posx, body.posy)
            pg.draw.circle(self.screen, body.color, pos, body.radius)

    def _draw_ghost(self):
        for body in self.bodies:
            for i in range(0, len(body._previous_pos) - 1):
                p1 = self._get_screen_position(body._previous_pos[i][0], body._previous_pos[i][1])
                p2 = self._get_screen_position(body._previous_pos[i+1][0], body._previous_pos[i+1][1])
                pg.draw.line(self.screen, body.color, p1, p2)

    def _draw_gravitational_forces(self):
        for body in self.bodies:
            for force in body.velocity_change:
                p1 = self._get_screen_position(body.posx, body.posy)
                p2 = p1[0] + int(force.x * 5000), p1[1] + int(force.y * 5000)
                pg.draw.aaline(self.screen, (255, 255, 255), p1, p2)

    def _draw_speed_text(self):
        text = self.cfont.render(self.speed_text, True, (210, 210, 210))
        self.screen.blit(text, (10, 10,))

    def timescale_faster(self):
        if GL.CURRENT_SPEED >= len(GL.SPEEDS) - 1:
            return
        GL.CURRENT_SPEED += 1
        GL.TIMESCALE = GL.SPEEDS[GL.CURRENT_SPEED]
        self.speed_text = self._compute_speed_text()

    def timescale_slower(self):
        if GL.CURRENT_SPEED <= 0:
            return
        GL.CURRENT_SPEED -= 1
        GL.TIMESCALE = GL.SPEEDS[GL.CURRENT_SPEED]
        self.speed_text = self._compute_speed_text()

    def _compute_speed_text(self) -> str:
        speed_mult = int(round(GL.TIMESCALE * FRAME_RATE))
        return f"Speed: {speed_mult:,}X"

    def _get_screen_position(self, x: float, y: float) -> Tuple[int, int]:
        xp = int(x * GL.SCALE)
        yp = int(y * GL.SCALE)
        xp += WINDOW_SIZE[0] // 2
        yp += WINDOW_SIZE[1] // 2
        return (xp, yp,)





