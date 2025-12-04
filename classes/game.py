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

    # noinspection PyTypeChecker
    def __init__(self, frame: Frame, game_page: 'GamePage', cell_size: int, game_map_json: dict):
        self._game_page = game_page
        self._game_map = game_map_json["gameMap"]
        self._cell_size = cell_size
        self._dot_num = 0
        self._pac: Pac
        self.process = "game"

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
        self._canvas.destroy()

    def on_win(self):
        self.process = 'game_ended'
        self._game_page.win()

    def on_lose(self):
        self.process = 'game_ended'
        self._game_page.lose()

    def pause(self):
        self.process = 'menu'
        self._game_page.pause()

    def continue_game(self):
        if self.process == 'menu':
            self._game_page.close_modal()
            self.process = 'game'

    def remove_dot(self, x: int, y: int):
        self._canvas.delete(self._game_map[int(y)][int(x)])
        self._game_map[int(y)][int(x)] = ' '
        self._dot_num -= 1

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


class MiniView:
    pac_id = None
    game_state = None
    gs_label = None

    def __init__(self, parent_frame, game_map):
        self.parent_frame = parent_frame
        self.map_width = len(game_map["gameMap"][0])
        self.map_height = len(game_map["gameMap"])

        parent_frame.update_idletasks()
        frame_width = parent_frame.winfo_width()
        frame_height = parent_frame.winfo_height()

        self.cell_size = min(frame_width / self.map_width, frame_height / self.map_height)

        self.x_offset = (frame_width - self.map_width * self.cell_size) / 2
        self.y_offset = (frame_height - self.map_height * self.cell_size) / 2

        self.canvas = tk.Canvas(parent_frame, width=frame_width, height=frame_height, background='black',
                                highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)

        self.pac_state = None
        self.dot_positions = set()
        self.dot_ids = {}
        self.wall_ids = set()

        self._build_from_map(game_map["gameMap"])

    @staticmethod
    def init_mini_views(game):
        outer_frames = [
            tk.Frame(game.field, background='black'),
            tk.Frame(game.field, background='black'),
            tk.Frame(game.field, background='black'),
            tk.Frame(game.field, background='black'),
        ]
        outer_frames[0].place(x=0, y=int(3 / 40 * game.window_height), anchor='nw',
                              height=int(35 / 80 * game.window_height), width=int(0.25 * game.window_width))
        outer_frames[1].place(x=game.window_width, y=int(3 / 40 * game.window_height), anchor='ne',
                              height=int(35 / 80 * game.window_height), width=int(0.25 * game.window_width))
        outer_frames[2].place(x=0, y=int(41 / 80 * game.window_height), anchor='nw',
                              height=int(35 / 80 * game.window_height), width=int(0.25 * game.window_width))
        outer_frames[3].place(x=game.window_width, y=int(41 / 80 * game.window_height), anchor='ne',
                              height=int(35 / 80 * game.window_height), width=int(0.25 * game.window_width))

        game.window.update()
        print(outer_frames[0].winfo_width())
        playername_labels = [
            tk.Label(outer_frames[0], text="Player 1", font=('Arial', int(game.window_height / 60), 'bold'),
                     fg='purple', bg='black'),
            tk.Label(outer_frames[1], text="Player 2", font=('Arial', int(game.window_height / 60), 'bold'),
                     fg='purple', bg='black'),
            tk.Label(outer_frames[2], text="Player 3", font=('Arial', int(game.window_height / 60), 'bold'),
                     fg='purple', bg='black'),
            tk.Label(outer_frames[3], text="Player 4", font=('Arial', int(game.window_height / 60), 'bold'),
                     fg='purple', bg='black')
        ]
        frames = [
            tk.Frame(outer_frames[0], bg='black'),
            tk.Frame(outer_frames[1], bg='black'),
            tk.Frame(outer_frames[2], bg='black'),
            tk.Frame(outer_frames[3], bg='black')
        ]

        playername_labels[0].pack(side='top')
        playername_labels[1].pack(side='top')
        playername_labels[2].pack(side='top')
        playername_labels[3].pack(side='top')
        frames[0].pack(side='top', fill='both', expand=True)
        frames[1].pack(side='top', fill='both', expand=True)
        frames[2].pack(side='top', fill='both', expand=True)
        frames[3].pack(side='top', fill='both', expand=True)

        game.window.update()
        print(outer_frames[0].winfo_width())

        mini_views = [
            (outer_frames[0], playername_labels[0], frames[0]),
            (outer_frames[1], playername_labels[1], frames[1]),
            (outer_frames[2], playername_labels[2], frames[2]),
            (outer_frames[3], playername_labels[3], frames[3])
        ]

        return mini_views

    @staticmethod
    def get_state(game):
        pac_state = {"pos": (game.pac.x, game.pac.y), "direction": game.pac.direction} if game.pac else None

        current_dots = set()
        for row_num, row in enumerate(game.game_map):
            for col_num, cell in enumerate(row):
                if isinstance(cell, int):
                    if "Dot" in game.field.gettags(cell):
                        current_dots.add((col_num, row_num))

        eaten_dots = set()
        if hasattr(game, "_last_dot_positions"):
            eaten_dots = game._last_dot_positions - current_dots

        game._last_dot_positions = current_dots.copy()

        return {
            "pac_state": pac_state,
            "eaten_dots": list(eaten_dots),
            "game_state": game.process,
        }

    def apply_state(self, state):
        new_game_state = state.get("game_state")
        if new_game_state != self.game_state:
            self.game_state = new_game_state
            if new_game_state == "game":
                self._remove_game_state_label()
            else:
                self._create_game_state_label()

        new_pac = state.get("pac_state")
        if new_pac != self.pac_state:
            pac_pos = new_pac["pos"]
            pac_dir = new_pac["direction"]
            if hasattr(self, 'pac_id') and self.pac_id:
                self.canvas.delete(self.pac_id)
            if new_pac:
                x, y = pac_pos
                px = self.x_offset + x * self.cell_size
                py = self.y_offset + y * self.cell_size
                arc_size = 270
                self.pac_id = self.canvas.create_arc(px, py, px + self.cell_size, py + self.cell_size,
                                                     fill='yellow', start = pac_dir - arc_size / 2, extent = arc_size)
            self.pac_state = new_pac

        for dot in state.get("eaten_dots", []):
            dot = tuple(dot)
            if dot in self.dot_ids:
                self.canvas.delete(self.dot_ids[dot])
                del self.dot_ids[dot]

    def _build_from_map(self, game_map):
        self.canvas.delete("all")
        self.dot_positions.clear()
        self.dot_ids.clear()
        self.wall_ids.clear()

        for y, row in enumerate(game_map):
            for x, cell in enumerate(row):
                px = self.x_offset + x * self.cell_size
                py = self.y_offset + y * self.cell_size

                if cell == '#':
                    self.wall_ids.add(
                        self.canvas.create_rectangle(px, py,
                                                     px + self.cell_size, py + self.cell_size,
                                                     fill='purple')
                    )
                elif cell == '.':
                    dot_id = self.canvas.create_rectangle(px + 0.4 * self.cell_size, py + 0.4 * self.cell_size,
                                                          px + 0.6 * self.cell_size, py + 0.6 * self.cell_size,
                                                          fill='white')
                    self.dot_positions.add((x, y))
                    self.dot_ids[(x, y)] = dot_id

    def _create_game_state_label(self):
        if self.game_state == "menu":
            label_text = "Paused"
        elif self.game_state == "game_ended":
            label_text = "Game Ended"
        else:
            return

        self.gs_label = tk.Label(self.canvas, text=label_text, font=('Arial', int(self.canvas.winfo_height() / 25), 'bold'),
                                 background="black", foreground="purple", highlightthickness=5,
                                 highlightbackground="purple")
        self.gs_label.place(x=int(self.canvas.winfo_width() / 2), y=int(self.canvas.winfo_height() / 2),
                            anchor='center')

    def _remove_game_state_label(self):
        if self.gs_label:
            self.gs_label.destroy()

