import copy
import typing

from classes.game import Game
from classes.gui.game_modal import GameModal
from classes.gui.pages.page import Page
from classes.gui.widgets import Frame, Button

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes.game_window import GameWindow


class GamePage(Page):
    def __init__(
            self,
            window: 'GameWindow',
            game_map: dict,
            game_class: type[Game],
            restartable: bool = True,
            quitable: bool = True
    ):
        super().__init__(window)

        self._restartable = restartable
        self._quitable = quitable

        self._game_map_json = game_map
        self._game_class = game_class

        game_map = self._game_map_json["gameMap"]

        self._cell_size: int = int(min(
            (self.window_height * 36/40) / len(game_map),
            (self.window_width * 19/40) / len(game_map[0]),
            self.window_height/40
        ))

        map_width = len(game_map[0])
        map_height = len(game_map)

        self._game_frame = Frame(
            self,
            width=(map_width+0.5)*self._cell_size,
            height=(map_height+0.5)*self._cell_size,
            highlightthickness=0
        )
        self._game_frame.place(x=self.window_width//2, y=self.window_height//2, anchor='center')
        self._game_frame.pack_propagate(False)

        self._top_frame = Frame(
            self,
            height=self.window_height//20,
            width=self.window_width+2,
            highlightthickness=1
        )
        self._top_frame.place(x=-1, y=-1)
        self._top_frame.pack_propagate(False)

        self._bottom_frame = Frame(
            self,
            height=self.window_height//20,
            width=self.window_width+2,
            highlightthickness=1
        )
        self._bottom_frame.place(x=-1, y=self.window_height+1, anchor='sw')
        self._bottom_frame.pack_propagate(False)

        self.update()

        self._game: typing.Optional[Game] = None
        self._modal: typing.Optional[GameModal] = None

    def game_start(self):
        self._close_modal()
        for widget in self._top_frame.winfo_children():
            widget.destroy()
        for widget in self._bottom_frame.winfo_children():
            widget.destroy()

        self._game = self._game_class(self._game_frame, self, self._cell_size, copy.deepcopy(self._game_map_json))

        self._top_frame.update()
        self._game.init_top_bar_content(self._top_frame)
        self._bottom_frame.update()
        self._game.init_bottom_bar_content(self._bottom_frame)

    def pause(self):
        try:
            self._open_modal("Game Paused")
            self._game.init_pause_modal_content(self._modal.content)
        except AttributeError:
            pass

    def win(self):
        try:
            self._open_modal("Game Over", can_continue=False)
            self._game.init_win_modal_content(self._modal.content)
        except AttributeError:
            pass

    def lose(self):
        try:
            self._open_modal("Game Over", can_continue=False)
            self._game.init_lose_modal_content(self._modal.content)
        except AttributeError:
            pass

    def unpause(self):
        self._close_modal()

    def _open_modal(self, title: str, can_continue: bool = True):
        self._modal = GameModal(
            self,
            self.window_width//3,
            self.window_height//3,
            self.window_width//2,
            self.window_height//2,
            title=title
        )

        self._modal.update()

        pady = self._modal.winfo_height()//25

        btn_frame = Frame(self._modal, highlightthickness=0)
        btn_frame.pack(side="top", fill="x", pady=pady)

        width = self._modal.winfo_width()
        fontsize = self._modal.winfo_height()//25

        if can_continue:
            Button(btn_frame, text="Continue", action=self._game.continue_game, width=width, fontsize=fontsize).pack()
        if self._restartable:
            Button(btn_frame, text="Restart", action=self._restart, width=width, fontsize=fontsize).pack()
        if self._quitable:
            Button(btn_frame, text="Quit to main menu", action=self._quit, width=width, fontsize=fontsize).pack()

        self._modal.update()

    def _close_modal(self):
        if self._modal:
            self._modal.destroy()
            self._modal = None

    def _restart(self):
        if self._game:
            self._game.cleanup()
            del self._game
        self.game_start()

    def _quit(self):
        self.window.open_start_screen()

    def destroy(self):
        self._game.cleanup()
        super().destroy()