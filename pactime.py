import os
import copy
import json
import time
import random

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox


class MainMenu:
    window = None
    menu_canvas = None
    window_width = 0
    window_height = 0

    menu_buttons = {}
    menu_btn_cycles = {'play': None, 'options': None, 'how_to_play': None, 'quit': None}
    animation = {}
    map_selector = {}
    map_btns = {}

    maps = os.listdir('./maps')

    def __init__(self):
        self.maps.sort()
        self.__window_init()
        self.open_menu()

    def open_menu(self):
        self.menu_canvas = tk.Canvas(self.window, width=self.window_width, height=self.window_height, bg='black')
        self.menu_canvas.place(x=-1, y=-1)
        self.__create_menu_gui()

        while self.window:
            try:
                try:
                    time.sleep(0.01)
                    try:
                        self.__menu_animation()
                    except tk.TclError:
                        pass

                    for btn in list(self.menu_buttons.keys()):
                        self.__btn_animation(btn, 'menu')

                    self.window.update_idletasks()
                    self.window.update()
                except AttributeError and tk.TclError:
                    pass
            except KeyboardInterrupt:
                exit()

    def close_menu(self):
        self.menu_canvas.destroy()

    def __play(self, selected_map):
        with open('./maps/' + selected_map) as map_file:
            game_map = json.load(map_file)

        self.close_menu()

        game = Game(self, game_map['gameMap'], game_map['maxGameDuration'])
        game.start()

    def __options(self):
        pass

    def __how_to_play(self):
        pass

    def __quit(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.window.destroy()
            self.window = None

    def __btn_animation(self, btn, btn_type=None):
        cycle = self.menu_btn_cycles[btn]
        if cycle:
            if btn_type == 'menu':
                if cycle == 1:
                    self.menu_buttons[btn].config(cursor='watch', bg='purple', fg='black')
                elif cycle <= 13:
                    self.menu_buttons[btn].config(font=('Arial', self.window_height // 30 - (cycle - 7), 'bold'))
                elif cycle <= 17:
                    self.menu_buttons[btn].config(font=('Arial', self.window_height // 30 + 3 - (cycle - 14), 'bold'))
                elif cycle == 18:
                    self.menu_buttons[btn].config(cursor='hand2', bg='black', fg='purple')
            elif btn_type == 'map_select':
                if cycle == 1:
                    self.menu_buttons[btn].config(cursor='watch', bg='purple', fg='black')
                elif cycle <= 13:
                    self.menu_buttons[btn].config(font=('Arial', self.window_height // 30 - (cycle - 7), 'bold'))
                elif cycle <= 17:
                    self.menu_buttons[btn].config(font=('Arial', self.window_height // 30 + 3 - (cycle - 14), 'bold'))
                elif cycle == 18:
                    self.menu_buttons[btn].config(cursor='hand2', bg='black', fg='purple')

            self.menu_btn_cycles[btn] += 1
        if cycle == 19:
            self.menu_btn_cycles[btn] = None

    def __create_menu_gui(self):
        def __click(event):
            if event.widget in self.menu_buttons.values():
                event.widget.config(relief='flat')
                btn_name = list(self.menu_buttons.keys())[list(self.menu_buttons.values()).index(event.widget)]
                self.menu_btn_cycles[btn_name] = 1

        self.__menu_animation_constructor()
        self.menu_buttons['play'] = tk.Button(self.menu_canvas, text='Play', fg='purple', bg='black', relief='flat',
                                              activebackground='purple', activeforeground='black', width=15,
                                              highlightthickness=5, highlightbackground='purple', cursor='hand2',
                                              font=('Arial', self.window_height // 30, 'bold'),
                                              command=self.__select_map)
        self.menu_buttons['options'] = tk.Button(self.menu_canvas, text='Options', fg='purple', bg='black',
                                                 relief='flat', activebackground='purple', activeforeground='black',
                                                 width=15, highlightthickness=5, highlightbackground='purple',
                                                 cursor='hand2', font=('Arial', self.window_height // 30, 'bold'),
                                                 command=self.__options)
        self.menu_buttons['how_to_play'] = tk.Button(self.menu_canvas, text='How to play', fg='purple', bg='black',
                                                     relief='flat', activebackground='purple', activeforeground='black',
                                                     width=15, highlightthickness=5, highlightbackground='purple',
                                                     cursor='hand2', font=('Arial', self.window_height // 30, 'bold'),
                                                     command=self.__how_to_play)
        self.menu_buttons['quit'] = tk.Button(self.menu_canvas, text='Quit', fg='purple', bg='black', relief='flat',
                                              activebackground='purple', activeforeground='black', width=15,
                                              highlightthickness=5, highlightbackground='purple', cursor='hand2',
                                              font=('Arial', self.window_height // 30, 'bold'), command=self.__quit)

        self.menu_buttons['play'].place(x=0.5 * self.window_width, y=15 / 30 * self.window_height, anchor='center')
        self.menu_buttons['options'].place(x=0.5 * self.window_width, y=19 / 30 * self.window_height,
                                           anchor='center')
        self.menu_buttons['how_to_play'].place(x=0.5 * self.window_width, y=23 / 30 * self.window_height,
                                               anchor='center')
        self.menu_buttons['quit'].place(x=0.5 * self.window_width, y=27 / 30 * self.window_height, anchor='center')

        self.window.bind('<Button-1>', __click)

    def __menu_animation_constructor(self):
        self.animation['height'] = self.window_height // 9
        self.animation['width'] = self.window_height // 3

        self.animation['frame'] = tk.Frame(self.menu_canvas, height=self.animation['height'],
                                           width=self.animation['width'], bg='black')
        self.animation['frame'].place(x=0.5 * self.window_width, y=self.window_height // 10, anchor='center')
        self.animation['canvas'] = tk.Canvas(self.animation['frame'], bg='black', width=self.animation['width'],
                                             height=self.animation['height'])
        self.animation['canvas'].place(x=-1, y=-1)

        self.animation['cycle'] = 0

        for dot_num in range(3):
            self.animation['dot' + str(dot_num + 1)] = self.animation['canvas'].create_rectangle(
                [(dot_num + 1) * self.animation['height'] - 0.09 * self.animation['height'],
                 0.41 * self.animation['height']],
                [(dot_num + 1) * self.animation['height'] + 0.09 * self.animation['height'],
                 0.59 * self.animation['height']],
                fill='white'
            )

        self.animation['pac'] = self.animation['canvas'].create_arc(
            [0, 0], [self.animation['height'], self.animation['height']], fill='yellow', start=-45, extent=-270
        )

    def __menu_animation(self):
        if self.animation['cycle'] % 40 < 20:
            arc_size = -280 - (self.animation['cycle'] % 40) * 4
        else:
            arc_size = -280 - (39 - self.animation['cycle'] % 40) * 4

        if self.animation['cycle'] == 120:
            self.animation['cycle'] = 0

        for dot in range(3):
            if self.animation['cycle'] == dot * 40 + 20:
                self.animation['canvas'].move(self.animation['dot' + str(dot + 1)], self.animation['height'] * 3, 0)
            self.animation['canvas'].move(self.animation['dot' + str(dot + 1)], - 0.025 * self.animation['height'], 0)

        self.animation['cycle'] += 1

        self.animation['canvas'].itemconfig(self.animation['pac'], start=-180 - arc_size / 2, extent=arc_size)

        self.window.update()

    def __select_map(self):
        for btn in self.menu_buttons.values():
            btn.destroy()
        self.menu_buttons = {}

        self.animation['frame'].destroy()

        self.map_selector['frame'] = tk.Frame(self.menu_canvas, height=int(0.7 * self.window_height),
                                              width=int(0.8 * self.window_width), highlightbackground='purple',
                                              highlightthickness=3, bg='black')
        self.map_selector['frame'].pack_propagate(False)
        self.map_selector['frame'].place(x=int(0.5 * self.window_width), y=int(0.5 * self.window_height),
                                         anchor='center')

        self.map_selector['canvas'] = tk.Canvas(self.map_selector['frame'], bg='black', highlightthickness=0)
        self.map_selector['canvas'].pack(side='left', fill='both', expand=True)

        self.map_selector['inner_frame'] = tk.Frame(self.map_selector['canvas'], highlightbackground='purple',
                                                    highlightthickness=3, bg='black')

        self.map_selector['scrollbar'] = ttk.Scrollbar(self.map_selector['frame'], orient='vertical', cursor='hand1')
        self.map_selector['scrollbar'].pack(side='right', fill='y')

        self.map_selector['canvas'].config(yscrollcommand=self.map_selector['scrollbar'].set)
        self.map_selector['scrollbar'].config(command=self.map_selector['canvas'].yview)

        self.window.update_idletasks()

        self.map_selector['canvas'].create_window(int(0.5 * self.map_selector['canvas'].winfo_width()), 0,
                                                  anchor='n', window=self.map_selector['inner_frame'],
                                                  width=int(self.map_selector['canvas'].winfo_width()))

        self.window.update_idletasks()

        for num, game_map in enumerate(self.maps):
            with open('./maps/' + game_map) as map_file:
                map_json = json.load(map_file)
                self.map_btns[map_json['name']] = tk.Button(self.map_selector['inner_frame'], text=map_json['name'],
                                                    font=('Arial', int(self.map_selector['canvas'].winfo_height() / 15),
                                                          'bold'),
                                                    width=int(0.9 * self.map_selector['inner_frame'].winfo_width()),
                                                            fg='purple', bg='black', relief='flat', cursor='hand2',
                                                            activebackground='purple', activeforeground='black',
                                                            highlightthickness=5, highlightbackground='purple',
                                                    command=game_map)

            self.map_btns[map_json['name']].pack(side='top',
                                                 pady=int(self.map_selector['canvas'].winfo_height() / 60),
                                                 padx=int(self.map_selector['canvas'].winfo_width() / 40))

            self.map_btns[map_json['name']].bind('<Button-1>', lambda event: self.__play(event.widget.cget('command')))

        self.map_selector['canvas'].config(scrollregion=(self.map_selector['canvas'].bbox('all')))

    def __window_init(self):
        self.window = tk.Tk(className='pactime')
        self.window.title('PacTime')
        self.window.iconphoto(True, tk.PhotoImage(file='images/icon.png'))
        self.window['bg'] = 'black'
        self.window.attributes('-fullscreen', True)
        self.window.update()

        self.window_width = self.window.winfo_width()
        self.window_height = self.window.winfo_height()

        self.window.protocol("WM_DELETE_WINDOW", self.__quit)


class Game:
    main_menu = None
    field = None
    game_map = None
    pac = None

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

    __map_local_copy = None

    __game_start_time = 0
    __pause_start_time = 0
    __pause_duration = 0
    __modal_labels = []

    __time_label = None
    score_label = None

    def __init__(self, main_menu, game_map, max_game_duration):
        self.main_menu = main_menu

        self.score = 0
        self.process = 'game'

        self.__map_local_copy = game_map
        self.game_map = copy.deepcopy(self.__map_local_copy)
        self.max_game_duration = max_game_duration

    def start(self):
        self.__map_init()

        self.main_menu.window.bind('<KeyPress>', self.pac.turn)
        self.main_menu.window.bind('<KeyRelease>', self.__process_change)

        self.__game_start_time = time.time()

        try:
            while self.main_menu.window:
                self.main_menu.window.update_idletasks()
                self.__game_cycle()
                self.main_menu.window.update()
        except tk.TclError:
            pass

    def restart_game(self):
        self.field.delete('all')
        self.pac = None
        self.game_map = None

        self.score = 0
        self.process = 'game'
        self.__game_start_time = time.time()

        self.game_map = copy.deepcopy(self.__map_local_copy)
        self.__map_init()

        self.main_menu.window.bind('<KeyPress>', self.pac.turn)
        self.main_menu.window.bind('<KeyRelease>', self.__process_change)

    def __close_game(self):
        self.field.destroy()

    def __open_menu(self):
        self.__pause_start_time = time.time()
        self.__show_modal()

        self.__modal_labels.append(self.field.create_text(0.5 * self.window_width, 0.455 * self.window_height,
                                                          text='Menu', fill='white', font=('ArialBold', 18)))
        self.__modal_labels.append(self.field.create_text(0.5 * self.window_width, 0.53 * self.window_height,
                                                          text='Press "Esc" to continue game', fill='white',
                                                          font=('Arial', int(0.005 * self.window_height))))
        self.__modal_labels.append(self.field.create_text(0.5 * self.window_width, 0.55 * self.window_height,
                                                          text='Press "Enter" tо restart game', fill='white',
                                                          font=('Arial', int(0.005 * self.window_height))))

        self.process = 'menu'

    def __won_game(self):
        self.__show_modal()
        self.__modal_labels.append(self.field.create_text(0.5 * self.window_width, 0.455 * self.window_height,
                                                          text='You won!!!', fill='white',
                                                          font=('ArialBold', int(0.01 * self.window_height))))
        self.__modal_labels.append(self.field.create_text(0.5 * self.window_width, 0.485 * self.window_height,
                                                          text='Your score: ' + str(self.score), fill='white',
                                                          font=('ArialBold', int(0.008 * self.window_height))))
        self.__modal_labels.append(self.field.create_text(0.5 * self.window_width, 0.55 * self.window_height,
                                                          text='Press "Enter" tо restart game', fill='white',
                                                          font=('Arial', int(0.005 * self.window_height))))
        self.process = 'game ended'

    def __lost_game(self):
        self.__show_modal()
        self.__modal_labels.append(self.field.create_text(0.5 * self.window_width, 0.475 * self.window_height,
                                                          text="Time's up!!! \n Game over", fill='white',
                                                          font=('ArialBold', int(0.01 * self.window_height))))
        self.__modal_labels.append(self.field.create_text(0.5 * self.window_width, 0.55 * self.window_height,
                                                          text='Press "Enter" tо restart game', fill='white',
                                                          font=('Arial', int(0.005 * self.window_height))))
        self.process = 'game ended'

    def __close_menu(self):
        self.__hide_modal()

        self.process = 'game'

        self.__pause_duration += time.time() - self.__pause_start_time
        self.__pause_start_time = 0

    def __show_modal(self):
        self.__modal_labels.append(self.field.create_rectangle((0.35*self.window_width,
                                                                0.4*self.window_height),
                                                               (0.65*self.window_width,
                                                                0.6*self.window_height),
                                                               fill='black', outline='purple'))

    def __hide_modal(self):
        self.__remove_modal_labels()

    def __remove_modal_labels(self):
        for index, label in enumerate(self.__modal_labels):
            self.field.delete(label)

        self.__modal_labels = []

    def __game_cycle(self):
        try:
            time.sleep(0.03)
            if self.process == 'game':
                self.pac.move()

                game_time = self.max_game_duration - (
                            time.time() - self.__game_start_time - self.__pause_duration)

                if game_time < 0:
                    self.__lost_game()
                elif 0 == self.dot_num:
                    self.score += round(game_time * 1000)
                    self.__won_game()
                else:
                    time_m = game_time // 60
                    time_s = game_time % 60

                    if self.process == 'game':
                        self.field.itemconfig(self.__time_label,
                                              text='Time left: ' + str(int(time_m)) + ':' + str(round(time_s, 1)))
        except KeyboardInterrupt:
            exit()

    def __process_change(self, event):
        key = event.keysym
        if self.process == 'game':
            if key == 'Escape':
                self.__open_menu()
        elif self.process == 'menu':
            if key == 'Return':
                self.restart_game()
            if key == 'Escape':
                self.__close_menu()
            if key == 'BackSpace':
                self.__close_game()
                self.main_menu.open_menu()
        elif self.process == 'game ended':
            if key == 'Return':
                self.restart_game()

    def __map_init(self):
        self.window_height = self.main_menu.window_height
        self.window_width = self.main_menu.window_width

        self.cell_size = min((self.window_height * 36 / 40) // len(self.game_map),
                             (self.window_width * 39 / 40) // len(self.game_map[0]), 40)

        self.map_width = len(self.game_map[0]) * self.cell_size + 0.5 * self.cell_size
        self.map_height = len(self.game_map) * self.cell_size + 0.5 * self.cell_size

        self.offset_x = 0.5 * (self.window_width - self.map_width)
        self.offset_y = 0.5 * (1.025 * self.window_height - self.map_height)

        self.field = tk.Canvas(self.main_menu.window, width=self.window_width, height=self.window_height, bg='black')
        self.field.place(x=-1, y=-1)

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
                                    outline='black', width=self.cell_size * 2)

        self.field.create_rectangle((0, 0), (self.window_width + 1, self.window_height/20), fill='black',
                                    outline='purple')
        self.field.create_rectangle((0, self.window_height - self.window_height/40),
                                    (self.window_width + 1, self.window_height + 1),
                                    fill='black', outline='purple')

        self.score_label = self.field.create_text(40, self.window_height/40, text='Score: 0', fill='white',
                                                  font=('ArialBold', self.window_height // 50), anchor='w')

        self.__time_label = self.field.create_text(self.window_width - 40, self.window_height/40,
                                                   text='Time left: ' + str(self.max_game_duration // 60) + ':' +
                                                        str(float(self.max_game_duration % 60)),
                                                   fill='white', font=('ArialBold', self.window_height // 50),
                                                   anchor='e')

        self.field.create_text(self.window_width/2, self.window_height - self.window_height / 110, text='Menu -- "Esc"',
                               fill='white', font=('ArialBold', self.window_height // 90), anchor='center')


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
    
    def __move_mouth(self):
        if self.mouth_phase < 5:
            arc_size = -280 - self.mouth_phase * 17
        else:
            arc_size = -280 - (9 - self.mouth_phase) * 17

        if self.mouth_phase == 10:
            self.mouth_phase = 0

        self.mouth_phase += 1

        self.game.field.itemconfig(self.graphic_obj, start=self.direction - arc_size / 2, extent=arc_size)

    def __eat_dot(self):
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
        self.__move_mouth()
        self.__eat_dot()

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
            elif not self.in_cell or self.game.game_map[int(self.y)][int(self.x - 1)] != '#':
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
            elif not self.in_cell or self.game.game_map[int(self.y - 1)][int(self.x)] != '#':
                self.y = round(self.y - 0.1, 1)
                y_to_move = -0.1 * self.game.cell_size

        self.game.field.move(self.graphic_obj, x_to_move, y_to_move)


class MapGenerationError(Exception):
    pass


if __name__ == "__main__":
    menu = MainMenu()
