from classes.game import Game
from classes.gui.game_mini_view import MiniView
from classes.gui.pages.game_page import GamePage

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes.game_window import GameWindow

class MultiplayerGamePage(GamePage):
    def __init__(
            self,
            window: 'GameWindow',
            game_map: dict,
            game_class: type[Game],
            player_list: list
    ):
        super().__init__(window, game_map, game_class, False, False)
        self.update()

        height = self.winfo_height()
        width = self.winfo_width()

        mv_height = int(30 / 80 * height)
        mv_width = int(0.25 * width)

        player_count = len(player_list)

        self._mini_views: dict[str, MiniView] = {}
        if player_count >= 1:
            self._mini_views[player_list[0]] = MiniView(
                self,
                game_map,
                player_list[0],
                x=0,
                y=int(3 / 40 * height),
                height=mv_height,
                width=mv_width
            )
        if player_count >= 2:
            self._mini_views[player_list[1]] = MiniView(
                self,
                game_map,
                player_list[1],
                x=width,
                y=int(3 / 40 * height),
                anchor="ne",
                height=mv_height,
                width=mv_width
            )
        if player_count >= 3:
            self._mini_views[player_list[2]] = MiniView(
                self,
                game_map,
                player_list[2],
                x=0,
                y=int(41 / 80 * height),
                height=mv_height,
                width=mv_width
            )
        if player_count >= 4:
            self._mini_views[player_list[3]] = MiniView(
                self,
                game_map,
                player_list[3],
                x=width,
                y=int(41 / 80 * height),
                anchor="ne",
                height=mv_height,
                width=mv_width
            )

    def update_mini_view(self, player: str, state: dict):
        self._mini_views[player].apply_state(state)

    @property
    def state(self):
        return self._game.get_state()

    @property
    def stats(self):
        return self._game.get_stats()

    @property
    def is_game_over(self) -> bool:
        return self._game.process == "game_ended"
