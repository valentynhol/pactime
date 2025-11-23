import os
import time
import json
import tkinter as tk
import tkinter.ttk as ttk
from queue import Queue

from classes.game import Game
from classes.multiplayer import MultiplayerGameWrapper

class MainMenu:
    window = None
    menu_canvas = None
    window_width = 0
    window_height = 0

    gui_queue = None

    menu_btns = {}
    menu_btn_phase = {}
    animation = {}

    selector_type = ''
    selector = {}
    selector_btns = {}
    selector_btn_phase = {}

    curr_gm_class = None

    multiplayer = None

    maps = os.listdir('./maps')

    def __init__(self):
        self.gui_queue = Queue()
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
                self.window.after(0, self.__process_gui_queue())

                for btn in list(self.menu_btns.keys()):
                    self.__btn_animation(btn, 'menu')
                for btn in list(self.selector_btns.keys()):
                    self.__btn_animation(btn, 'selector')

                if self.window:
                    self.window.update_idletasks()
                    self.window.update()
                else:
                    break
            except KeyboardInterrupt or AttributeError:
                break

    def close_menu(self):
        self.menu_canvas.destroy()
        self.window.unbind('<Escape>')

    def update_lobby_gui(self, player_list):
        if not self.selector_type == 'lobby':
            pass

        print(player_list)

        for label in self.selector['players'].keys():
            self.selector['players'][label].destroy()

        self.selector_btns['start_game'].pack_forget()
        self.selector_btns['leave_lobby'].pack_forget()
        self.selector_btns['delete_lobby'].pack_forget()

        for player in player_list:
            self.selector['players'][player] = tk.Label(self.selector['inner_frame'], text=player,
                                                        font=('Arial',
                                                              int(self.selector['canvas'].winfo_height() / 30), 'bold'),
                                                        fg='purple', bg='black')
            self.selector['players'][player].pack(side='top', pady=int(self.selector['canvas'].winfo_height() / 120),
                                                  padx=int(self.selector['canvas'].winfo_width() / 40))

        self.selector_btns['start_game'].pack(side='top', pady=int(self.selector['canvas'].winfo_height() / 60),
                                              padx=int(self.selector['canvas'].winfo_width() / 40))
        self.selector_btns['leave_lobby'].pack(side='top', pady=int(self.selector['canvas'].winfo_height() / 60),
                                               padx=int(self.selector['canvas'].winfo_width() / 40))
        self.selector_btns['delete_lobby'].pack(side='top', pady=int(self.selector['canvas'].winfo_height() / 60),
                                                padx=int(self.selector['canvas'].winfo_width() / 40))

        self.window.update_idletasks()

        self.selector['canvas'].config(scrollregion=(self.selector['canvas'].bbox('all')))

    def __clear_menu(self):
        for widget in self.menu_canvas.place_slaves():
            widget.place_forget()

        self.window.unbind('<Escape>')

    def __start_game(self, selected_map):
        with open('./maps/' + selected_map) as map_file:
            game_map = json.load(map_file)

        if self.multiplayer:
            username = None
            with open('./user_data/multiplayer.json') as json_file:
                data = json.load(json_file)
                username = data.get('username')

            if username:
                lobby_name, lobby_code, players = self.multiplayer.create(self.curr_gm_class, game_map, username)
                self.__create_lobby_gui(lobby_name, lobby_code, players)
        else:
            self.close_menu()
            game = self.curr_gm_class(self, game_map)
            game.start()

    def __options(self):
        pass # TODO

    def __multiplayer_game(self, selected_option):
        if selected_option == 'create':
            self.__open_game_mode_selection()
        elif selected_option == 'join':
            self.selector_type = 'lobby_list'
            self.__clear_menu()
            self.__construct_selector_submenu(self.multiplayer.get_lobby_list())
        elif selected_option == 'join_code':
            self.__open_multiplayer_lobby_code_field()

    def __quit(self):
        if self.multiplayer:
            self.multiplayer.disconnect_ws()

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
                    self.multiplayer = None
                    self.__open_game_mode_selection()
                elif btn == "multiplayer":
                    self.multiplayer = MultiplayerGameWrapper(self)

                    if os.path.isfile('./user_data/multiplayer.json'):
                        with open('./user_data/multiplayer.json') as json_file:
                            data = json.load(json_file)
                            username = data.get('username')
                            if username:
                                self.__open_multiplayer_game_lobby_selector(username)
                                return

                    self.__open_multiplayer_username_field()
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
                elif self.selector_type == "lobby_join_create":
                    if btn == 'change_username':
                        self.__open_multiplayer_username_field()
                        return

                    self.__multiplayer_game(btn)
                elif self.selector_type == "username":
                    username = self.selector['textbox'].get()
                    if username:
                        self.__open_multiplayer_game_lobby_selector(username)
                elif self.selector_type == "get_lobby_code":
                    if os.path.isfile('./user_data/multiplayer.json'):
                        username = None
                        with open('./user_data/multiplayer.json') as json_file:
                            data = json.load(json_file)
                            username = data.get('username')

                        lobby_code = self.selector['textbox'].get()

                        if username and lobby_code:
                            lobby_name, lobby_code, players = self.multiplayer.join(lobby_code, username)
                            self.__create_lobby_gui(lobby_name, lobby_code, players)
                elif self.selector_type == "lobby_list":
                    username = None
                    with open('./user_data/multiplayer.json') as json_file:
                        data = json.load(json_file)
                        username = data.get('username')

                    lobby_name, lobby_code, players = self.multiplayer.join(btn, username)
                    self.__create_lobby_gui(lobby_name, lobby_code, players)
                elif self.selector_type == "lobby":
                    if btn == 'start_game':
                        self.multiplayer.play()
                    elif btn == 'leave_lobby':
                        self.multiplayer.leave()
                        self.__close_selector()
                        self.open_menu()
                    elif btn == 'delete_lobby':
                        self.multiplayer.delete()
                        self.__close_selector()
                        self.open_menu()

    def __process_gui_queue(self):
        while not self.gui_queue.empty():
            callback = self.gui_queue.get_nowait()
            callback()

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

    # TODO: rewrite
    def __create_lobby_gui(self, lobby_name, lobby_code, player_list):
        self.selector_type = 'lobby'
        self.__clear_menu()

        self.selector['frame'] = tk.Frame(self.menu_canvas, height=int(0.7 * self.window_height),
                                          width=int(0.8 * self.window_width), highlightbackground='purple',
                                          highlightthickness=5, bg='black', highlightcolor='purple')
        self.selector['frame'].pack_propagate(False)
        self.selector['frame'].place(x=int(0.5 * self.window_width), y=int(0.5 * self.window_height),
                                     anchor='center')

        self.selector['canvas'] = tk.Canvas(self.selector['frame'], bg='black', highlightthickness=0)
        self.selector['canvas'].pack(side='left', fill='both', expand=True)

        self.selector['inner_frame'] = tk.Frame(self.selector['canvas'], bg='black')

        self.window.update_idletasks()

        self.selector['canvas'].create_window(int(0.5 * self.selector['canvas'].winfo_width()), 0,
                                              anchor='n', window=self.selector['inner_frame'],
                                              width=int(self.selector['canvas'].winfo_width()))

        style = ttk.Style()
        style.layout('Custom.Vertical.TScrollbar',
                     [('Vertical.Scrollbar.trough', {'sticky': 'ns', 'children':
                         [('Vertical.Scrollbar.thumb', {'sticky': 'nswe'})]})])
        style.configure('Custom.Vertical.TScrollbar', width=int(0.01 * self.window_width),
                        arrowsize=int(0.01 * self.window_width), troughcolor='black', outline='purple', borderwidth=0)
        style.map('Custom.Vertical.TScrollbar', background=[('', 'purple')])

        self.selector['scrollbar'] = ttk.Scrollbar(self.selector['frame'], cursor='hand1',
                                                   style='Custom.Vertical.TScrollbar')
        self.selector['scrollbar'].pack(side='right', fill='y', padx=5, pady=5)
        self.selector['canvas'].config(yscrollcommand=self.selector['scrollbar'].set)
        self.selector['scrollbar'].config(command=self.selector['canvas'].yview)

        self.window.update_idletasks()

        self.selector['lobby_name'] = tk.Label(self.selector['inner_frame'], text=lobby_name,
                                               font=('Arial', int(self.selector['canvas'].winfo_height() / 15),
                                                     'bold'),
                                               fg='purple', bg='black')
        self.selector['lobby_name'].pack(side='top', pady=int(self.selector['canvas'].winfo_height() / 60),
                                         padx=int(self.selector['canvas'].winfo_width() / 40))

        self.selector['code_label'] = tk.Label(self.selector['inner_frame'], text=f'Lobby code:',
                                               font=('Arial', int(self.selector['canvas'].winfo_height() / 15),
                                                     'bold'),
                                               fg='purple', bg='black')
        self.selector['code_label'].pack(side='top', pady=int(self.selector['canvas'].winfo_height() / 60),
                                         padx=int(self.selector['canvas'].winfo_width() / 40))

        self.selector['textbox'] = tk.Text(self.selector['inner_frame'],
                                            font=('Arial', int(self.selector['canvas'].winfo_height() / 15), 'bold'),
                                            width=int(0.9 * self.selector['inner_frame'].winfo_width()), height=1,
                                            fg='purple', bg='black', relief='flat', cursor='hand2',
                                            selectbackground='purple', highlightthickness=5,
                                            highlightbackground='purple', highlightcolor='purple',
                                            insertbackground='purple', insertwidth=5, wrap="none")
        self.selector['textbox'].insert(tk.END, lobby_code)
        self.selector['textbox'].config(state='disabled')
        self.selector['textbox'].pack(side='top', pady=int(self.selector['canvas'].winfo_height() / 60),
                                      padx=int(self.selector['canvas'].winfo_width() / 40))

        self.selector['player_list_label'] = tk.Label(self.selector['inner_frame'], text='Players: ',
                                                      font=('Arial', int(self.selector['canvas'].winfo_height() / 15),
                                                            'bold'),
                                                      fg='purple', bg='black')
        self.selector['player_list_label'].pack(side='top', pady=int(self.selector['canvas'].winfo_height() / 120),
                                                padx=int(self.selector['canvas'].winfo_width() / 40))

        self.selector['players'] = {}
        for player in player_list:
            self.selector['players'][player] = tk.Label(self.selector['inner_frame'], text=player,
                                                        font=('Arial',
                                                              int(self.selector['canvas'].winfo_height() / 30), 'bold'),
                                                        fg='purple', bg='black')
            self.selector['players'][player].pack(side='top', pady=int(self.selector['canvas'].winfo_height() / 120),
                                                  padx=int(self.selector['canvas'].winfo_width() / 40))

        self.selector_btns['start_game'] = tk.Button(self.selector['inner_frame'], text='Start Game',
                                                     font=('Arial', int(self.selector['canvas'].winfo_height() / 15),
                                                           'bold'),
                                                     width=int(0.9 * self.selector['inner_frame'].winfo_width()),
                                                     fg='purple', bg='black', relief='flat', cursor='hand2',
                                                     activebackground='purple', activeforeground='black',
                                                     highlightthickness=5, highlightbackground='purple')
        self.selector_btns['start_game'].pack(side='top', pady=int(self.selector['canvas'].winfo_height() / 60),
                                              padx=int(self.selector['canvas'].winfo_width() / 40))

        self.selector_btns['leave_lobby'] = tk.Button(self.selector['inner_frame'], text='Leave Lobby',
                                                      font=('Arial', int(self.selector['canvas'].winfo_height() / 15),
                                                            'bold'),
                                                      width=int(0.9 * self.selector['inner_frame'].winfo_width()),
                                                      fg='purple', bg='black', relief='flat', cursor='hand2',
                                                      activebackground='purple', activeforeground='black',
                                                      highlightthickness=5, highlightbackground='purple')
        self.selector_btns['leave_lobby'].pack(side='top', pady=int(self.selector['canvas'].winfo_height() / 60),
                                               padx=int(self.selector['canvas'].winfo_width() / 40))

        self.selector_btns['delete_lobby'] = tk.Button(self.selector['inner_frame'], text='Delete Lobby',
                                                       font=('Arial', int(self.selector['canvas'].winfo_height() / 15),
                                                             'bold'),
                                                       width=int(0.9 * self.selector['inner_frame'].winfo_width()),
                                                       fg='purple', bg='black', relief='flat', cursor='hand2',
                                                       activebackground='purple', activeforeground='black',
                                                       highlightthickness=5, highlightbackground='purple')
        self.selector_btns['delete_lobby'].pack(side='top', pady=int(self.selector['canvas'].winfo_height() / 60),
                                                padx=int(self.selector['canvas'].winfo_width() / 40))

        self.selector_btn_phase['start_game'] = None
        self.selector_btn_phase['leave_lobby'] = None
        self.selector_btn_phase['delete_lobby'] = None
        self.selector_btns['start_game'].bind('<Button-1>', self.__btn_click)
        self.selector_btns['leave_lobby'].bind('<Button-1>', self.__btn_click)
        self.selector_btns['delete_lobby'].bind('<Button-1>', self.__btn_click)

        self.window.update_idletasks()
        self.selector['canvas'].config(scrollregion=(self.selector['canvas'].bbox('all')))

        self.window.bind('<Escape>', lambda _: self.__close_selector())

    def __open_multiplayer_game_lobby_selector(self, username):
        if os.path.isfile('./user_data/multiplayer.json'):
            with open('./user_data/multiplayer.json') as json_file:
                data = json.load(json_file)
                lobby_code = data.get('lobby_code')
                if lobby_code:
                    lobby_name, lobby_code, players = self.multiplayer.join(lobby_code, username)
                    self.__create_lobby_gui(lobby_name, lobby_code, players)
                    return

        with open('./user_data/multiplayer.json', 'w') as json_file:
            json_file.write(json.dumps({'username': username}))

        btn_list = {'create': 'Create a lobby', 'join': 'Join a lobby',
                    'join_code': 'Join a lobby by code', 'change_username': 'Change username'}

        self.selector_type = 'lobby_join_create'
        self.__clear_menu()
        self.__construct_selector_submenu(btn_list)

    # TODO: rewrite
    def __open_multiplayer_lobby_code_field(self):
        self.selector_type = 'get_lobby_code'
        self.__clear_menu()

        self.selector['frame'] = tk.Frame(self.menu_canvas, height=int(0.7 * self.window_height),
                                          width=int(0.8 * self.window_width), highlightbackground='purple',
                                          highlightthickness=5, bg='black', highlightcolor='purple')
        self.selector['frame'].pack_propagate(False)
        self.selector['frame'].place(x=int(0.5 * self.window_width), y=int(0.5 * self.window_height),
                                     anchor='center')

        self.selector['canvas'] = tk.Canvas(self.selector['frame'], bg='black', highlightthickness=0)
        self.selector['canvas'].pack(side='left', fill='both', expand=True)

        self.selector['inner_frame'] = tk.Frame(self.selector['canvas'], bg='black')

        self.window.update_idletasks()

        self.selector['canvas'].create_window(int(0.5 * self.selector['canvas'].winfo_width()), 0,
                                              anchor='n', window=self.selector['inner_frame'],
                                              width=int(self.selector['canvas'].winfo_width()))

        self.window.update_idletasks()

        self.selector['textbox_label'] = tk.Label(self.selector['inner_frame'], text='Lobby code:',
                                                  font=('Arial', int(self.selector['canvas'].winfo_height() / 15),
                                                        'bold'),
                                                  fg='purple', bg='black')
        self.selector['textbox_label'].pack(side='top', pady=int(self.selector['canvas'].winfo_height() / 60),
                                            padx=int(self.selector['canvas'].winfo_width() / 40))

        self.selector['textbox'] = tk.Entry(self.selector['inner_frame'],
                                            font=('Arial', int(self.selector['canvas'].winfo_height() / 15), 'bold'),
                                            width=int(0.9 * self.selector['inner_frame'].winfo_width()),
                                            fg='purple', bg='black', relief='flat', cursor='hand2',
                                            selectbackground='purple', highlightthickness=5,
                                            highlightbackground='purple', highlightcolor='purple',
                                            insertbackground='purple', insertwidth=5)
        self.selector['textbox'].focus_force()
        self.selector['textbox'].pack(side='top', pady=int(self.selector['canvas'].winfo_height() / 60),
                                      padx=int(self.selector['canvas'].winfo_width() / 40))

        self.selector_btns['confirm_button'] = tk.Button(self.selector['inner_frame'], text='Confirm',
                                                         font=('Arial',
                                                               int(self.selector['canvas'].winfo_height() / 15),
                                                               'bold'),
                                                         width=int(0.9 * self.selector['inner_frame'].winfo_width()),
                                                         fg='purple', bg='black', relief='flat', cursor='hand2',
                                                         activebackground='purple', activeforeground='black',
                                                         highlightthickness=5, highlightbackground='purple')
        self.selector_btns['confirm_button'].pack(side='top', pady=int(self.selector['canvas'].winfo_height() / 60),
                                                  padx=int(self.selector['canvas'].winfo_width() / 40))

        self.selector_btn_phase['confirm_button'] = None
        self.selector_btns['confirm_button'].bind('<Button-1>', self.__btn_click)

        self.window.update_idletasks()

        self.window.bind('<Escape>', lambda _: self.__close_selector())

    # TODO: rewrite
    def __open_multiplayer_username_field(self):
        self.selector_type = 'username'
        self.__clear_menu()

        self.selector['frame'] = tk.Frame(self.menu_canvas, height=int(0.7 * self.window_height),
                                          width=int(0.8 * self.window_width), highlightbackground='purple',
                                          highlightthickness=5, bg='black', highlightcolor='purple')
        self.selector['frame'].pack_propagate(False)
        self.selector['frame'].place(x=int(0.5 * self.window_width), y=int(0.5 * self.window_height),
                                     anchor='center')

        self.selector['canvas'] = tk.Canvas(self.selector['frame'], bg='black', highlightthickness=0)
        self.selector['canvas'].pack(side='left', fill='both', expand=True)

        self.selector['inner_frame'] = tk.Frame(self.selector['canvas'], bg='black')

        self.window.update_idletasks()

        self.selector['canvas'].create_window(int(0.5 * self.selector['canvas'].winfo_width()), 0,
                                              anchor='n', window=self.selector['inner_frame'],
                                              width=int(self.selector['canvas'].winfo_width()))

        self.window.update_idletasks()

        self.selector['textbox_label'] = tk.Label(self.selector['inner_frame'], text='Your username:',
                                                  font=('Arial', int(self.selector['canvas'].winfo_height() / 15),
                                                        'bold'),
                                                  fg='purple', bg='black')
        self.selector['textbox_label'].pack(side='top', pady=int(self.selector['canvas'].winfo_height() / 60),
                                            padx=int(self.selector['canvas'].winfo_width() / 40))

        self.selector['textbox'] = tk.Entry(self.selector['inner_frame'],
                                            font=('Arial', int(self.selector['canvas'].winfo_height() / 15), 'bold'),
                                            width=int(0.9 * self.selector['inner_frame'].winfo_width()),
                                            fg='purple', bg='black', relief='flat', cursor='hand2',
                                            selectbackground='purple', highlightthickness=5,
                                            highlightbackground='purple', highlightcolor='purple',
                                            insertbackground='purple', insertwidth=5)
        self.selector['textbox'].focus_force()
        self.selector['textbox'].pack(side='top', pady=int(self.selector['canvas'].winfo_height() / 60),
                                      padx=int(self.selector['canvas'].winfo_width() / 40))

        self.selector_btns['confirm_button'] = tk.Button(self.selector['inner_frame'], text='Confirm',
                                                         font=('Arial',
                                                               int(self.selector['canvas'].winfo_height() / 15),
                                                               'bold'),
                                                         width=int(0.9 * self.selector['inner_frame'].winfo_width()),
                                                         fg='purple', bg='black', relief='flat', cursor='hand2',
                                                         activebackground='purple', activeforeground='black',
                                                         highlightthickness=5, highlightbackground='purple')
        self.selector_btns['confirm_button'].pack(side='top', pady=int(self.selector['canvas'].winfo_height() / 60),
                                                  padx=int(self.selector['canvas'].winfo_width() / 40))

        self.selector_btn_phase['confirm_button'] = None
        self.selector_btns['confirm_button'].bind('<Button-1>', self.__btn_click)

        self.window.update_idletasks()

        self.window.bind('<Escape>', lambda _: self.__close_selector())

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
                                          highlightthickness=5, bg='black', highlightcolor='purple')
        self.selector['frame'].pack_propagate(False)
        self.selector['frame'].place(x=int(0.5 * self.window_width), y=int(0.5 * self.window_height),
                                     anchor='center')

        self.selector['canvas'] = tk.Canvas(self.selector['frame'], bg='black', highlightthickness=0)
        self.selector['canvas'].pack(side='left', fill='both', expand=True)

        self.selector['inner_frame'] = tk.Frame(self.selector['canvas'], bg='black')

        style = ttk.Style()
        style.layout('Custom.Vertical.TScrollbar',
                     [('Vertical.Scrollbar.trough', {'sticky': 'ns', 'children':
                           [('Vertical.Scrollbar.thumb', {'sticky': 'nswe'})]})])
        style.configure('Custom.Vertical.TScrollbar', width=int(0.01 * self.window_width),
                        arrowsize=int(0.01 * self.window_width), troughcolor='black', outline='purple', borderwidth=0)
        style.map('Custom.Vertical.TScrollbar', background=[('', 'purple')])

        self.selector['scrollbar'] = ttk.Scrollbar(self.selector['frame'], cursor='hand1',
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

        px = self.window.winfo_pointerx()
        py = self.window.winfo_pointery()
        self.window.geometry(f"+{px}+{py}")

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
