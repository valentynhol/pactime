from classes.gui.widgets import Frame, ScrollFrame
from classes.gui.pages.page import Page

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.game_window import GameWindow


class Submenu(Page):
    def __init__(
            self,
            window: 'GameWindow',
            **kwargs
    ):
        super().__init__(window, **kwargs)

        frame = Frame(
            self,
            height=int(0.8 * self.window_height),
            width=int(0.9 * self.window_width)
        )
        frame.pack_propagate(False)
        frame.place(x=int(0.5 * self.window_width), y=int(0.5 * self.window_height), anchor='center')

        self.update()

        self._frame = frame
        self.content = frame


class ScrollableSubmenu(Submenu):
    def __init__(
            self,
            window: 'GameWindow',
            **kwargs
    ):
        super().__init__(window, **kwargs)

        self.content = ScrollFrame(self._frame)
