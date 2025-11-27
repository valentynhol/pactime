import os
import time
import json
import tkinter as tk
from queue import Queue

from classes.gui.pages.lobby_code_form import LobbyCodeForm
from classes.gui.pages.lobby_submenu import LobbySubmenu
from classes.gui.pages.page import Page
from classes.gui.pages.username_form import UsernameForm
from classes.gui.pages.btn_list_submenu import BtnListSubmenu
from classes.gui.pages.start_screen import StartScreen

from classes.game import Game
from classes.multiplayer import MultiplayerGameWrapper
from constants import USERDATA_FILE


class GameWindow(tk.Tk):
    def __init__(self):
        self.gui_queue = Queue()
        self.maps = os.listdir('./maps')
        self.maps.sort()

        super().__init__(className='pactime')

        self.geometry(f"+{self.winfo_pointerx()}+{self.winfo_pointery()}")

        self.unbind_all("<<NextWindow>>")
        self.unbind_all("<<PrevWindow>>")
        self.title('PacTime')
        self.iconphoto(True, tk.PhotoImage(file='images/icon.png'))
        self.configure(background='black')
        self.attributes('-fullscreen', True)
        self.protocol("WM_DELETE_WINDOW", self.quit)

        self.update()

        self.window_width = self.winfo_width()
        self.window_height = self.winfo_height()
        self.multiplayer_wrapper = None

        self.page = StartScreen(self)

        self.mainloop()

    def singleplayer(self):
        self.multiplayer_wrapper = None
        self.open_game_mode_selector()

    def multiplayer(self):
        self.multiplayer_wrapper = MultiplayerGameWrapper(self)

        if os.path.isfile(USERDATA_FILE):
            with open(USERDATA_FILE) as json_file:
                data = json.load(json_file)
                username = data.get('username')
                if username:
                    self.open_multiplayer_action_selector(username)
                    return

        self.open_username_form()

    def options(self):
        pass  # TODO

    def quit(self):
        if self.multiplayer_wrapper:
            self.multiplayer_wrapper.disconnect_ws()

        super().quit()

    def open_menu(self):
        while self:
            try:
                time.sleep(0.01)
                self.after(0, self._process_gui_queue)

                self.update_idletasks()
                self.update()
            except KeyboardInterrupt or AttributeError:
                break

    def start_game(self, gm_class, selected_map):
        with open('./maps/' + selected_map) as map_file:
            game_map = json.load(map_file)

        if self.multiplayer_wrapper:
            self.multiplayer_wrapper.start_game(game_map)
        else:
            self.unbind('<Escape>')
            print(gm_class)
            game = gm_class(self, game_map)
            game.start()

    def open_start_screen(self):
        self.multiplayer_wrapper = None
        self.close_submenus()
        self.page = StartScreen(self)

    def open_map_selector(self, gm_class):
        btn_list = []
        for num, game_map in enumerate(self.maps):
            with open('./maps/' + game_map) as map_file:
                map_json = json.load(map_file)
                if gm_class.gm_short in map_json["gameModes"]:
                    btn_list.append((map_json['name'], lambda gm=gm_class, g_map=game_map: self.start_game(gm, g_map)))

        self.close_submenus()
        self.page = BtnListSubmenu(self, btn_list)

    def open_game_mode_selector(self):
        btn_list = []
        for gm_class in Game.__subclasses__():
            if self.multiplayer_wrapper:
                action = lambda gm=gm_class: self.open_lobby_submenu(self.multiplayer_wrapper.create(gm))
            else:
                action = lambda gm=gm_class: self.open_map_selector(gm)
            btn_list.append((gm_class.gm_name, action))

        self.close_submenus()
        self.page = BtnListSubmenu(self, btn_list)

    def open_multiplayer_action_selector(self, username):
        if os.path.isfile(USERDATA_FILE):
            with open(USERDATA_FILE) as json_file:
                data = json.load(json_file)
            lobby_code = data.get('lobby_code')
            if lobby_code:
                self.open_lobby_submenu(self.multiplayer_wrapper.join(lobby_code, username))
                return # TODO: rewrite

        with open(USERDATA_FILE, 'w') as json_file:
            json_file.write(json.dumps({'username': username}))

        btn_list = [
            ('Create a lobby', self.open_game_mode_selector),
            ('Join a lobby', self.open_lobby_selector),
            ('Join a lobby by code', self.open_lobby_code_form),
            ('Change username', self.open_username_form)
        ]

        self.close_submenus()
        self.page = BtnListSubmenu(self, btn_list)

    def open_lobby_selector(self):
        self.close_submenus()
        self.page = BtnListSubmenu(self, self.multiplayer_wrapper.get_lobby_list())

    def open_lobby_submenu(self, lobby_info):
        self.close_submenus()
        self.page = LobbySubmenu(self, lobby_info)

    def open_lobby_code_form(self):
        self.close_submenus()
        self.page = LobbyCodeForm(self)

    def open_username_form(self):
        self.close_submenus()
        self.page = UsernameForm(self)

    def close_submenus(self):
        if self.page:
            self.page.destroy()
            self.page = None

        self.unbind('<Escape>')

    def _process_gui_queue(self):
        while not self.gui_queue.empty():
            callback = self.gui_queue.get_nowait()
            callback()
