from typing import Callable, Tuple, List, TYPE_CHECKING

from classes.gui.widgets import Button
from classes.gui.pages.submenu import ScrollableSubmenu, Submenu

if TYPE_CHECKING:
    from classes.game_window import GameWindow


class BtnListSubmenu(ScrollableSubmenu):
    def __init__(
            self,
            window: 'GameWindow',
            btn_list: List[Tuple[str, Callable]],
            button_fontsize: int = None,
            **kwargs
    ):
        super().__init__(window, **kwargs)

        frame_height = self._frame.winfo_height()
        frame_width = self._frame.winfo_width()

        if not button_fontsize:
            button_fontsize = frame_height//15

        self.selector_btns: List[Button] = []
        for btn_text, btn_action in btn_list:
            btn = Button(self.content, btn_action, text=btn_text, fontsize=button_fontsize, width=int(0.9*frame_width))
            btn.pack(side='top', pady=frame_height//60, padx=frame_width//40)
            self.selector_btns.append(btn)

        self.update()