from classes.gui.pages.page import Page
from classes.gui.widgets import Label

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.game_window import GameWindow


class GameStartCountdown(Page):
    def __init__(
            self,
            window: 'GameWindow',
            **kwargs
    ):
        Page.__init__(self, window, **kwargs)

        frame_height = self.winfo_height()
        frame_width = self.winfo_width()

        self._cd_label = Label(
            self,
            text="Game starts in: ",
            fontsize=frame_height//15
        )

        self._cd_label.place(x=frame_width//2, y=frame_height//2, anchor='center')

    def update_cd(self, num):
        self._cd_label.config(text=f"Game starts in: {num}")