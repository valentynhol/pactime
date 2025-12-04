import time
import random
import tkinter as tk

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.game import Game, ClassicGameMode


class CharacterEntity:
    def __init__(
            self,
            game: 'Game',
            game_canvas: tk.Canvas,
            game_map_state: dict,
            cell_size: int,
            x: int,
            y: int
    ):
        self._game = game
        self._game_canvas = game_canvas
        self._game_map = game_map_state
        self._cell_size = cell_size
        self.x = x
        self.y = y

        self.direction = 180
        self.next_direction = 180

        self._icon = []

    def move(self):
        in_cell = self.x % 1 == 0 and self.y % 1 == 0

        gm = self._game_map
        gm_w = len(gm[0])
        gm_h = len(gm)
        cs = self._cell_size
        
        if in_cell:
            if 0 <= self.x <= gm_w - 1 and 0 <= self.y <= gm_h - 1:
                if self.next_direction == 0:
                    if self.x == 0:
                        if gm[int(self.y)][gm_w - 1] != '#':
                            self.direction = self.next_direction
                    elif self.x < 0:
                        pass
                    elif gm[int(self.y)][int(self.x - 1)] != '#':
                        self.direction = self.next_direction
                elif self.next_direction == 90:
                    if self.y == gm_h - 1:
                        if gm[0][int(self.x)] != '#':
                            self.direction = self.next_direction
                    elif self.y > gm_h - 1:
                        pass
                    elif gm[int(self.y + 1)][int(self.x)] != '#':
                        self.direction = self.next_direction
                elif self.next_direction == 180:
                    if self.x == gm_w - 1:
                        if gm[int(self.y)][0] != '#':
                            self.direction = self.next_direction
                    elif self.x > gm_w - 1:
                        pass
                    elif gm[int(self.y)][int(self.x + 1)] != '#':
                        self.direction = self.next_direction
                elif self.next_direction == 270:
                    if self.y == 0:
                        if gm[gm_h - 1][int(self.x)] != '#':
                            self.direction = self.next_direction
                    elif self.y < 0:
                        pass
                    elif gm[int(self.y - 1)][int(self.x)] != '#':
                        self.direction = self.next_direction

        x_to_move = 0
        y_to_move = 0

        if self.direction == 0:
            if self.x <= -1.3 and gm[int(self.y)][gm_w - 1] != '#':
                self.x = self.x + gm_w + 2
                x_to_move = (gm_w + 2) * cs
            elif self.x <= -1 or not in_cell or gm[int(self.y)][int(self.x - 1)] != '#':
                self.x = round(self.x - 0.1, 1)
                x_to_move = -0.1 * cs
        elif self.direction == 90:
            if self.y >= gm_h - 1:
                if gm[0][int(self.x)] != '#':
                    if self.y >= gm_h + 0.3:
                        self.y = self.y - gm_h - 2
                        y_to_move = - (gm_h + 2) * cs
                    else:
                        self.y = round(self.y + 0.1, 1)
                        y_to_move = 0.1 * cs
            elif not in_cell or gm[int(self.y + 1)][int(self.x)] != '#':
                self.y = round(self.y + 0.1, 1)
                y_to_move = 0.1 * cs
        elif self.direction == 180:
            if self.x >= gm_w - 1:
                if gm[int(self.y)][0] != '#':
                    if self.x >= gm_w + 0.3:
                        self.x = self.x - gm_w - 2
                        x_to_move = - (gm_w + 2) * cs
                    else:
                        self.x = round(self.x + 0.1, 1)
                        x_to_move = 0.1 * cs
            elif not in_cell or gm[int(self.y)][int(self.x + 1)] != '#':
                self.x = round(self.x + 0.1, 1)
                x_to_move = 0.1 * cs
        elif self.direction == 270:
            if self.y <= -1.3 and gm[gm_h - 1][int(self.x)] != '#':
                self.y = self.y + gm_h + 2
                y_to_move = (gm_h + 2) * cs
            elif self.y <= -1 or not in_cell or gm[int(self.y - 1)][int(self.x)] != '#':
                self.y = round(self.y - 0.1, 1)
                y_to_move = -0.1 * cs

        self._move_icon(x_to_move, y_to_move)

    def _move_icon(self, x_to_move, y_to_move):
        for item in self._icon:
            self._game_canvas.move(item, x_to_move, y_to_move)


class Pac(CharacterEntity):

    def __init__(
            self,
            game: 'Game',
            game_canvas: tk.Canvas,
            game_map_state: dict,
            cell_size: int,
            x: int,
            y: int
    ):
        super().__init__(game, game_canvas, game_map_state, cell_size, x, y)

        cs = self._cell_size
        icon_x = x * cs + 0.25 * cs
        icon_y = y * cs + 0.25 * cs

        self._icon = [self._game_canvas.create_arc(
            (icon_x, icon_y),
            (icon_x + cs, icon_y + cs),
            fill='yellow',
            start=45,
            extent=-270,
            tags=["CharacterEntity", "Pac"]
        )]

        self.mouth_phase = 0

        self._game_canvas.bind_all('<KeyPress>', self.turn)

    def _move_mouth(self):
        if self.mouth_phase < 5:
            arc_size = -280 - self.mouth_phase * 17
        else:
            arc_size = -280 - (9 - self.mouth_phase) * 17

        if self.mouth_phase == 10:
            self.mouth_phase = 0

        self.mouth_phase += 1

        self._game_canvas.itemconfig(self._icon[0], start=self.direction - arc_size / 2, extent=arc_size)

    def _eat_dot(self):
        gm = self._game_map
        gm_w = len(gm[0])
        gm_h = len(gm)

        in_cell = self.x % 1 == 0 and self.y % 1 == 0

        if 0 <= self.x <= gm_w - 1 and 0 <= self.y <= gm_h - 1:
            if in_cell and gm[int(self.y)][int(self.x)] in self._game_canvas.find_withtag("Dot"):
                self._game.remove_dot(self.x, self.y)

                if hasattr(self._game, 'add_score'):
                    self._game.add_score(10)

    def turn(self, event):
        if self._game.process == 'game':
            key = event.keysym
            if key == 'Left' or key == 'a' or key == 'A':
                self.next_direction = 0
            if key == 'Down' or key == 's' or key == 'S':
                self.next_direction = 90
            if key == 'Right' or key == 'd' or key == 'D':
                self.next_direction = 180
            if key == 'Up' or key == 'w' or key == 'W':
                self.next_direction = 270

    def move(self):
        self._move_mouth()
        self._eat_dot()
        super().move()

    def die(self):
        arc_size = -280 - self.mouth_phase * 17
        while arc_size:
            arc_size += 30
            arc_size = min(arc_size, 0)
            self._game_canvas.itemconfig(self._icon[0], start=self.direction - arc_size / 2, extent=arc_size)
            self._game_canvas.update()
            time.sleep(0.03)

        self._game.on_lose()


class Ghost(CharacterEntity):
    def __init__(
            self,
            game: 'ClassicGameMode',
            game_canvas: tk.Canvas,
            game_map_state: dict,
            cell_size: int,
            x: int,
            y: int,
            color="red"
    ):
        super().__init__(game, game_canvas, game_map_state, cell_size, x, y)
        self.color = color

        cs = self._cell_size

        icon_x = x * cs + 0.25 * cs
        icon_y = y * cs + 0.25 * cs
        self._icon = [
            self._game_canvas.create_arc(
                (icon_x + 0.1 * cs - 1, icon_y),
                (icon_x + cs - 0.1 * cs, icon_y + cs),
                fill=color,
                start=0,
                extent=180,
                tags=["CharacterEntity", "Ghost"]
            ),
            self._game_canvas.create_polygon(
                (icon_x + 0.1 * cs, icon_y + 0.5 * cs),
                (icon_x + 0.9 * cs, icon_y + 0.5 * cs),
                (icon_x + 0.9 * cs, icon_y + cs),
                (icon_x + 0.8 * cs, icon_y + 0.9 * cs),
                (icon_x + 0.7 * cs, icon_y + cs),
                (icon_x + 0.6 * cs, icon_y + 0.9 * cs),
                (icon_x + 0.5 * cs, icon_y + cs),
                (icon_x + 0.4 * cs, icon_y + 0.9 * cs),
                (icon_x + 0.3 * cs, icon_y + cs),
                (icon_x + 0.2 * cs, icon_y + 0.9 * cs),
                (icon_x + 0.1 * cs, icon_y + cs),
                fill=color,
                tags=["CharacterEntity", "Ghost"]
            ),
            self._game_canvas.create_rectangle(
                (icon_x + 0.25 * cs, icon_y + 0.4 * cs),
                (icon_x + 0.4 * cs, icon_y + 0.55 * cs),
                fill="black",
                outline="white",
                tags=["CharacterEntity", "Ghost"]
            ),
            self._game_canvas.create_rectangle(
                (icon_x + 0.6 * cs, icon_y + 0.4 * cs),
                (icon_x + 0.75 * cs, icon_y + 0.55 * cs),
                fill="black",
                outline="white",
                tags=["CharacterEntity", "Ghost"]
            )
        ]

    def kill_pac(self):
        pac = self._game.pac
        if (self.y == pac.y and pac.x + 1 > self.x > pac.x - 1) or (self.x == pac.x and pac.y + 1 > self.y > pac.y - 1):
            pac.die()

    def move(self):
        self.kill_pac()
        in_cell = self.x % 1 == 0 and self.y % 1 == 0
        if in_cell:
            dir_choice = [0, 90, 180, 270] * 2
            dir_choice += [self.direction] * 2
            if self.direction + 180 % 360 in dir_choice:
                dir_choice.remove(self.direction + 180 % 360)

            self.next_direction = random.choice(dir_choice)

        super().move()
