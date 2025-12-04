from typing import Tuple, List

from classes.gui.pages.submenu import ScrollableSubmenu
from classes.gui.widgets import Label, Button, TextBox, Frame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.game_window import GameWindow


class LobbySubmenu(ScrollableSubmenu):
    def __init__(
            self,
            window: 'GameWindow',
            lobby_info: List[Tuple[str, str, List[str]]],
            **kwargs
    ):
        super().__init__(window, **kwargs)
        def leave():
            self.window.multiplayer_wrapper.leave()
            self.window.close_submenus()

        def delete():
            self.window.multiplayer_wrapper.delete()
            self.window.close_submenus()

        lobby_name, lobby_code, player_list = lobby_info
        frame_height = self._frame.winfo_height()
        frame_width = self._frame.winfo_width()
        
        self._lobby_name_label = Label(
            self.content,
            text=lobby_name,
            fontsize=frame_height//15
        )
        self._lobby_name_label.pack(side='top', pady=frame_height//60, padx=frame_width//40)

        self._code_label = Label(self.content, text=f'Lobby code:', fontsize=frame_height//15)
        self._code_label.pack(side='top', pady=frame_height//60, padx=frame_width//40)

        self._code = TextBox(self.content, fontsize=frame_height//15, width=int(0.9*frame_width))
        self._code.end_insert(lobby_code)
        self._code.disable()
        self._code.pack(side='top', pady=frame_height//60, padx=frame_width//40)

        self._player_list_label = Label(self.content, text='Players:', fontsize=frame_height//15)
        self._player_list_label.pack(side='top', pady=frame_height//120, padx=frame_width//40)

        self._player_list_frame = Frame(self.content)
        self._player_list_frame.pack(side='top', pady=frame_height//120, padx=frame_width//40)

        self._player_list: List[Label] = []
        for player in player_list:
            label = Label(self._player_list_frame, text=player, fontsize=frame_height//30)
            label.pack(side='top', pady=frame_height//120, padx=frame_width//40)
            self._player_list.append(label)

        self._start_game_btn = Button(
            self.content,
            lambda: self.window.open_map_selector(self.window.multiplayer_wrapper.gm_class),
            text='Start Game',
            fontsize=frame_height//15,
            width=int(0.9*frame_width)
        )
        self._start_game_btn.pack(side='top', pady=frame_height//60, padx=frame_width//40)

        self._leave_lobby_btn = Button(
            self.content,
            leave,
            text='Leave Lobby',
            fontsize=frame_height//15,
            width=int(0.9*frame_width)
        )
        self._leave_lobby_btn.pack(side='top', pady=frame_height//60, padx=frame_width//40)

        self._delete_lobby_btn = Button(
            self.content,
            delete,
            text='Delete Lobby',
            fontsize=frame_height//15,
            width=int(0.9*frame_width)
        )
        self._delete_lobby_btn.pack(side='top', pady=frame_height//60, padx=frame_width//40)

        self.update()

    def update_player_list(self, player_list):
        frame_height = self._frame.winfo_height()
        frame_width = self._frame.winfo_width()

        for player in self._player_list:
            player.destroy()

        self._player_list.clear()

        for player in player_list:
            label = Label(self._player_list_frame, text=player, fontsize=frame_height//30)
            label.pack(side='top', pady=frame_height//120, padx=frame_width//40)
            self._player_list.append(label)

        self.update()

