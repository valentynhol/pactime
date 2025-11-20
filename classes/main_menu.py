import os
import time
import json
import tkinter as tk
import tkinter.ttk as ttk

from classes.game import Game

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

    curr_gm_class = None

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
                time.sleep(0.01)
                self.__menu_animation()

                for btn in list(self.menu_btns.keys()):
                    self.__btn_animation(btn, 'menu')
                for btn in list(self.selector_btns.keys()):
                    self.__btn_animation(btn, 'selector')

                if self.window:
                    self.window.update_idletasks()
                    self.window.update()
                else:
                    break
            except KeyboardInterrupt:
                break

    def close_menu(self):
        self.menu_canvas.destroy()
        self.window.unbind('<Escape>')

    def __clear_menu(self):
        for widget in self.menu_canvas.place_slaves():
            widget.place_forget()

        self.window.unbind('<Escape>')

    def __start_game(self, selected_map):
        with open('./maps/' + selected_map) as map_file:
            game_map = json.load(map_file)

        self.close_menu()

        game = self.curr_gm_class(self, game_map)
        game.start()

    def __options(self):
        pass # TODO

    def __multiplayer_game(self):
        pass # TODO

    def __quit(self):
        self.window.quit()
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
                if btn == "singleplayer":
                    self.__open_game_mode_selection()
                elif btn == "multiplayer":
                    self.__multiplayer_game()
                elif btn == "options":
                    self.__options()
                elif btn == "quit":
                    self.__quit()

        elif btn_type == 'selector':
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
                if self.selector_type == "map_select":
                    self.__start_game(btn)
                elif self.selector_type == "gm_select":
                    self.__open_map_selection(btn)

    def __create_menu_gui(self):
        self.menu_btn_phase = {'singleplayer': None, 'multiplayer': None, 'options': None, 'quit': None}
        self.__menu_animation_constructor()
        self.menu_btns['singleplayer'] = tk.Button(self.menu_canvas, text='Singleplayer', fg='purple', bg='black',
                                                   relief='flat', activebackground='purple', activeforeground='black',
                                                   width=15, highlightthickness=5, highlightbackground='purple',
                                                   cursor='hand2', font=('Arial', self.window_height // 30, 'bold'))
        self.menu_btns['multiplayer'] = tk.Button(self.menu_canvas, text='Multiplayer', fg='purple', bg='black',
                                                  relief='flat', activebackground='purple', activeforeground='black',
                                                  width=15, highlightthickness=5, highlightbackground='purple',
                                                  cursor='hand2', font=('Arial', self.window_height // 30, 'bold'))
        self.menu_btns['options'] = tk.Button(self.menu_canvas, text='Options', fg='purple', bg='black',
                                              relief='flat', activebackground='purple', activeforeground='black',
                                              width=15, highlightthickness=5, highlightbackground='purple',
                                              cursor='hand2', font=('Arial', self.window_height // 30, 'bold'))
        self.menu_btns['quit'] = tk.Button(self.menu_canvas, text='Quit', fg='purple', bg='black', relief='flat',
                                           activebackground='purple', activeforeground='black', width=15,
                                           highlightthickness=5, highlightbackground='purple', cursor='hand2',
                                           font=('Arial', self.window_height // 30, 'bold'))

        self.menu_btns['singleplayer'].place(x=0.5 * self.window_width, y=15 / 30 * self.window_height, anchor='center')
        self.menu_btns['multiplayer'].place(x=0.5 * self.window_width, y=19 / 30 * self.window_height, anchor='center')
        self.menu_btns['options'].place(x=0.5 * self.window_width, y=23 / 30 * self.window_height, anchor='center')
        self.menu_btns['quit'].place(x=0.5 * self.window_width, y=27 / 30 * self.window_height, anchor='center')

        self.menu_canvas.bind_all('<Button-1>', self.__btn_click)

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

    def __open_map_selection(self, gm_class):
        self.curr_gm_class = gm_class

        btn_list = {}
        for num, game_map in enumerate(self.maps):
            with open('./maps/' + game_map) as map_file:
                map_json = json.load(map_file)
                if gm_class.gm_short in map_json["gameModes"]:
                    btn_list[game_map] = map_json['name']

        self.selector_type = "map_select"
        self.__clear_menu()
        self.__construct_selector_submenu(btn_list)

    def __open_game_mode_selection(self):
        btn_list = {}
        for gm_class in Game.__subclasses__():
            btn_list[gm_class] = gm_class.gm_name

        self.selector_type = "gm_select"
        self.__clear_menu()
        self.__construct_selector_submenu(btn_list)

    def __close_selector(self):
        self.selector['frame'].destroy()
        self.window.unbind('<Escape>')
        self.open_menu()

    def __construct_selector_submenu(self, btn_list):
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
            self.selector_btns[btn_idx].bind('<Button-1>', self.__btn_click)

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
        self.window.unbind_all("<<NextWindow>>")
        self.window.unbind_all("<<PrevWindow>>")
        self.window.title('PacTime')
        self.window.iconphoto(True, tk.PhotoImage(file='images/icon.png'))
        self.window['bg'] = 'black'
        self.window.attributes('-fullscreen', True)
        self.window.update()

        self.window_width = self.window.winfo_width()
        self.window_height = self.window.winfo_height()

        self.window.protocol("WM_DELETE_WINDOW", self.__quit)

    def __btn_click(self, event):
        if event.widget in self.menu_btns.values():
            btn_name = list(self.menu_btns.keys())[list(self.menu_btns.values()).index(event.widget)]
            self.menu_btn_phase[btn_name] = 1
        elif event.widget in self.selector_btns.values():
            btn_name = list(self.selector_btns.keys())[list(self.selector_btns.values()).index(event.widget)]
            self.selector_btn_phase[btn_name] = 1

        event.widget.config(relief='flat')
        return "break"
