from classes.gui.pages.submenu import ScrollableSubmenu
from classes.gui.widgets import Label, Frame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes.game_window import GameWindow

class ScoreboardPage(ScrollableSubmenu):
    def __init__(
            self,
            master: 'GameWindow',
            local_player_id: str,
            players_stats: dict[str, dict],
            players_usernames: dict[str, str],
            **kwargs
    ):
        super().__init__(master, **kwargs)

        fontsize = self._frame.winfo_height() // 30
        stat_headers = list(players_stats.values())[0].keys()

        frame = Frame(self.content)
        frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        Label(frame, fontsize=fontsize, text="PLAYER").pack(fill="both")

        for i, col_header in enumerate(stat_headers, 1):
            frame = Frame(self.content)
            frame.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            Label(frame, fontsize=fontsize, text=col_header.upper()).pack(fill="both")

        Frame(self.content, height=2).grid(row=1, column=0, padx=5, sticky="nsew", columnspan=len(stat_headers) + 1)

        for i, player_id in enumerate(players_stats.keys(), 2):
            if player_id == local_player_id:
                frame = Frame(self.content, bg="purple")
                frame.grid(row=i, column=0, padx=5, pady=5, sticky="nsew")
                Label(frame, fontsize=fontsize, text=players_usernames[player_id], fg="black", bg="purple").pack(fill="both")

                for j, stat in enumerate(stat_headers, 1):
                    frame = Frame(self.content, bg="purple")
                    frame.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                    Label(
                        frame,
                        fontsize=fontsize,
                        fontstyle="normal",
                        text=players_stats[player_id][stat],
                        fg="black",
                        bg="purple"
                    ).pack(fill="both")
            else:
                frame = Frame(self.content)
                frame.grid(row=i, column=0, padx=5, pady=5, sticky="nsew")
                Label(frame, fontsize=fontsize, text=players_usernames[player_id]).pack(fill="both")

                for j, stat in enumerate(stat_headers, 1):
                    frame = Frame(self.content)
                    frame.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                    Label(
                        frame,
                        fontsize=fontsize,
                        fontstyle="normal",
                        text=players_stats[player_id][stat]
                    ).pack(fill="both")

        rows = len(players_stats) + 1
        cols = len(stat_headers) + 1
        for r in range(rows):
            self.content.grid_rowconfigure(r, weight=1)
        for c in range(cols):
            self.content.grid_columnconfigure(c, weight=1)

        self.update()
