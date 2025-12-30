from classes.gui.pages.submenu import ScrollableSubmenu
from classes.gui.widgets import Label, Button, TextBox, Frame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.game_window import GameWindow


class LobbySubmenu(ScrollableSubmenu):
    def __init__(
            self,
            window: 'GameWindow',
            lobby_info: tuple[str, str, bool, str, dict[str, str]],
            **kwargs
    ):
        def leave():
            self.window.multiplayer_wrapper.leave()
            self.window.open_start_screen()

        def delete():
            self.window.multiplayer_wrapper.delete()
            self.window.open_start_screen()

        super().__init__(window, **kwargs)

        lobby_name, lobby_code, is_host, local_player_id, players_usernames = lobby_info
        frame_height = self._frame.winfo_height()
        frame_width = self._frame.winfo_width()

        self._local_player_id = local_player_id
        
        self._lobby_name_label = Label(
            self.content,
            text=lobby_name,
            fontsize=frame_height//15,
            wraplength=int(0.9*frame_width)
        )
        self._lobby_name_label.pack(side='top', pady=frame_height//60, padx=frame_width//40)

        self._code_frame = Frame(self.content, highlightthickness=0)
        self._code_frame.pack(side='top', pady=frame_height//60, padx=frame_width//40)

        self._code_label = Label(self._code_frame, text=f'Lobby code:', fontsize=frame_height//20)
        self._code_label.pack(side='left', padx=frame_width//40)

        self._code = TextBox(self._code_frame, fontsize=frame_height//20, width=int(0.9*frame_width))
        self._code.end_insert(lobby_code)
        self._code.disable()
        self._code.pack(side='right', padx=frame_width//40)

        self._player_list_label = Label(self.content, text='Players:', fontsize=frame_height//20)
        self._player_list_label.pack(side='top', pady=frame_height//120, padx=frame_width//40)

        self._player_list_frame = Frame(self.content)
        self._player_list_frame.pack(side='top', pady=frame_height//120, padx=frame_width//40, fill="x")

        self._player_list_labels: list[Label] = []
        for player_id in players_usernames.keys():
            if player_id == local_player_id:
                label = Label(self._player_list_frame, text=players_usernames[player_id], fontsize=frame_height//30, bg='purple', fg='black')
            else:
                label = Label(self._player_list_frame, text=players_usernames[player_id], fontsize=frame_height//30)
            label.pack(side='top', pady=frame_height//120, padx=frame_width//40)
            self._player_list_labels.append(label)

        if is_host:
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

        if is_host:
            self._delete_lobby_btn = Button(
                self.content,
                delete,
                text='Delete Lobby',
                fontsize=frame_height//15,
                width=int(0.9*frame_width)
            )
            self._delete_lobby_btn.pack(side='top', pady=frame_height//60, padx=frame_width//40)

            self.update()

    def update_player_list(self, players_usernames: dict[str, str]):
        frame_height = self._frame.winfo_height()
        frame_width = self._frame.winfo_width()

        for player in self._player_list_labels:
            player.destroy()

        self._player_list_labels.clear()

        for player_id in players_usernames.keys():
            if player_id == self._local_player_id:
                label = Label(self._player_list_frame, text=players_usernames[player_id], fontsize=frame_height//30,
                              bg='purple', fg='black')
            else:
                label = Label(self._player_list_frame, text=players_usernames[player_id], fontsize=frame_height//30)
            label.pack(side='top', pady=frame_height//120, padx=frame_width//40)
            self._player_list_labels.append(label)

        self.update()

