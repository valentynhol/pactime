import os
import copy
import json
import time
import random

import tkinter as tk


class MainMenu:
    pass


class Game:
    field = None
    game_map = None
    pac = None
    window = None

    window_height = 0
    window_width = 0
    map_width = 0
    map_height = 0
    offset_x = 0
    offset_y = 0
    cell_size = 0
    
    process = 'game'
    score = 0
    dot_num = 0
    
    max_game_duration = 0

    __game_start_time = 0
    __pause_start_time = 0
    __pause_duration = 0
    __modal_labels = []

    __time_label = None
    score_label = None

    def __init__(self, game_map, max_game_duration):
        self.score = 0
        self.process = 'game'
        self.game_map = copy.deepcopy(game_map)
        self.max_game_duration = max_game_duration

    def open_menu(self):
        self.__pause_start_time = time.time()
        self.__show_modal()

        self.__modal_labels.append(self.field.create_text(0.5 * self.window_width, 0.5*self.window_height - 30,
                                                          text='Menu', fill='white', font=('ArialBold', 18)))
        self.__modal_labels.append(self.field.create_text(0.5 * self.window_width, 0.5*self.window_height + 10,
                                                          text='Press "Esc" to continue game', fill='white'))
        self.__modal_labels.append(self.field.create_text(0.5 * self.window_width, 0.5*self.window_height + 25,
                                                          text='Press "Enter" tо restart game', fill='white'))

        self.process = 'menu'

    def win_game(self):
        self.__show_modal()
        self.__modal_labels.append(self.field.create_text(0.5 * self.window_width, 0.5*self.window_height - 30,
                                                          text='You won!!!', fill='white', font=('ArialBold', 18)))
        self.__modal_labels.append(self.field.create_text(0.5 * self.window_width, 0.5*self.window_height - 5,
                                                          text='Your score: ' + str(self.score), fill='white',
                                                          font=('ArialBold', 13)))
        self.__modal_labels.append(self.field.create_text(0.5 * self.window_width, 0.5*self.window_height + 25,
                                                          text='Press "Enter" tо restart game', fill='white'))
        self.process = 'game ended'

    def lose_game(self):
        self.__show_modal()
        self.__modal_labels.append(self.field.create_text(0.5 * self.window_width, 0.5*self.window_height - 15,
                                                          text="Time's up!!! \n Game over", fill='white',
                                                          font=('ArialBold', 15)))
        self.__modal_labels.append(self.field.create_text(0.5 * self.window_width, 0.5*self.window_height + 25,
                                                          text='Press "Enter" tо restart game', fill='white'))
        self.process = 'game ended'

    def restart_game(self):
        self.field.delete('all')
        self.pac = None
        self.game_map = None

        self.score = 0
        self.process = 'game'
        self.__game_start_time = time.time()

        self.game_map = copy.deepcopy(selected_map['gameMap'])
        self.map_init()

        self.window.bind('<KeyPress>', self.pac.turn)
        self.window.bind('<KeyRelease>', self.process_change)

    def close_menu(self):
        self.__hide_modal()

        self.process = 'game'

        self.__pause_duration += time.time() - self.__pause_start_time
        self.__pause_start_time = 0

    def __show_modal(self):
        self.__modal_labels.append(self.field.create_rectangle((0.5*self.window_width - 125,
                                                                0.5*self.window_height - 50),
                                                               (0.5*self.window_width + 125,
                                                                0.5*self.window_height + 50),
                                                               fill='black', outline='purple'))

    def __hide_modal(self):
        self.__remove_modal_labels()

    def __remove_modal_labels(self):
        for index, label in enumerate(self.__modal_labels):
            self.field.delete(label)

        self.__modal_labels = []

    def game_cycle(self):
        time.sleep(0.03)

        if self.process == 'game':
            self.pac.move()
            self.pac.move_mouth()

            game_time = self.max_game_duration - (
                        time.time() - self.__game_start_time - self.__pause_duration)

            if game_time < 0:
                self.lose_game()
            elif 0 == self.dot_num:
                self.score += round(game_time * 1000)
                self.win_game()
            else:
                time_m = game_time // 60
                time_s = game_time % 60
                
                if self.process == 'game':
                    self.field.itemconfig(self.__time_label,
                                          text='Time left: ' + str(int(time_m)) + ':' + str(round(time_s, 1)))

    def process_change(self, event):
        key = event.keysym
        if self.process == 'game':
            if key == 'Escape':
                self.open_menu()
        elif self.process == 'menu':
            if key == 'Return':
                self.restart_game()
            if key == 'Escape':
                self.close_menu()
        elif self.process == 'game ended':
            if key == 'Return':
                self.restart_game()

    def map_init(self):
        pac_created = False
        graphic_pac_x = 0
        graphic_pac_y = 0
        pac_x = 0
        pac_y = 0

        for row_num, row in enumerate(self.game_map, start=0):
            for cell_num, cell in enumerate(row, start=0):
                x = cell_num * self.cell_size + self.offset_x + 0.25*self.cell_size
                y = row_num * self.cell_size + self.offset_y + 0.25*self.cell_size

                if self.game_map[row_num][cell_num] == '#':
                    end_x = x + self.cell_size
                    end_y = y + self.cell_size

                    self.field.create_rectangle((x, y), (end_x, end_y), fill='purple')

                elif self.game_map[row_num][cell_num] == '.':
                    start_x = x + 0.41*self.cell_size
                    start_y = y + 0.41*self.cell_size
                    end_x = x + 0.59*self.cell_size
                    end_y = y + 0.59*self.cell_size

                    self.game_map[row_num][cell_num] = self.field.create_rectangle((start_x, start_y),
                                                                                   (end_x, end_y), fill='white')
                    self.dot_num += 1

                elif self.game_map[row_num][cell_num] == 'p':
                    graphic_pac_x = x
                    graphic_pac_y = y
                    pac_x = cell_num
                    pac_y = row_num
                    pac_created = True

        if not pac_created:
            raise MapGenerationError(
                "Map has no pacman location specified!!! If you are the creator of this map, you should"
                " set 'p' on map array to set pacman start location.")

        graphic_obj = self.field.create_arc([graphic_pac_x, graphic_pac_y],
                                            [graphic_pac_x + self.cell_size, graphic_pac_y + self.cell_size],
                                            fill='yellow', start=45, extent=-270)
        self.pac = Pac(self, pac_x, pac_y, graphic_obj)

        self.field.create_rectangle((self.offset_x - self.cell_size, self.offset_y - self.cell_size),
                                    (self.offset_x + self.map_width + self.cell_size,
                                     self.offset_y + self.map_height + self.cell_size + 1),
                                    outline='black', width=self.cell_size*2)

        self.field.create_rectangle((0, 0), (self.window_width + 1, self.window_height/20), fill='black',
                                    outline='purple')
        self.field.create_rectangle((0, self.window_height - self.window_height/40),
                                    (self.window_width + 1, self.window_height + 1),
                                    fill='black', outline='purple')

        self.score_label = self.field.create_text(40, self.window_height/40, text='Score: 0', fill='white',
                                                  font=('ArialBold', self.window_height//50), anchor='w')

        self.__time_label = self.field.create_text(self.window_width - 40, self.window_height/40,
                                                   text='Time left: ' + str(self.max_game_duration // 60) + ':' +
                                                        str(float(self.max_game_duration % 60)),
                                                   fill='white', font=('ArialBold', self.window_height//50), anchor='e')

        self.field.create_text(self.window_width/2, self.window_height - self.window_height/80, text='Menu -- "Esc"',
                               fill='white', font=('ArialBold', self.window_height//90), anchor='center')

    def window_init(self):
        self.window = tk.Tk(className='pactime')
        self.window.title('PacTime')

        self.window.attributes('-fullscreen', True)
        self.window.update()
        self.window_width = self.window.winfo_width()
        self.window_height = self.window.winfo_height()

        self.cell_size = min((self.window_height*32/40) // len(self.game_map),
                             (self.window_width*35/40) // len(self.game_map[0]), 40)

        self.map_width = len(self.game_map[0])*self.cell_size + 0.5*self.cell_size
        self.map_height = len(self.game_map)*self.cell_size + 0.5*self.cell_size

        self.offset_x = 0.5 * (self.window_width - self.map_width)
        self.offset_y = 0.5 * (1.025*self.window_height - self.map_height)

        self.window.iconphoto(True, tk.PhotoImage(file='images/icon.png'))

        self.field = tk.Canvas(self.window, width=self.window_width, height=self.window_height, bg='black')
        self.field.place(x=-1, y=-1)

    def start(self):
        self.window_init()
        self.map_init()

        self.window.bind('<KeyPress>', self.pac.turn)
        self.window.bind('<KeyRelease>', self.process_change)

        self.__game_start_time = time.time()

        while True:
            self.window.update_idletasks()
            self.window.update()
            self.game_cycle()


class Pac:
    x = 0
    y = 0
    mouth_phase = 0
    direction = 180
    next_direction = 180
    graphic_obj = None
    in_cell = True
    game = None
    
    def __init__(self, game_object, x, y, graphic_obj):
        self.game = game_object
        self.x = x
        self.y = y
        self.graphic_obj = graphic_obj
    
    def move_mouth(self):
        if self.mouth_phase < 5:
            arc_size = -280 - self.mouth_phase * 17
        else:
            arc_size = -280 - (9 - self.mouth_phase) * 17

        if self.mouth_phase == 10:
            self.mouth_phase = 0

        self.mouth_phase += 1

        self.game.field.itemconfig(self.graphic_obj, start=self.direction - arc_size / 2, extent=arc_size)

    def eat_dot(self):
        if 0 <= self.x <= len(self.game.game_map[0]) - 1 and 0 <= self.y <= len(self.game.game_map) - 1:
            if self.in_cell and self.game.game_map[int(self.y)][int(self.x)] not in ['p', '#', ' ']:
                self.game.field.delete(self.game.game_map[int(self.y)][int(self.x)])
                self.game.game_map[int(self.y)][int(self.x)] = ' '
                self.game.score += 10
                self.game.dot_num -= 1
                self.game.field.itemconfig(self.game.score_label, text='Score: ' + str(self.game.score))

    def turn(self, event):
        if self.game.process == 'game':
            key = event.keysym
            if key == 'Left':
                self.next_direction = 0
            if key == 'Down':
                self.next_direction = 90
            if key == 'Right':
                self.next_direction = 180
            if key == 'Up':
                self.next_direction = 270
    
    def move(self):
        self.in_cell = self.x % 1 == 0 and self.y % 1 == 0
        self.eat_dot()

        if self.in_cell:
            if 0 <= self.x <= len(self.game.game_map[0]) - 1 and 0 <= self.y <= len(self.game.game_map) - 1:
                if self.next_direction == 0:
                    if self.x == 0:
                        if self.game.game_map[int(self.y)][len(self.game.game_map[0])-1] != '#':
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
                        if self.game.game_map[len(self.game.game_map)-1][int(self.x)] != '#':
                            self.direction = self.next_direction
                    elif self.y < 0:
                        pass
                    elif self.game.game_map[int(self.y - 1)][int(self.x)] != '#':
                        self.direction = self.next_direction

        x_to_move = 0
        y_to_move = 0

        if self.direction == 0:
            if self.x <= -1.3 and self.game.game_map[int(self.y)][len(self.game.game_map[0])-1] != '#':
                self.x = self.x + len(self.game.game_map[0]) + 2
                x_to_move = (len(self.game.game_map[0]) + 2) * self.game.cell_size
            else:
                if not self.in_cell or self.game.game_map[int(self.y)][int(self.x-1)] != '#':
                    self.x = round(self.x-0.1, 1)
                    x_to_move = -0.1 * self.game.cell_size
        elif self.direction == 90:
            if self.y >= len(self.game.game_map) - 1:
                if self.game.game_map[0][int(self.x)] != '#':
                    if self.y >= len(self.game.game_map) + 0.3:
                        self.y = self.y - len(self.game.game_map) - 2
                        y_to_move = - (len(self.game.game_map) + 2)*self.game.cell_size
                    else:
                        self.y = round(self.y + 0.1, 1)
                        y_to_move = 0.1 * self.game.cell_size
            else:
                if not self.in_cell or self.game.game_map[int(self.y+1)][int(self.x)] != '#':
                    self.y = round(self.y+0.1, 1)
                    y_to_move = 0.1 * self.game.cell_size
        elif self.direction == 180:
            if self.x >= len(self.game.game_map[0]) - 1:
                if self.game.game_map[int(self.y)][0] != '#':
                    if self.x >= len(self.game.game_map[0]) + 0.3:
                        self.x = self.x - len(self.game.game_map[0]) - 2
                        x_to_move = - (len(self.game.game_map[0]) + 2)*self.game.cell_size
                    else:
                        self.x = round(self.x + 0.1, 1)
                        x_to_move = 0.1 * self.game.cell_size
            else:
                if not self.in_cell or self.game.game_map[int(self.y)][int(self.x+1)] != '#':
                    self.x = round(self.x+0.1, 1)
                    x_to_move = 0.1 * self.game.cell_size
        elif self.direction == 270:
            if self.y <= -1.3 and self.game.game_map[len(self.game.game_map) - 1][int(self.x)] != '#':
                self.y = self.y + len(self.game.game_map) + 2
                y_to_move = (len(self.game.game_map) + 2) * self.game.cell_size
            elif not self.in_cell or self.game.game_map[int(self.y-1)][int(self.x)] != '#':
                self.y = round(self.y-0.1, 1)
                y_to_move = -0.1 * self.game.cell_size

        self.game.field.move(self.graphic_obj, x_to_move, y_to_move)


class MapGenerationError(Exception):
    pass


with open('./maps/' + random.choice(os.listdir('./maps'))) as map_file:
    selected_map = json.load(map_file)

game = Game(selected_map['gameMap'], selected_map['maxGameDuration'])
game.start()
