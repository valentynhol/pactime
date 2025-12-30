import json
import os
import typing
from typing import TYPE_CHECKING

from classes.google_auth_handler import GoogleAuthHandler
from classes.gui.pages.submenu import Submenu
from classes.gui.widgets import Button, Label
from constants import USERDATA_FILE

if TYPE_CHECKING:
    from classes.game_window import GameWindow


class GoogleLoginPage(Submenu):
    def __init__(
            self,
            window: 'GameWindow',
            **kwargs
    ):
        super().__init__(window, **kwargs)

        frame_height = self._frame.winfo_height()
        frame_width = self._frame.winfo_width()

        self._login_btn = Button(
            self.content,
            self.login,
            text='Login via Google',
            fontsize=frame_height//15,
            width=int(0.9*frame_width)
        )
        self._login_btn.pack(side='top', pady=frame_height//60, padx=frame_width//40)

        self._cancel_btn = Button(
            self.content,
            self._on_cancel,
            text='Cancel',
            fontsize=frame_height // 15,
            width=int(0.9 * frame_width)
        )

        self._msg_label = Label(
            self.content,
            fontsize=frame_height//30,
            text="Please, proceed to the opened browser page",
            wraplength=int(0.9*frame_width)
        )

        self._auth_handler: typing.Optional[GoogleAuthHandler] = None
        self._auth_start_time = 0

    def login(self):
        self._login_btn.pack_forget()

        frame_height = self._frame.winfo_height()
        frame_width = self._frame.winfo_width()

        self._msg_label.pack(side='top', pady=frame_height//60, padx=frame_width//40)
        self._cancel_btn.pack(side='top', pady=frame_height // 60, padx=frame_width // 40)

        try:
            self._auth_handler = GoogleAuthHandler()
            self._auth_handler.start()

            self.window.after(0, self._check_login_state)
        except:
            self._login_btn.pack(side='top', pady=frame_height//60, padx=frame_width//40)

    def _on_cancel(self):
        self._auth_handler.cancel()

        self._cancel_btn.pack_forget()
        self._msg_label.pack_forget()

        frame_height = self._frame.winfo_height()
        frame_width = self._frame.winfo_width()

        self._login_btn.pack(side='top', pady=frame_height//60, padx=frame_width//40)

    def _check_login_state(self):
        if self.window.page != self:
            self._auth_handler.cancel()
            return

        if self._auth_handler.is_finished():
            self.save_credentials(self._auth_handler.get_result())
            self.window.multiplayer()
        else:
            self.window.after(100, self._check_login_state)

    @staticmethod
    def save_credentials(jwt):
        json_data = {}
        if os.path.isfile(USERDATA_FILE):
            with open(USERDATA_FILE) as file:
                json_data = json.load(file)

        json_data['auth_token'] = jwt

        with open(USERDATA_FILE, "w") as file:
            file.write(json.dumps(json_data))

    @staticmethod
    def get_credentials():
        if not os.path.isfile(USERDATA_FILE):
            return None

        with open(USERDATA_FILE) as file:
            json_data = json.load(file)

        if not 'auth_token' in json_data.keys():
            return None

        return json_data['auth_token']

    @staticmethod
    def delete_credentials():
        if not os.path.isfile(USERDATA_FILE):
            return

        with open(USERDATA_FILE) as file:
            json_data = json.load(file)

        if not 'auth_token' in json_data.keys():
            return

        json_data.pop('auth_token')

        with open(USERDATA_FILE, "w") as file:
            file.write(json.dumps(json_data))
