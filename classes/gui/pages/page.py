import tkinter as tk

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.game_window import GameWindow


class Page(tk.Frame):
    def __init__(
            self,
            window: 'GameWindow',
            **kwargs
    ):
        self.window = window
        self.window_height: int = window.winfo_height()
        self.window_width: int = window.winfo_width()

        kwargs.setdefault('background', 'black')
        super().__init__(window, **kwargs)

        self.pack(fill='both', expand=True)
        self.update()
