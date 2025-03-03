import os
import copy
import json
import time
import random

import tkinter as tk
import tkinter.ttk as ttk
from cgitb import reset
from os import remove
from time import sleep
from tkinter import messagebox
from xml.dom.pulldom import parse


class MainMenu:
    window = None
    menu_canvas = None
    window_width = 0
    window_height = 0

    menu_btns = {}
    menu_btn_phase = {}
    animation = {}

    selector_type = ''
    selector = {}
    selector_btns = {}
    selector_btn_phase = {}

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

                    for btn in list(self.menu_btns.keys()):
                        self.__btn_animation(btn, 'menu')
                    for btn in list(self.selector_btns.keys()):
                        self.__btn_animation(btn, self.selector_type)

                    self.window.update_idletasks()
                    self.window.update()
                except AttributeError and tk.TclError:
                    pass
            except KeyboardInterrupt:
                exit()

    def close_menu(self):
        self.menu_canvas.destroy()
        self.window.unbind('<Escape>')

    def __clear_menu(self):
        for widget in self.menu_canvas.place_slaves():
            widget.place_forget()

        self.window.unbind('<Escape>')

    def __play(self, selected_map):
        with open('./maps/' + selected_map) as map_file:
            game_map = json.load(map_file)

        self.close_menu()

        #game = TimeRaceGameMode(self, game_map['gameMap'], game_map['maxGameDuration'])
        game = ClassicGameMode(self, game_map['gameMap'])
        game.start()

    def __options(self):
        pass # TODO

    def __how_to_play(self):
        pass # TODO

    def __quit(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.window.destroy()
            self.window = None

    def __btn_animation(self, btn, btn_type=None):
        if btn_type == 'menu':
            cycle = self.menu_btn_phase[btn]
            if cycle:
                if cycle == 1:
                    self.menu_btns[btn].config(cursor='watch', bg='purple', fg='black')
                elif cycle <= 13:
                    self.menu_btns[btn].config(font=('Arial', self.window_height // 30 - (cycle - 7), 'bold'))
                elif cycle <= 17:
                    self.menu_btns[btn].config(font=('Arial', self.window_height // 30 + 3 - (cycle - 14), 'bold'))
                elif cycle == 18:
                    self.menu_btns[btn].config(cursor='hand2', bg='black', fg='purple')

                self.menu_btn_phase[btn] += 1

            if cycle == 19:
                self.menu_btn_phase[btn] = None

        elif btn_type == 'map_select':
            cycle = self.selector_btn_phase[btn]
            if cycle:
                if cycle == 1:
                    self.selector_btns[btn].config(cursor='watch', bg='purple', fg='black')
                elif cycle <= 13:
                    self.selector_btns[btn].config(font=('Arial', int(self.selector['canvas'].winfo_height() / 15)
                                                         - (cycle - 7), 'bold'))
                elif cycle <= 17:
                    self.selector_btns[btn].config(font=('Arial', int(self.selector['canvas'].winfo_height() / 15) + 3
                                                         - (cycle - 14), 'bold'))
                elif cycle == 18:
                    self.selector_btns[btn].config(cursor='hand2', bg='black', fg='purple')

                self.selector_btn_phase[btn] += 1

            if cycle == 19:
                self.selector_btn_phase[btn] = None
                self.__play(btn)

    def __create_menu_gui(self):
        def __click(event):
            if event.widget in self.menu_btns.values():
                event.widget.config(relief='flat')
                btn_name = list(self.menu_btns.keys())[list(self.menu_btns.values()).index(event.widget)]
                self.menu_btn_phase[btn_name] = 1
            return "break"

        self.menu_btn_phase = {'play': None, 'options': None, 'how_to_play': None, 'quit': None}
        self.__menu_animation_constructor()
        self.menu_btns['play'] = tk.Button(self.menu_canvas, text='Play', fg='purple', bg='black', relief='flat',
                                           activebackground='purple', activeforeground='black', width=15,
                                           highlightthickness=5, highlightbackground='purple', cursor='hand2',
                                           font=('Arial', self.window_height // 30, 'bold'),
                                           command=self.__open_map_selection)
        self.menu_btns['options'] = tk.Button(self.menu_canvas, text='Options', fg='purple', bg='black',
                                              relief='flat', activebackground='purple', activeforeground='black',
                                              width=15, highlightthickness=5, highlightbackground='purple',
                                              cursor='hand2', font=('Arial', self.window_height // 30, 'bold'),
                                              command=self.__options)
        self.menu_btns['how_to_play'] = tk.Button(self.menu_canvas, text='How to play', fg='purple', bg='black',
                                                  relief='flat', activebackground='purple', activeforeground='black',
                                                  width=15, highlightthickness=5, highlightbackground='purple',
                                                  cursor='hand2', font=('Arial', self.window_height // 30, 'bold'),
                                                  command=self.__how_to_play)
        self.menu_btns['quit'] = tk.Button(self.menu_canvas, text='Quit', fg='purple', bg='black', relief='flat',
                                           activebackground='purple', activeforeground='black', width=15,
                                           highlightthickness=5, highlightbackground='purple', cursor='hand2',
                                           font=('Arial', self.window_height // 30, 'bold'), command=self.__quit)

        self.menu_btns['play'].place(x=0.5 * self.window_width, y=15 / 30 * self.window_height, anchor='center')
        self.menu_btns['options'].place(x=0.5 * self.window_width, y=19 / 30 * self.window_height,
                                        anchor='center')
        self.menu_btns['how_to_play'].place(x=0.5 * self.window_width, y=23 / 30 * self.window_height,
                                            anchor='center')
        self.menu_btns['quit'].place(x=0.5 * self.window_width, y=27 / 30 * self.window_height, anchor='center')

        self.menu_canvas.bind_all('<Button-1>', __click)

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

    def __open_map_selection(self):
        btn_list = {}
        for num, game_map in enumerate(self.maps):
            with open('./maps/' + game_map) as map_file:
                btn_list[game_map] = json.load(map_file)['name']

        self.selector_type = 'map_select'
        self.__clear_menu()
        self.__construct_selector_submenu(btn_list)

    def __open_game_mode_selection(self):
        btn_list = {}
        for gm_class in Game.__subclasses__():
            btn_list[gm_class] = gm_class.__name__

        self.selector_type = 'gm_select'
        self.__clear_menu()
        self.__construct_selector_submenu(btn_list)

    def __close_selector(self):
        self.selector['frame'].destroy()
        self.window.unbind('<Escape>')
        self.open_menu()

    def __construct_selector_submenu(self, btn_list):
        def __click(event):
            if event.widget in self.selector_btns.values():
                event.widget.config(relief='flat')
                btn_name = list(self.selector_btns.keys())[list(self.selector_btns.values()).index(event.widget)]
                self.selector_btn_phase[btn_name] = 1
            return "break"

        self.selector['frame'] = tk.Frame(self.menu_canvas, height=int(0.7 * self.window_height),
                                          width=int(0.8 * self.window_width), highlightbackground='purple',
                                          highlightthickness=3, bg='black')
        self.selector['frame'].pack_propagate(False)
        self.selector['frame'].place(x=int(0.5 * self.window_width), y=int(0.5 * self.window_height),
                                     anchor='center')

        self.selector['canvas'] = tk.Canvas(self.selector['frame'], bg='black', highlightthickness=0)
        self.selector['canvas'].pack(side='left', fill='both', expand=True)

        self.selector['inner_frame'] = tk.Frame(self.selector['canvas'], highlightbackground='purple',
                                                highlightthickness=3, bg='black')

        style = ttk.Style()
        style.layout('Custom.Vertical.TScrollbar',
                     [('Vertical.Scrollbar.trough', {'sticky': 'ns', 'children':
                           [('Vertical.Scrollbar.thumb', {'sticky': 'nswe'})]})])
        style.configure('Custom.Vertical.TScrollbar', width=int(0.01 * self.window_width),
                        arrowsize=int(0.01 * self.window_width), troughcolor='black', outline='purple', borderwidth=0)
        style.map('Custom.Vertical.TScrollbar', background=[('', 'purple')])

        self.selector['scrollbar'] = ttk.Scrollbar(self.selector['frame'], orient='vertical', cursor='hand1',
                                                   style='Custom.Vertical.TScrollbar')
        self.selector['scrollbar'].pack(side='right', fill='y', padx=5, pady=5)
        self.selector['canvas'].config(yscrollcommand=self.selector['scrollbar'].set)
        self.selector['scrollbar'].config(command=self.selector['canvas'].yview)

        self.window.update_idletasks()

        self.selector['canvas'].create_window(int(0.5 * self.selector['canvas'].winfo_width()), 0,
                                              anchor='n', window=self.selector['inner_frame'],
                                              width=int(self.selector['canvas'].winfo_width()))

        self.window.update_idletasks()

        for btn_idx in btn_list.keys():
            self.selector_btns[btn_idx] = tk.Button(self.selector['inner_frame'], text=btn_list[btn_idx],
                                                    font=('Arial', int(self.selector['canvas'].winfo_height() / 15),
                                                      'bold'),
                                                    width=int(0.9 * self.selector['inner_frame'].winfo_width()),
                                                    fg='purple', bg='black', relief='flat', cursor='hand2',
                                                    activebackground='purple', activeforeground='black',
                                                    highlightthickness=5, highlightbackground='purple')
            self.selector_btns[btn_idx].pack(side='top', pady=int(self.selector['canvas'].winfo_height() / 60),
                                             padx=int(self.selector['canvas'].winfo_width() / 40))
            self.selector_btn_phase[btn_idx] = None
            self.selector_btns[btn_idx].bind('<Button-1>', __click)

        self.window.update_idletasks()
        self.selector['canvas'].config(scrollregion=(self.selector['canvas'].bbox('all')))

        # Scroll for Linux
        self.selector['inner_frame'].bind_all('<Button-4>',
                                              lambda event: self.selector['canvas'].yview_scroll(-1, 'units'))
        self.selector['inner_frame'].bind_all('<Button-5>',
                                              lambda event: self.selector['canvas'].yview_scroll(1, 'units'))

        self.window.bind('<Escape>', lambda _: self.__close_selector())

        self.window.update_idletasks()

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
    dot_num = 0

    _map_local_copy = None

    _modal = []

    def __init__(self, main_menu, game_map):
        self.main_menu = main_menu

        self._reset_properties()

        self._map_local_copy = game_map
        self.game_map = copy.deepcopy(self._map_local_copy)

    def start(self):
        self._map_init()
        self._gui_init()

        self.field.bind_all('<KeyPress>', self.pac.turn)
        self.field.bind_all('<KeyRelease>', self._process_change)

        try:
            while self.main_menu.window:
                self.main_menu.window.update_idletasks()
                self._game_cycle()
                self.main_menu.window.update()
        except tk.TclError:
            pass

    def restart_game(self):
        self.field.delete('all')
        self.pac = None
        self.game_map = None

        self._reset_properties()

        self.game_map = copy.deepcopy(self._map_local_copy)
        self._map_init()
        self._gui_init()

        self.field.bind_all('<KeyPress>', self.pac.turn)
        self.field.bind_all('<KeyRelease>', self._process_change)

    def close_game(self):
        self.field.destroy()
        self.main_menu.window.update_idletasks()
        self.field = None

    def won_game(self):
        self._show_modal()
        self._modal.append(self.field.create_text(0.5 * self.window_width, 0.455 * self.window_height,
                                                  text='You won!!!', fill='white',
                                                  font=('ArialBold', int(0.01 * self.window_height))))
        self._modal.append(self.field.create_text(0.5 * self.window_width, 0.485 * self.window_height,
                                                  text='Your score: ' + str(self.score), fill='white',
                                                  font=('ArialBold', int(0.008 * self.window_height))))
        self._modal.append(self.field.create_text(0.5 * self.window_width, 0.55 * self.window_height,
                                                  text='Press "Enter" tо restart game', fill='white',
                                                  font=('Arial', int(0.005 * self.window_height))))
        self.process = 'game ended'

    def lost_game(self):
        self._show_modal()
        self._modal.append(self.field.create_text(0.5 * self.window_width, 0.475 * self.window_height,
                                                  text="Time's up!!! \n Game over", fill='white',
                                                  font=('ArialBold', int(0.01 * self.window_height))))
        self._modal.append(self.field.create_text(0.5 * self.window_width, 0.55 * self.window_height,
                                                  text='Press "Enter" tо restart game', fill='white',
                                                  font=('Arial', int(0.005 * self.window_height))))
        self.process = 'game ended'

    def _reset_properties(self):
        self.process = 'game'

    def _open_menu(self):
        self._show_modal()

        self._modal.append(self.field.create_text(0.5 * self.window_width, 0.455 * self.window_height,
                                                  text='Menu', fill='white', font=('ArialBold', 18)))
        self._modal.append(self.field.create_text(0.5 * self.window_width, 0.53 * self.window_height,
                                                  text='Press "Esc" to continue game', fill='white',
                                                  font=('Arial', int(0.005 * self.window_height))))
        self._modal.append(self.field.create_text(0.5 * self.window_width, 0.55 * self.window_height,
                                                  text='Press "Enter" tо restart game', fill='white',
                                                  font=('Arial', int(0.005 * self.window_height))))

        self.process = 'menu'

    def _close_menu(self):
        if self.field:
            self._hide_modal()

            self.process = 'game'

    def _show_modal(self):
        self._modal.append(self.field.create_rectangle((0.35 * self.window_width, 0.4 * self.window_height),
                                                       (0.65*self.window_width, 0.6*self.window_height),
                                                       fill='black', outline='purple'))

    def _hide_modal(self):
        for element in self._modal:
            self.field.delete(element)

        self._modal = []

    def _game_cycle(self):
        try:
            time.sleep(0.03)
            if self.process == 'game':
                self.pac.move()

                self._game_rules()
        except KeyboardInterrupt:
            exit()

    def _game_rules(self):
        pass

    def _process_change(self, event):
        if self.field:
            key = event.keysym
            if self.process == 'game':
                if key == 'Escape':
                    self._open_menu()
            elif self.process == 'menu':
                if key == 'Return':
                    self.restart_game()
                if key == 'Escape':
                    self._close_menu()
                if key == 'BackSpace':
                    self.close_game()
                    self.main_menu.open_menu()
                    del self
            elif self.process == 'game ended':
                if key == 'Return':
                    self.restart_game()

    def _map_init(self):
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

                    self.game_map[row_num][cell_num] = self.field.create_rectangle((start_x, start_y), (end_x, end_y),
                                                                                   fill='white', tags="Dot")
                    self.dot_num += 1

                elif self.game_map[row_num][cell_num] == ' ':
                    pass

                else:
                    if not self._more_game_objects(row_num, cell_num):
                        raise MapGenerationError(
                            f"Unknown character found in the map table: '{self.game_map[row_num][cell_num]}'. "
                            f"If you are the creator of this map, replace the character on position "
                            f"{[row_num, cell_num]} with valid one")

        if not self.pac:
            raise MapGenerationError(
                "Map has no pacman location specified!!! If you are the creator of this map, you should "
                "set 'p' in map array to set pacman start location.")

        self.field.tag_raise("CharacterEntity", "Dot")

        self.field.create_rectangle((self.offset_x - self.cell_size, self.offset_y - self.cell_size),
                                    (self.offset_x + self.map_width + self.cell_size,
                                     self.offset_y + self.map_height + self.cell_size + 1),
                                    outline='black', width=self.cell_size * 2)

        self.field.create_rectangle((0, 0), (self.window_width + 1, self.window_height/20), fill='black',
                                    outline='purple')
        self.field.create_rectangle((0, self.window_height - self.window_height/40),
                                    (self.window_width + 1, self.window_height + 1),
                                    fill='black', outline='purple')

    def _more_game_objects(self, row_num, cell_num):
        if self.game_map[row_num][cell_num] == 'p':
            self.pac = Pac(self, cell_num, row_num)
            return True
        return False

    def _gui_init(self):
        self.field.create_text(self.window_width / 2, self.window_height - self.window_height / 110,
                               text='Menu -- "Esc"',
                               fill='white', font=('ArialBold', self.window_height // 90), anchor='center')

class ClassicGameMode(Game):
    gm_name = "Classic"

    score = 0
    ghosts = []

    def _reset_properties(self):
        self.process = 'game'
        self.score = 0
        self.ghosts = [] # comment this to see something funny

    def _gui_init(self):
        self.score_label = self.field.create_text(40, self.window_height/40, text='Score: 0', fill='white',
                                                  font=('ArialBold', self.window_height // 50), anchor='w')

        self.field.create_text(self.window_width / 2, self.window_height - self.window_height / 110,
                               text='Menu -- "Esc"',
                               fill='white', font=('ArialBold', self.window_height // 90), anchor='center')

    def _game_rules(self):
        if 0 == self.dot_num:
            self.won_game()

    def _more_game_objects(self, row_num, cell_num):
        if super()._more_game_objects(row_num, cell_num):
            return True
        elif self.game_map[row_num][cell_num] == 'g':
            self.ghosts.append(Ghost(self, cell_num, row_num, random.choice(["red", "blue", "orange", "pink", "cyan", "gray", "brown"])))
            return True
        return False

    def _game_cycle(self):
        try:
            time.sleep(0.03)
            if self.process == 'game':
                self.pac.move()

                for ghost in self.ghosts:
                    ghost.move()

                self._game_rules()
        except KeyboardInterrupt:
            exit()

class TimeRaceGameMode(Game):
    gm_name = "Time race"

    score = 0
    max_game_duration = 0

    _game_start_time = 0
    _pause_start_time = 0
    _pause_duration = 0

    _time_label = None
    score_label = None

    def __init__(self, main_menu, game_map, max_game_duration):
        super().__init__(main_menu, game_map)
        self.max_game_duration = max_game_duration

    def _open_menu(self):
        self._pause_start_time = time.time()
        super()._open_menu()

    def _close_menu(self):
        super()._close_menu()
        self._pause_duration += time.time() - self._pause_start_time
        self._pause_start_time = 0

    def _gui_init(self):
        self.score_label = self.field.create_text(40, self.window_height/40, text='Score: 0', fill='white',
                                                  font=('ArialBold', self.window_height // 50), anchor='w')

        self._time_label = self.field.create_text(self.window_width - 40, self.window_height / 40,
                                                  text='Time left: ' + str(self.max_game_duration // 60) + ':' +
                                                        str(float(self.max_game_duration % 60)),
                                                  fill='white', font=('ArialBold', self.window_height // 50),
                                                  anchor='e')

        self.field.create_text(self.window_width/2, self.window_height - self.window_height / 110, text='Menu -- "Esc"',
                               fill='white', font=('ArialBold', self.window_height // 90), anchor='center')

    def _reset_properties(self):
        self.process = 'game'
        self.score = 0
        self._game_start_time = time.time()

    def _game_rules(self):
        game_time = self.max_game_duration - (time.time() - self._game_start_time - self._pause_duration)

        if game_time < 0:
            self.pac.die()
        elif 0 == self.dot_num:
            self.score += round(game_time * 1000)
            self.won_game()
        else:
            time_m = game_time // 60
            time_s = game_time % 60

            if self.process == 'game':
                self.field.itemconfig(self._time_label,
                                      text='Time left: ' + str(int(time_m)) + ':' + str(round(time_s, 1)))

class ObstacleCourseGameMode(Game):
    gm_name = "Obstacle course"


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

    def __init__(self, game, x, y, color = "red"):
        super().__init__(game, x, y)
        self.color = color

        cs = game.cell_size
        graphic_obj_x = x * cs + game.offset_x + 0.25 * cs
        graphic_obj_y = y * cs + game.offset_y + 0.25 * cs
        self.graphic_obj = [
            game.field.create_arc([graphic_obj_x + 0.1*cs, graphic_obj_y],
                                  [graphic_obj_x + cs - 0.1*cs, graphic_obj_y + cs],
                                  fill=color, start=0, extent=180, tags=["CharacterEntity", "Ghost"]),
            game.field.create_polygon([graphic_obj_x + 0.1*cs, graphic_obj_y + 0.5*cs],
                                      [graphic_obj_x + 0.9*cs, graphic_obj_y + 0.5*cs],
                                      [graphic_obj_x + 0.9*cs, graphic_obj_y + cs],
                                      [graphic_obj_x + 0.8*cs, graphic_obj_y + 0.9*cs],
                                      [graphic_obj_x + 0.7*cs, graphic_obj_y + cs],
                                      [graphic_obj_x + 0.6*cs, graphic_obj_y + 0.9*cs],
                                      [graphic_obj_x + 0.5*cs, graphic_obj_y + cs],
                                      [graphic_obj_x + 0.4*cs, graphic_obj_y + 0.9*cs],
                                      [graphic_obj_x + 0.3*cs, graphic_obj_y + cs],
                                      [graphic_obj_x + 0.2*cs, graphic_obj_y + 0.9*cs],
                                      [graphic_obj_x + 0.1*cs, graphic_obj_y + cs],
                                      fill=color, tags=["CharacterEntity", "Ghost"]),
            game.field.create_rectangle([graphic_obj_x + 0.25*cs, graphic_obj_y + 0.4*cs],
                                        [graphic_obj_x + 0.4*cs, graphic_obj_y + 0.55*cs],
                                        fill="black", outline="white", tags=["CharacterEntity", "Ghost"]),
            game.field.create_rectangle([graphic_obj_x + 0.6*cs, graphic_obj_y + 0.4*cs],
                                        [graphic_obj_x + 0.75*cs, graphic_obj_y + 0.55*cs],
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

class MapGenerationError(Exception):
    pass


if __name__ == "__main__":
    menu = MainMenu()
