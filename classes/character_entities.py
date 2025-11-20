import time
import random

class CharacterEntity:
    x = 0
    y = 0
    direction = 180
    next_direction = 180
    graphic_obj = None
    in_cell = True
    game = None

    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y

    def move(self):
        self.in_cell = self.x % 1 == 0 and self.y % 1 == 0

        if self.in_cell:
            if 0 <= self.x <= len(self.game.game_map[0]) - 1 and 0 <= self.y <= len(self.game.game_map) - 1:
                if self.next_direction == 0:
                    if self.x == 0:
                        if self.game.game_map[int(self.y)][len(self.game.game_map[0]) - 1] != '#':
                            self.direction = self.next_direction
                    elif self.x < 0:
                        pass
                    elif self.game.game_map[int(self.y)][int(self.x - 1)] != '#':
                        self.direction = self.next_direction
                elif self.next_direction == 90:
                    if self.y == len(self.game.game_map) - 1:
                        if self.game.game_map[0][int(self.x)] != '#':
                            self.direction = self.next_direction
                    elif self.y > len(self.game.game_map) - 1:
                        pass
                    elif self.game.game_map[int(self.y + 1)][int(self.x)] != '#':
                        self.direction = self.next_direction
                elif self.next_direction == 180:
                    if self.x == len(self.game.game_map[0]) - 1:
                        if self.game.game_map[int(self.y)][0] != '#':
                            self.direction = self.next_direction
                    elif self.x > len(self.game.game_map[0]) - 1:
                        pass
                    elif self.game.game_map[int(self.y)][int(self.x + 1)] != '#':
                        self.direction = self.next_direction
                elif self.next_direction == 270:
                    if self.y == 0:
                        if self.game.game_map[len(self.game.game_map) - 1][int(self.x)] != '#':
                            self.direction = self.next_direction
                    elif self.y < 0:
                        pass
                    elif self.game.game_map[int(self.y - 1)][int(self.x)] != '#':
                        self.direction = self.next_direction

        x_to_move = 0
        y_to_move = 0

        if self.direction == 0:
            if self.x <= -1.3 and self.game.game_map[int(self.y)][len(self.game.game_map[0]) - 1] != '#':
                self.x = self.x + len(self.game.game_map[0]) + 2
                x_to_move = (len(self.game.game_map[0]) + 2) * self.game.cell_size
            elif self.x <= -1 or not self.in_cell or self.game.game_map[int(self.y)][int(self.x - 1)] != '#':
                self.x = round(self.x - 0.1, 1)
                x_to_move = -0.1 * self.game.cell_size
        elif self.direction == 90:
            if self.y >= len(self.game.game_map) - 1:
                if self.game.game_map[0][int(self.x)] != '#':
                    if self.y >= len(self.game.game_map) + 0.3:
                        self.y = self.y - len(self.game.game_map) - 2
                        y_to_move = - (len(self.game.game_map) + 2) * self.game.cell_size
                    else:
                        self.y = round(self.y + 0.1, 1)
                        y_to_move = 0.1 * self.game.cell_size
            elif not self.in_cell or self.game.game_map[int(self.y + 1)][int(self.x)] != '#':
                self.y = round(self.y + 0.1, 1)
                y_to_move = 0.1 * self.game.cell_size
        elif self.direction == 180:
            if self.x >= len(self.game.game_map[0]) - 1:
                if self.game.game_map[int(self.y)][0] != '#':
                    if self.x >= len(self.game.game_map[0]) + 0.3:
                        self.x = self.x - len(self.game.game_map[0]) - 2
                        x_to_move = - (len(self.game.game_map[0]) + 2) * self.game.cell_size
                    else:
                        self.x = round(self.x + 0.1, 1)
                        x_to_move = 0.1 * self.game.cell_size
            elif not self.in_cell or self.game.game_map[int(self.y)][int(self.x + 1)] != '#':
                self.x = round(self.x + 0.1, 1)
                x_to_move = 0.1 * self.game.cell_size
        elif self.direction == 270:
            if self.y <= -1.3 and self.game.game_map[len(self.game.game_map) - 1][int(self.x)] != '#':
                self.y = self.y + len(self.game.game_map) + 2
                y_to_move = (len(self.game.game_map) + 2) * self.game.cell_size
            elif self.y <= -1 or not self.in_cell or self.game.game_map[int(self.y - 1)][int(self.x)] != '#':
                self.y = round(self.y - 0.1, 1)
                y_to_move = -0.1 * self.game.cell_size

        self._move_graphic_obj(x_to_move, y_to_move)

    def _move_graphic_obj(self, x_to_move, y_to_move):
        self.game.field.move(self.graphic_obj, x_to_move, y_to_move)


class Pac(CharacterEntity):
    x = 0
    y = 0
    mouth_phase = 0
    direction = 180
    next_direction = 180
    graphic_obj = None
    in_cell = True
    game = None

    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        cs = game.cell_size
        graphic_obj_x = x * cs + game.offset_x + 0.25 * cs
        graphic_obj_y = y * cs + game.offset_y + 0.25 * cs
        self.graphic_obj = game.field.create_arc([graphic_obj_x, graphic_obj_y],
                                                 [graphic_obj_x + cs, graphic_obj_y + cs],
                                                 fill='yellow', start=45, extent=-270, tags="CharacterEntity")

    def _move_mouth(self):
        if self.mouth_phase < 5:
            arc_size = -280 - self.mouth_phase * 17
        else:
            arc_size = -280 - (9 - self.mouth_phase) * 17

        if self.mouth_phase == 10:
            self.mouth_phase = 0

        self.mouth_phase += 1

        self.game.field.itemconfig(self.graphic_obj, start=self.direction - arc_size / 2, extent=arc_size)

    def _eat_dot(self):
        if 0 <= self.x <= len(self.game.game_map[0]) - 1 and 0 <= self.y <= len(self.game.game_map) - 1:
            if self.in_cell and self.game.game_map[int(self.y)][int(self.x)] in self.game.field.find_withtag("Dot"):
                self.game.field.delete(self.game.game_map[int(self.y)][int(self.x)])
                self.game.game_map[int(self.y)][int(self.x)] = ' '
                self.game.score += 10
                self.game.dot_num -= 1
                self.game.field.itemconfig(self.game.score_label, text='Score: ' + str(self.game.score))

    def turn(self, event):
        if self.game.process == 'game':
            key = event.keysym
            if key == 'Left' or key == 'a':
                self.next_direction = 0
            if key == 'Down' or key == 's':
                self.next_direction = 90
            if key == 'Right' or key == 'd':
                self.next_direction = 180
            if key == 'Up' or key == 'w':
                self.next_direction = 270

    def move(self):
        self.in_cell = self.x % 1 == 0 and self.y % 1 == 0
        self._move_mouth()
        self._eat_dot()
        super().move()

    def die(self):
        arc_size = -280 - self.mouth_phase * 17
        while arc_size:
            arc_size += 30
            arc_size = min(arc_size, 0)
            self.game.field.itemconfig(self.graphic_obj, start=self.direction - arc_size / 2, extent=arc_size)
            self.game.main_menu.window.update()
            time.sleep(0.03)

        self.game.lost_game()


class Ghost(CharacterEntity):
    color = ""

    def __init__(self, game, x, y, color="red"):
        super().__init__(game, x, y)
        self.color = color

        cs = game.cell_size
        graphic_obj_x = x * cs + game.offset_x + 0.25 * cs
        graphic_obj_y = y * cs + game.offset_y + 0.25 * cs
        self.graphic_obj = [
            game.field.create_arc([graphic_obj_x + 0.1 * cs - 1, graphic_obj_y],
                                  [graphic_obj_x + cs - 0.1 * cs, graphic_obj_y + cs],
                                  fill=color, start=0, extent=180, tags=["CharacterEntity", "Ghost"]),
            game.field.create_polygon([graphic_obj_x + 0.1 * cs, graphic_obj_y + 0.5 * cs],
                                      [graphic_obj_x + 0.9 * cs, graphic_obj_y + 0.5 * cs],
                                      [graphic_obj_x + 0.9 * cs, graphic_obj_y + cs],
                                      [graphic_obj_x + 0.8 * cs, graphic_obj_y + 0.9 * cs],
                                      [graphic_obj_x + 0.7 * cs, graphic_obj_y + cs],
                                      [graphic_obj_x + 0.6 * cs, graphic_obj_y + 0.9 * cs],
                                      [graphic_obj_x + 0.5 * cs, graphic_obj_y + cs],
                                      [graphic_obj_x + 0.4 * cs, graphic_obj_y + 0.9 * cs],
                                      [graphic_obj_x + 0.3 * cs, graphic_obj_y + cs],
                                      [graphic_obj_x + 0.2 * cs, graphic_obj_y + 0.9 * cs],
                                      [graphic_obj_x + 0.1 * cs, graphic_obj_y + cs],
                                      fill=color, tags=["CharacterEntity", "Ghost"]),
            game.field.create_rectangle([graphic_obj_x + 0.25 * cs, graphic_obj_y + 0.4 * cs],
                                        [graphic_obj_x + 0.4 * cs, graphic_obj_y + 0.55 * cs],
                                        fill="black", outline="white", tags=["CharacterEntity", "Ghost"]),
            game.field.create_rectangle([graphic_obj_x + 0.6 * cs, graphic_obj_y + 0.4 * cs],
                                        [graphic_obj_x + 0.75 * cs, graphic_obj_y + 0.55 * cs],
                                        fill="black", outline="white", tags=["CharacterEntity", "Ghost"])
        ]

    def kill_pac(self):
        pac = self.game.pac
        if (self.y == pac.y and pac.x + 1 > self.x > pac.x - 1) or \
                (self.x == pac.x and pac.y + 1 > self.y > pac.y - 1):
            pac.die()

    def move(self):
        self.kill_pac()
        self.in_cell = self.x % 1 == 0 and self.y % 1 == 0
        if self.in_cell:
            dir_choice = [0, 90, 180, 270] * 2
            dir_choice += [self.direction] * 2
            if self.direction + 180 % 360 in dir_choice:
                dir_choice.remove(self.direction + 180 % 360)

            self.next_direction = random.choice(dir_choice)

        super().move()

    def _move_graphic_obj(self, x_to_move, y_to_move):
        for obj in self.graphic_obj:
            self.game.field.move(obj, x_to_move, y_to_move)
