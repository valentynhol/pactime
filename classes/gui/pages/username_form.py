from classes.gui.pages.submenu import Submenu
from classes.gui.widgets import Label, Button, Entry

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.game_window import GameWindow


class UsernameForm(Submenu):
    def __init__(
            self,
            window: 'GameWindow',
            **kwargs
    ):
        super().__init__(window, **kwargs)

        frame_height = self._frame.winfo_height()
        frame_width = self._frame.winfo_width()

        self._entry_label = Label(
            self.content,
            text='Your username:',
            fontsize=frame_height//15
        )
        self._entry_label.pack(side='top', pady=frame_height//60, padx=frame_width//40)

        self._username_entry = Entry(
            self.content,
            fontsize=frame_height//15,
            width=int(0.9*frame_width)
        )
        curr_username = self.window.multiplayer_wrapper.get_username()
        if curr_username:
            self._username_entry.insert(0, curr_username)
        self._username_entry.focus_force()
        self._username_entry.pack(side='top', pady=frame_height//60, padx=frame_width//40)

        self._confirm_btn = Button(
            self.content,
            self._confirm_username,
            text='Confirm',
            fontsize=frame_height//15,
            width=int(0.9*frame_width)
        )
        self._confirm_btn.pack(side='top', pady=frame_height//60, padx=frame_width//40)

    def _confirm_username(self):
        username = self._username_entry.get()

        if username:
            self.window.multiplayer_wrapper.update_username(username)
            self.window.open_multiplayer_action_selector()
