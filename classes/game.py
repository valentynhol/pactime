import tkinter as tk
import typing
import random
import time

from classes.character_entities import Pac, Ghost
from classes.exceptions import MapGenerationError
from classes.gui.widgets import Frame, Label

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.gui.pages.game_page import GamePage


class Game:
    gm_name = "Default"
    gm_short = "def"

    def __init__(self, frame: Frame, game_page: 'GamePage', cell_size: int, game_map_json: dict):
        self._game_page = game_page
        self._game_map = game_map_json["gameMap"]
        self._cell_size = cell_size
        self._dot_num = 0
        self._pac: Pac
        self._last_dot_positions: typing.Optional[set[tuple[int, int]]] = None
        self.process = "game"
        self._won = False

        self._canvas = tk.Canvas(frame, bg='black', highlightthickness=0)
        self._canvas.pack(fill="both", expand=True)

        for row_num, row in enumerate(self._game_map):
            for cell_num, cell in enumerate(row):
                x = cell_num*cell_size + 0.25*cell_size
                y = row_num*cell_size + 0.25*cell_size

                if self._game_map[row_num][cell_num] == '#':
                    self._canvas.create_rectangle(
                        (x, y),
                        (x + cell_size, y + cell_size),
                        fill="purple",
                        tags="Wall"
                    )
                elif self._game_map[row_num][cell_num] == '.':
                    self._game_map[row_num][cell_num] = self._canvas.create_rectangle(
                        (x + 0.41*cell_size, y + 0.41*cell_size),
                        (x + 0.59*cell_size, y + 0.59*cell_size),
                        fill="white",
                        tags="Dot"
                    )
                    self._dot_num += 1
                elif self._game_map[row_num][cell_num] == 'p':
                    self.pac = Pac(self, self._canvas, self._game_map, self._cell_size, cell_num, row_num)
                elif self._game_map[row_num][cell_num] == ' ':
                    pass
                else:
                    if not self._more_game_objects(row_num, cell_num):
                        raise MapGenerationError(
                            f"Unknown character found in the map matrix: '{self._game_map[row_num][cell_num]}'. "
                            f"If you are the creator of this map, replace the character on position "
                            f"{[row_num, cell_num]} with valid one."
                        )

        if not self.pac:
            raise MapGenerationError(
                "Map has no pacman location specified. If you are the creator of this map, you should set 'p' in the "
                "matrix of the map to set the pacman's start location."
            )

        self._canvas.tag_raise("CharacterEntity", "Dot")

        self._canvas.bind_all('<KeyRelease>', self._process_change)

        # noinspection PyTypeChecker
        self._canvas.after(30, self._game_cycle)

    def cleanup(self):
        self._canvas.unbind_all('<KeyPress>')
        self._canvas.unbind_all('<KeyRelease>')
        self._canvas.destroy()

    def on_win(self):
        self.process = 'game_ended'
        self._won = True
        self._game_page.win()

    def on_lose(self):
        self.process = 'game_ended'
        self._won = False
        self._game_page.lose()

    def pause(self):
        self.process = 'menu'
        self._game_page.pause()

    def continue_game(self):
        if self.process == 'menu':
            self._game_page.unpause()
            self.process = 'game'

    def remove_dot(self, x: int, y: int):
        self._canvas.delete(self._game_map[int(y)][int(x)])
        self._game_map[int(y)][int(x)] = ' '
        self._dot_num -= 1

    def get_state(self):
        pac_state = {"pos": (self.pac.x, self.pac.y), "direction": self.pac.direction} if self.pac else None

        current_dots = set()
        for row_num, row in enumerate(self._game_map):
            for col_num, cell in enumerate(row):
                if isinstance(cell, int):
                    if "Dot" in self._canvas.gettags(cell):
                        current_dots.add((col_num, row_num))

        eaten_dots = set()
        if self._last_dot_positions:
            eaten_dots = self._last_dot_positions - current_dots

        self._last_dot_positions = current_dots.copy()

        return {
            "pac_state": pac_state,
            "eaten_dots": list(eaten_dots),
            "game_state": self.process,
        }

    def get_stats(self) -> dict:
        return {
            "won": self._won
        }

    def _game_cycle(self):
        if self.process == 'game':
            self.pac.move()
            self._game_rules()

        # noinspection PyTypeChecker
        self._canvas.after(30, self._game_cycle)

    def _process_change(self, event):
        if self._canvas:
            key = event.keysym
            if self.process == 'game':
                if key == 'Escape':
                    self.pause()
            elif self.process == 'menu':
                if key == 'Escape':
                    self.continue_game()
            elif self.process == 'game_ended':
                if key == 'Return':
                    self.cleanup()
                    self._game_page.game_start()

    """
    Extension methods
    """
    def _game_rules(self):
        pass

    def _more_game_objects(self, row_num, cell_num):
        pass

    def init_win_modal_content(self, frame: Frame):
        pass

    def init_lose_modal_content(self, frame: Frame):
        pass

    def init_pause_modal_content(self, frame: Frame):
        pass

    def init_top_bar_content(self, frame: Frame):
        pass

    # noinspection PyMethodMayBeStatic
    def init_bottom_bar_content(self, frame: Frame):
        Label(
            frame,
            text='Menu -- "Esc"',
            fontsize=frame.winfo_height()//4,
            fg='white'
        ).pack(side="top", fill="both")


class ClassicGameMode(Game):
    gm_name = "Classic"
    gm_short = "cl"

    def __init__(self, frame: Frame, game_page: 'GamePage', cell_size: int, game_map_json: dict):
        self.score = 0
        self.ghosts = []
        self._score_label: typing.Optional[Label] = None
        super().__init__(frame, game_page, cell_size, game_map_json)

    def get_stats(self):
        stats = super().get_stats()
        stats["score"] = self.score
        return stats

    def _game_cycle(self):
        if self.process == 'game':
            self.pac.move()
            for ghost in self.ghosts:
                ghost.move()
            self._game_rules()

        # noinspection PyTypeChecker
        self._canvas.after(30, self._game_cycle)

    def _game_rules(self):
        if 0 == self._dot_num:
            self.on_win()

    def _more_game_objects(self, row_num, cell_num):
        if super()._more_game_objects(row_num, cell_num):
            return True
        elif self._game_map[row_num][cell_num] == 'g':
            self.ghosts.append(Ghost(
                self,
                self._canvas,
                self._game_map,
                self._cell_size,
                cell_num,
                row_num,
                random.choice(["red", "blue", "orange", "pink", "cyan", "gray", "brown"])
            ))
            return True
        return False

    def init_win_modal_content(self, frame: Frame):
        Label(
            frame,
            text="You win!",
            fg='white',
            fontsize=frame.winfo_height()//15
        ).pack(side='top', fill="x")

        Label(
            frame,
            text=f"Your score: {self.score}",
            fg='white',
            fontsize=frame.winfo_height()//15
        ).pack(side='top', fill="x")

    def init_lose_modal_content(self, frame: Frame):
        Label(
            frame,
            text="You've died!",
            fg='white',
            fontsize=frame.winfo_height()//15
        ).pack(side='top', fill="x")

        Label(
            frame,
            text=f"Your score: {self.score}",
            fg='white',
            fontsize=frame.winfo_height()//15
        ).pack(side='top', fill="x")

    def init_top_bar_content(self, frame: Frame):
        self._score_label = Label(
            frame,
            text="Score: 0",
            fg='white',
            fontsize=frame.winfo_height()//4
        )
        self._score_label.pack(side='left', padx=frame.winfo_width()//100)

    def add_score(self, score: int):
        self.score += score
        self._score_label.config(text=f"Score: {str(self.score)}")


class TimeRaceGameMode(Game):
    gm_name = "Time race"
    gm_short = "tr"

    def __init__(self, frame: Frame, game_page: 'GamePage', cell_size: int, game_map_json: dict):
        self.score = 0
        self.max_game_duration = game_map_json["maxGameDuration"]

        self._pause_start_time = 0
        self._pause_duration = 0

        self._time_label: typing.Optional[Label] = None
        self._score_label: typing.Optional[Label] = None
        super().__init__(frame, game_page, cell_size, game_map_json)

        self._game_start_time = time.time()

    def pause(self):
        self._pause_start_time = time.time()
        super().pause()

    def continue_game(self):
        super().continue_game()
        self._pause_duration += time.time() - self._pause_start_time
        self._pause_start_time = 0

    def get_stats(self):
        stats = super().get_stats()
        stats["score"] = self.score
        game_time = min(self.max_game_duration, time.time() - self._game_start_time - self._pause_duration)
        stats["time"] = f"{game_time // 60}:{game_time % 60}"
        return stats

    def _game_rules(self):
        game_time = self.max_game_duration - (time.time() - self._game_start_time - self._pause_duration)

        if game_time < 0:
            self.pac.die()
        elif 0 == self._dot_num:
            self.score += round(game_time * 1000)
            self.on_win()
        else:
            time_m = game_time // 60
            time_s = game_time % 60

            if self.process == 'game':
                self._time_label.config(text=f"Time left: {str(int(time_m))}:{str(round(time_s, 1))}")

    def init_win_modal_content(self, frame: Frame):
        Label(
            frame,
            text="You win!",
            fg='white',
            fontsize=frame.winfo_height() // 15
        ).pack(side='top', fill="x")

        Label(
            frame,
            text=f"Your score: {self.score}",
            fg='white',
            fontsize=frame.winfo_height() // 15
        ).pack(side='top', fill="x")

    def init_lose_modal_content(self, frame: Frame):
        Label(
            frame,
            text="Time's up!",
            fg='white',
            fontsize=frame.winfo_height() // 15
        ).pack(side='top', fill="x")

        Label(
            frame,
            text=f"Your score: {self.score}",
            fg='white',
            fontsize=frame.winfo_height() // 15
        ).pack(side='top', fill="x")

    def init_top_bar_content(self, frame: Frame):
        self._score_label = Label(
            frame,
            text="Score: 0",
            fg='white',
            fontsize=frame.winfo_height()//4
        )
        self._score_label.pack(side='left', padx=frame.winfo_width()//100)

        self._time_label = Label(
            frame,
            text=f"Time left: {str(self.max_game_duration//60)}:{str(float(self.max_game_duration%60))}",
            fg='white',
            fontsize=frame.winfo_height()//4
        )
        self._time_label.pack(side='right', padx=frame.winfo_width() // 100)

    def add_score(self, score: int):
        self.score += score
        self._score_label.config(text=f"Score: {str(self.score)}")


class ObstacleCourseGameMode(Game):
    gm_name = "Obstacle course"
    gm_short = "oc"
