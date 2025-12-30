import os
import json
import tkinter as tk
import typing

from classes.exceptions import AuthFailedException
from classes.gui.pages.game_page import GamePage
from classes.gui.pages.game_start_countdown import GameStartCountdown
from classes.gui.pages.google_login_page import GoogleLoginPage
from classes.gui.pages.lobby_code_form import LobbyCodeForm
from classes.gui.pages.lobby_page import LobbySubmenu
from classes.gui.pages.page import Page
from classes.gui.pages.username_form import UsernameForm
from classes.gui.pages.btn_list_submenu import BtnListSubmenu
from classes.gui.pages.start_screen import StartScreen

from classes.game import Game
from classes.multiplayer import MultiplayerGameWrapper
from constants import USERDATA_FILE


class GameWindow(tk.Tk):
    def __init__(self):
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
        self.multiplayer_wrapper: typing.Optional[MultiplayerGameWrapper] = None

        self.page_stack: list[Page] = []
        self.page = StartScreen(self)
        self.remember_page = True

        self.mainloop()

    def singleplayer(self):
        self.multiplayer_wrapper = None
        self.open_game_mode_selector()

    def multiplayer(self):
        token = GoogleLoginPage.get_credentials()
        if token:
            try:
                self.multiplayer_wrapper = MultiplayerGameWrapper(self, token)
            except AuthFailedException:
                self.open_login_page()
        else:
            self.open_login_page()

    def options(self):
        pass  # TODO

    def quit(self):
        if self.multiplayer_wrapper:
            self.multiplayer_wrapper.disconnect_ws()

        super().quit()

    def open_page(self, page_factory: typing.Callable, remember=True, can_return=True):
        if self.page:
            if self.remember_page:
                self.page_stack.append(self.page)
            else:
                self.page.destroy()

        self.remember_page = remember

        if can_return:
            self.bind('<Escape>', lambda e: self.open_previous_page())
        else:
            self.unbind('<Escape>')

        self.page = page_factory()
        return self.page

    def open_previous_page(self):
        if not self.page_stack:
            self.open_start_screen()
            return

        if self.page:
            self.page.destroy()

        self.page = self.page_stack.pop()

    def open_start_screen(self):
        self.multiplayer_wrapper = None
        for page in self.page_stack:
            page.destroy()
        self.page_stack.clear()
        self.open_page(lambda: StartScreen(self), can_return=False)

    def start_game(self, gm_class, selected_map):
        with open('./maps/' + selected_map) as map_file:
            game_map = json.load(map_file)

        if self.multiplayer_wrapper:
            self.multiplayer_wrapper.start_game(game_map)
        else:
            self.unbind('<Escape>')
            self.open_game_page(game_map, gm_class)

    def start_multiplayer_countdown(self):
        self.multiplayer_wrapper.countdown_page = self.open_page(lambda: GameStartCountdown(self))

    def open_game_page(self, game_map_json, game_class):
        self.open_page(lambda: GamePage(self, game_map_json, game_class), remember=False, can_return=False).game_start()

    def open_map_selector(self, gm_class):
        btn_list = []
        for num, game_map in enumerate(self.maps):
            with open('./maps/' + game_map) as map_file:
                map_json = json.load(map_file)
                if gm_class.gm_short in map_json["gameModes"]:
                    btn_list.append((map_json['name'], lambda gm=gm_class, g_map=game_map: self.start_game(gm, g_map)))

        self.open_page(lambda: BtnListSubmenu(self, btn_list))

    def open_game_mode_selector(self):
        btn_list = []
        for gm_class in Game.__subclasses__():
            if self.multiplayer_wrapper:
                action = lambda gm=gm_class: self.open_lobby_submenu(self.multiplayer_wrapper.create(gm))
            else:
                action = lambda gm=gm_class: self.open_map_selector(gm)
            btn_list.append((gm_class.gm_name, action))

        self.open_page(lambda: BtnListSubmenu(self, btn_list))

    def open_multiplayer_action_selector(self):
        if os.path.isfile(USERDATA_FILE):
            with open(USERDATA_FILE) as json_file:
                data = json.load(json_file)
            lobby_code = data.get('lobby_code')
            if lobby_code:
                self.open_lobby_submenu(self.multiplayer_wrapper.join(lobby_code))
                return # TODO: rewrite

        btn_list = [
            ('Create a lobby', self.open_game_mode_selector),
            ('Join a lobby', self.open_lobby_selector),
            ('Join a lobby by code', self.open_lobby_code_form),
            ('Change username', self.open_username_form),
            ('Log out', self.log_out)
        ]

        self.open_page(lambda: BtnListSubmenu(self, btn_list))

    def open_lobby_selector(self):
        self.open_page(lambda: BtnListSubmenu(self, self.multiplayer_wrapper.get_lobby_btn_list()))

    def open_lobby_submenu(self, lobby_info):
        self.multiplayer_wrapper.lobby_page = self.open_page(lambda: LobbySubmenu(self, lobby_info))

    def open_lobby_code_form(self):
        self.open_page(lambda: LobbyCodeForm(self))

    def open_username_form(self):
        self.open_page(lambda: UsernameForm(self), remember=False)

    def open_login_page(self):
        self.open_page(lambda: GoogleLoginPage(self), remember=False)

    def log_out(self):
        self.close_submenus()
        GoogleLoginPage.delete_credentials()

    def close_submenus(self):
        if self.page:
            self.page.destroy()
            self.page = None

        self.unbind('<Escape>')
