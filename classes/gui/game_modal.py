from typing import Literal

from classes.gui.widgets import Frame, Label

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes.gui.pages.game_page import GamePage


class GameModal(Frame):
    def __init__(
            self,
            master: 'GamePage',
            width: int,
            height: int,
            x: int,
            y: int,
            anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"]="center",
            title: str="Modal",
            **kwargs
    ):
        kwargs.setdefault("width", width)
        kwargs.setdefault("height", height)
        super().__init__(master, **kwargs)
        self.place(x=x, y=y, anchor=anchor)
        self.pack_propagate(False)
        self.update()

        self._title_label = Label(self, text=title, fontsize=self.winfo_height()//15, fg='white')
        self._title_label.pack(side="top")

        self.content = Frame(self, highlightthickness=0)
        self.content.pack(side="top", fill="both", expand=True)

        self.update()
