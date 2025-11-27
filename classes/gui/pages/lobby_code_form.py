from classes.gui.pages.submenu import Submenu
from classes.gui.widgets import Label, Button, Entry

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.game_window import GameWindow


class LobbyCodeForm(Submenu):
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
            text='Lobby code:',
            fontsize=frame_height//15
        )
        self._entry_label.pack(side='top', pady=frame_height//60, padx=frame_width//40)

        self._code_entry = Entry(
            self.content,
            fontsize=frame_height//15,
            width=int(0.9*frame_width)
        )
        self._code_entry.focus_force()
        self._code_entry.pack(side='top', pady=frame_height//60, padx=frame_width//40)

        self._confirm_btn = Button(
            self.content,
            self._confirm_code,
            text='Confirm',
            fontsize=frame_height//15,
            width=int(0.9*frame_width)
        )
        self._confirm_btn.pack(side='top', pady=frame_height//60, padx=frame_width//40)

    def _confirm_code(self):
        lobby_code = self._code_entry.get()

        if lobby_code:
            self.window.open_lobby_submenu(self.window.multiplayer_wrapper.join(lobby_code))