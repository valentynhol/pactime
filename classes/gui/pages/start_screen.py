from typing import List, TYPE_CHECKING

from classes.gui.widgets import Button
from classes.gui.menu_animation import MenuAnimation
from classes.gui.pages.page import Page

if TYPE_CHECKING:
    from classes.game_window import GameWindow


class StartScreen(Page):
    def __init__(
            self,
            window: 'GameWindow',
            **kwargs
    ):
        super().__init__(window, **kwargs)

        self.animation: MenuAnimation = MenuAnimation(
            self,
            self.window_width//2,
            self.window_height//10,
            self.window_height//9
        )

        self.menu_btns: List[Button] = []

        self.menu_btns.append(Button(
            self,
            self.window.singleplayer,
            text='Singleplayer',
            fontsize=self.window_height//30,
            width=15
        ))
        self.menu_btns.append(Button(
            self,
            self.window.multiplayer,
            text='Multiplayer',
            fontsize=self.window_height//30,
            width=15
        ))
        self.menu_btns.append(Button(
            self,
            self.window.options,
            text='Options',
            fontsize=self.window_height//30,
            width=15
        ))
        self.menu_btns.append(Button(
            self,
            self.window.quit,
            text='Quit',
            fontsize=self.window_height//30,
            width=15
        ))

        self.menu_btns[0].place(x=0.5*self.window_width, y=15/30*self.window_height, anchor='center')
        self.menu_btns[1].place(x=0.5*self.window_width, y=19/30*self.window_height, anchor='center')
        self.menu_btns[2].place(x=0.5*self.window_width, y=23/30*self.window_height, anchor='center')
        self.menu_btns[3].place(x=0.5*self.window_width, y=27/30*self.window_height, anchor='center')
