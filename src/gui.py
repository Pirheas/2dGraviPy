import sys
import math
import pygame as pg
from constants import *
from globals import GL
from body import Body
from typing import  List, Tuple, Union

if not PYGAME_INIT:
    PYGAME_INIT = True
    pg.init()
    pg.display.set_caption('2dGraviPy')

WINDOW_SIZE = (1300, 1000,)
DRAW_GHOST_LINE = False


class Gui:

    def __init__(self, bodies: List[Body]):
        self.exit = False
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        self.clock = pg.time.Clock()
        self.bodies = bodies
        self.selected_body = None
        self.capture_counter = 0
        self.load_music()
        self.bcolor = STRING_COLORS['BLACK']
        self.cfont = pg.font.SysFont("calibri", 13)
        self.bfont = pg.font.SysFont("calibri", 17, bold=True)
        self.efont = pg.font.SysFont("calibri", 26)
        self.speed_text = self._compute_speed_text()

    def load_music(self):
        try:
            from pathlib import Path
            p = Path(__file__).parent.parent / 'music' / 'AmbiantSpace.ogg'
            pg.mixer.music.load(str(p))
            pg.mixer.music.set_volume(0.6)
        except:
            print("Oh oh", file=sys.stderr)

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
                    elif event.key == pg.K_s:
                        GL.DRAW_SCALE = not GL.DRAW_SCALE
                    elif event.key == pg.K_v:
                        self.change_music_state()
                elif event.type == pg.MOUSEBUTTONUP:
                    clickpos = pg.mouse.get_pos()
                    if event.button == 1: # Left click
                        self.select_body(clickpos[0], clickpos[1])
                    elif event.button == 3: # Right click
                        self.center_body(clickpos[0], clickpos[1])

            self.selected_body = None
            for fc in range(GL.FRAME_COMPUTE):
                for i in range(0, len(self.bodies)):
                    for j in range(0, len(self.bodies)):
                        if i != j:
                            self.bodies[i].compute_gravity(self.bodies[j])
                for body in self.bodies:
                    body.update_positon(fc == GL.FRAME_COMPUTE - 1)
            self.screen.fill(self.bcolor)
            if GL.DRAW_SCALE:
                self.draw_scale()
            if DRAW_GHOST_LINE:
                self._draw_ghost()
            if DRAW_GRAVITATIONAL_FORCES:
                self._draw_gravitational_forces()
            self._draw_bodies()
            if self.selected_body:
                self.print_body_properties()
            self._draw_speed_text()
            self.draw_focus_info()
            self.draw_music_info()
            pg.display.flip()
            self.capture_img()
            self.clock.tick(FRAME_RATE)
        pg.quit()


    def select_body(self, x: int, y: int):
        for body in self.bodies:
            body.selected = False
        closest_body = self.find_closest_body_from_position(x, y)
        if closest_body is not None:
            closest_body.selected = True

    def center_body(self, x: int, y: int):
        GL.FOCUS_BODY = self.find_closest_body_from_position(x, y)

    def find_closest_body_from_position(self, x: int, y: int, max_allowed_dist: float=10.0) -> Union[Body, None]:
        if len(self.bodies) < 1:
            return None
        min_dist = None
        min_index = -1
        for i in range(len(self.bodies)):
            body = self.bodies[i]
            bpos = self._real_to_screen(body.posx, body.posy)
            dist = ((x - bpos[0]) ** 2 + (y - bpos[1]) ** 2) ** 0.5
            if min_dist is None or dist < min_dist:
                min_dist = dist
                min_index = i
        if min_dist > max_allowed_dist:
            return None
        return self.bodies[min_index]

    def _draw_bodies(self):
        for body in self.bodies:
            pos = self._real_to_screen(body.posx, body.posy)
            pg.draw.circle(self.screen, body.color, pos, body.radius)
            if body.selected:
                self.draw_ngon(8, body.radius + 4, pos, math.pi / 16)
                self.selected_body = body

    def _draw_ghost(self):
        for body in self.bodies:
            for i in range(0, len(body._previous_pos) - 1):
                p1 = self._real_to_screen(body._previous_pos[i][0], body._previous_pos[i][1])
                p2 = self._real_to_screen(body._previous_pos[i + 1][0], body._previous_pos[i + 1][1])
                pg.draw.line(self.screen, body.color, p1, p2)

    def _draw_gravitational_forces(self):
        for body in self.bodies:
            for force in body.velocity_change:
                p1 = self._real_to_screen(body.posx, body.posy)
                p2 = p1[0] + int(force.x * 5000), p1[1] + int(force.y * 5000)
                pg.draw.aaline(self.screen, (255, 255, 255), p1, p2)

    def _draw_speed_text(self):
        text = self.cfont.render(self.speed_text, True, (210, 210, 210))
        self.screen.blit(text, (10, 10,))

    def draw_ngon(self, n: int, radius: int, position: Tuple[float, float], tiltAngle: float):
        pi2 = 2 * math.pi
        color = (255, 255, 255)
        pts = []
        for i in range(n):
            x = position[0] + radius * math.cos(tiltAngle + pi2 * i / n)
            y = position[1] + radius * math.sin(tiltAngle + pi2 * i / n)
            pts.append([int(x), int(y)])
        pg.draw.lines(self.screen, color, True, pts)

    def timescale_faster(self):
        if GL.CURRENT_SPEED >= len(GL.SPEEDS) - 1:
            return
        GL.CURRENT_SPEED += 1
        GL.update_speed()
        self.speed_text = self._compute_speed_text()

    def timescale_slower(self):
        if GL.CURRENT_SPEED <= 0:
            return
        GL.CURRENT_SPEED -= 1
        GL.update_speed()
        self.speed_text = self._compute_speed_text()

    def _compute_speed_text(self) -> str:
        speed_mult = int(round(GL.TIMESCALE * FRAME_RATE))
        return f"Speed: {speed_mult:,}X"


    def _real_to_screen(self, x: float, y: float) -> Tuple[int, int]:
        relative_pos = (0, 0,)
        if GL.FOCUS_BODY is not None:
            relative_pos = (GL.FOCUS_BODY.posx, GL.FOCUS_BODY.posy)
        xp = int((x - relative_pos[0]) * GL.SCALE)
        yp = int((y - relative_pos[1]) * GL.SCALE)
        xp += WINDOW_SIZE[0] // 2
        yp += WINDOW_SIZE[1] // 2
        return (xp, yp,)

    def print_body_properties(self):
        body = self.selected_body  # type: Body
        bname = self.bfont.render(body.name, True, body.color)
        masstxt = self.cfont.render(f'Mass: {body.mass} Kg', True, (210, 210, 210))
        xpostxt = self.cfont.render(f'Position X: {body.posx}', True, (210, 210, 210))
        ypostxt = self.cfont.render(f'Position Y: {body.posy}', True, (210, 210, 210))
        xvelo = self.cfont.render(f'Velocity X: {body.velocity.x:.3f} m/s', True, (210, 210, 210))
        yvelo = self.cfont.render(f'Velocity Y: {body.velocity.y:.3f} m/s', True, (210, 210, 210))
        velocity_total = (body.velocity.x ** 2 + body.velocity.y ** 2) ** 0.5
        totvelo = self.cfont.render(f'Velocity Total: {velocity_total:.3f} m/s', True, (210, 210, 210))
        self.screen.blit(bname, (10, 28,))
        self.screen.blit(masstxt, (10, 49,))
        self.screen.blit(xpostxt, (10, 66,))
        self.screen.blit(ypostxt, (10, 81,))
        self.screen.blit(xvelo, (10, 98,))
        self.screen.blit(yvelo, (10, 115,))
        self.screen.blit(totvelo, (10, 132,))

    def draw_scale(self):
        ref_length = 250
        color = (210, 210, 210)
        start_pos, end_pos = (10, WINDOW_SIZE[1] - (ref_length + 26)), (10, WINDOW_SIZE[1] - 26)
        pg.draw.line(self.screen, color, start_pos, end_pos)
        pg.draw.line(self.screen, color, start_pos, (start_pos[0] + 10, start_pos[1]))
        pg.draw.line(self.screen, color, end_pos, (end_pos[0] + 10, end_pos[1]))
        scale = (ref_length / GL.SCALE) / 1000
        scale_ua = (scale * 1000) / UA
        scale_text = self.cfont.render(f'{scale:,.4f} Km', True, color)
        scale_ua_text = self.cfont.render(f'{scale_ua:,.3f} UA', True, color)
        self.screen.blit(scale_text, (start_pos[0], start_pos[1] - 35,))
        self.screen.blit(scale_ua_text, (start_pos[0], start_pos[1] - 18,))

    def draw_focus_info(self):
        label_text = "Focus: "
        focus_text = str(GL.FOCUS_BODY.name) if GL.FOCUS_BODY is not None else 'None'
        focus_color = GL.FOCUS_BODY.color if GL.FOCUS_BODY is not None else (210, 210, 210,)
        focus_render = self.bfont.render(focus_text, True, focus_color)
        label_render = self.cfont.render(label_text, True, (210, 210, 210,))
        focus_rect = focus_render.get_rect()
        label_pos = ( WINDOW_SIZE[0] - 12 - focus_rect[2] - label_render.get_rect()[2] , 16)
        focus_pos = (WINDOW_SIZE[0] - 12 - focus_rect[2], 15)
        self.screen.blit(label_render, label_pos)
        self.screen.blit(focus_render, focus_pos)

    def draw_music_info(self):
        if GL.PLAY_SOUND:
            rtext = self.cfont.render('Music: On', True, (210, 210, 210))
        else:
            rtext = self.cfont.render('Music: Off', True, (210, 210, 210))
        self.screen.blit(rtext, (10, WINDOW_SIZE[1] - 18))

    def change_music_state(self):
        GL.PLAY_SOUND = not GL.PLAY_SOUND
        if GL.PLAY_SOUND:
            pg.mixer.music.play(-1)
        else:
            pg.mixer.music.stop()

    def capture_img(self):
        path = r'E:\pgimg\{0}.png'
        pg.image.save(self.screen, path.format(self.capture_counter))
        self.capture_counter += 1



