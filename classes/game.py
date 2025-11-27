import copy
import tkinter as tk

from classes.character_entities import *
from classes.exceptions import MapGenerationError


class Game:
    gm_name = "Default"
    gm_short = "def"

    field = None
    game_map = None
    pac = None

    window_height = 0
    window_width = 0
    map_width = 0
    map_height = 0
    offset_x = 0
    offset_y = 0
    cell_size = 0

    process = 'game'
    dot_num = 0

    _map_local_copy = None

    _modal = []

    def __init__(self, window, game_map):
        self.window = window

        self._reset_properties()

        self._map_local_copy = game_map["gameMap"]
        self.game_map = copy.deepcopy(self._map_local_copy)

    def start(self):
        self.game_window_init()

        try:
            while self.window:
                self.game_window_update()
        except tk.TclError:
            pass

    def game_window_init(self):
        self._map_init()
        self._gui_init()

        self.field.bind_all('<KeyPress>', self.pac.turn)
        self.field.bind_all('<KeyRelease>', self._process_change)

    def game_window_update(self):
        self.window.update_idletasks()
        self._game_cycle()
        self.window.update()

    def restart_game(self):
        self.field.delete('all')
        self.pac = None
        self.game_map = None

        self._reset_properties()

        self.game_map = copy.deepcopy(self._map_local_copy)
        self._map_init()
        self._gui_init()

        self.field.bind_all('<KeyPress>', self.pac.turn)
        self.field.bind_all('<KeyRelease>', self._process_change)

    def close_game(self):
        self.field.destroy()
        self.window.update_idletasks()
        self.field = None

    def won_game(self):
        self._show_modal()
        self._modal.append(self.field.create_text(0.5 * self.window_width, 0.455 * self.window_height,
                                                  text='You won!', fill='white',
                                                  font=('ArialBold', int(0.01 * self.window_height))))
        self._modal.append(self.field.create_text(0.5 * self.window_width, 0.485 * self.window_height,
                                                  text='Your score: ' + str(self.score), fill='white',
                                                  font=('ArialBold', int(0.008 * self.window_height))))
        self._modal.append(self.field.create_text(0.5 * self.window_width, 0.55 * self.window_height,
                                                  text='Press "Enter" tо restart game', fill='white',
                                                  font=('Arial', int(0.005 * self.window_height))))
        self.process = 'game_ended'

    def lost_game(self):
        self._show_modal()
        self._modal.append(self.field.create_text(0.5 * self.window_width, 0.475 * self.window_height,
                                                  text="Game over", fill='white',
                                                  font=('ArialBold', int(0.01 * self.window_height))))
        self._modal.append(self.field.create_text(0.5 * self.window_width, 0.55 * self.window_height,
                                                  text='Press "Enter" tо restart game', fill='white',
                                                  font=('Arial', int(0.005 * self.window_height))))
        self.process = 'game_ended'

    def _reset_properties(self):
        self.process = 'game'

    def _open_menu(self):
        self._show_modal()

        self._modal.append(self.field.create_text(0.5 * self.window_width, 0.455 * self.window_height,
                                                  text='Menu', fill='white', font=('ArialBold', 18)))
        self._modal.append(self.field.create_text(0.5 * self.window_width, 0.53 * self.window_height,
                                                  text='Press "Esc" to continue game', fill='white',
                                                  font=('Arial', int(0.005 * self.window_height))))
        self._modal.append(self.field.create_text(0.5 * self.window_width, 0.55 * self.window_height,
                                                  text='Press "Enter" tо restart game', fill='white',
                                                  font=('Arial', int(0.005 * self.window_height))))

        self.process = 'menu'

    def _close_menu(self):
        if self.field:
            self._hide_modal()

            self.process = 'game'

    def _show_modal(self):
        self._modal.append(self.field.create_rectangle((0.35 * self.window_width, 0.4 * self.window_height),
                                                       (0.65 * self.window_width, 0.6 * self.window_height),
                                                       fill='black', outline='purple'))

    def _hide_modal(self):
        for element in self._modal:
            self.field.delete(element)

        self._modal = []

    def _game_cycle(self):
        try:
            time.sleep(0.03)
            if self.process == 'game':
                self.pac.move()

                self._game_rules()
        except KeyboardInterrupt:
            exit()

    def _game_rules(self):
        pass

    def _process_change(self, event):
        if self.field:
            key = event.keysym
            if self.process == 'game':
                if key == 'Escape':
                    self._open_menu()
            elif self.process == 'menu':
                if key == 'Return':
                    self.restart_game()
                if key == 'Escape':
                    self._close_menu()
                if key == 'BackSpace':
                    self.close_game()
                    del self
            elif self.process == 'game_ended':
                if key == 'Return':
                    self.restart_game()

    def _map_init(self):
        self.window_height = self.window.window_height
        self.window_width = self.window.window_width

        self.cell_size = min((self.window_height * 36 / 40) // len(self.game_map),
                             (self.window_width * 19 / 40) // len(self.game_map[0]), 40)

        self.map_width = len(self.game_map[0]) * self.cell_size + 0.5 * self.cell_size
        self.map_height = len(self.game_map) * self.cell_size + 0.5 * self.cell_size

        self.offset_x = 0.5 * (self.window_width - self.map_width)
        self.offset_y = 0.5 * (1.025 * self.window_height - self.map_height)

        self.field = tk.Canvas(self.window, width=self.window_width, height=self.window_height, bg='black',
                               highlightthickness=0)
        self.field.place(x=0, y=0)

        for row_num, row in enumerate(self.game_map):
            for cell_num, cell in enumerate(row):
                x = cell_num * self.cell_size + self.offset_x + 0.25 * self.cell_size
                y = row_num * self.cell_size + self.offset_y + 0.25 * self.cell_size

                if self.game_map[row_num][cell_num] == '#':
                    end_x = x + self.cell_size
                    end_y = y + self.cell_size

                    self.field.create_rectangle((x, y), (end_x, end_y), fill='purple', tags="Wall")

                elif self.game_map[row_num][cell_num] == '.':
                    start_x = x + 0.41 * self.cell_size
                    start_y = y + 0.41 * self.cell_size
                    end_x = x + 0.59 * self.cell_size
                    end_y = y + 0.59 * self.cell_size

                    self.game_map[row_num][cell_num] = self.field.create_rectangle((start_x, start_y), (end_x, end_y),
                                                                                   fill='white', tags="Dot")
                    self.dot_num += 1

                elif self.game_map[row_num][cell_num] == ' ':
                    pass

                else:
                    if not self._more_game_objects(row_num, cell_num):
                        raise MapGenerationError(
                            f"Unknown character found in the map table: '{self.game_map[row_num][cell_num]}'. "
                            f"If you are the creator of this map, replace the character on position "
                            f"{[row_num, cell_num]} with valid one")

        if not self.pac:
            raise MapGenerationError(
                "Map has no pacman location specified!!! If you are the creator of this map, you should "
                "set 'p' in map array to set pacman start location.")

        self.field.tag_raise("CharacterEntity", "Dot")

        self.field.create_rectangle((self.offset_x - self.cell_size, self.offset_y - self.cell_size),
                                    (self.offset_x + self.map_width + self.cell_size,
                                     self.offset_y + self.map_height + self.cell_size + 1),
                                    outline='black', width=self.cell_size * 2)

        self.field.create_rectangle((-1, -1), (self.window_width + 1, self.window_height / 20), fill='black',
                                    outline='purple')
        self.field.create_rectangle((-1, self.window_height - self.window_height / 40),
                                    (self.window_width + 1, self.window_height + 1),
                                    fill='black', outline='purple')

    def _more_game_objects(self, row_num, cell_num):
        if self.game_map[row_num][cell_num] == 'p':
            self.pac = Pac(self, cell_num, row_num)
            return True
        return False

    def _gui_init(self):
        self.field.create_text(self.window_width / 2, self.window_height - self.window_height / 110,
                               text='Menu -- "Esc"',
                               fill='white', font=('ArialBold', self.window_height // 90), anchor='center')


class ClassicGameMode(Game):
    gm_name = "Classic"
    gm_short = "cl"

    score = 0
    ghosts = []

    def lost_game(self):
        super().lost_game()
        self._modal.append(self.field.create_text(0.5 * self.window_width, 0.440 * self.window_height,
                                                  text="You've died!", fill='white',
                                                  font=('ArialBold', int(0.01 * self.window_height))))

    def _reset_properties(self):
        self.process = 'game'
        self.score = 0
        self.ghosts = []  # comment this to see something funny

    def _gui_init(self):
        self.score_label = self.field.create_text(40, self.window_height / 40, text='Score: 0', fill='white',
                                                  font=('ArialBold', self.window_height // 50), anchor='w')

        self.field.create_text(self.window_width / 2, self.window_height - self.window_height / 110,
                               text='Menu -- "Esc"',
                               fill='white', font=('ArialBold', self.window_height // 90), anchor='center')

    def _game_rules(self):
        if 0 == self.dot_num:
            self.won_game()

    def _more_game_objects(self, row_num, cell_num):
        if super()._more_game_objects(row_num, cell_num):
            return True
        elif self.game_map[row_num][cell_num] == 'g':
            self.ghosts.append(Ghost(self, cell_num, row_num,
                                     random.choice(["red", "blue", "orange", "pink", "cyan", "gray", "brown"])))
            return True
        return False

    def _game_cycle(self):
        try:
            time.sleep(0.03)
            if self.process == 'game':
                self.pac.move()

                for ghost in self.ghosts:
                    ghost.move()

                self._game_rules()
        except KeyboardInterrupt:
            exit()


class TimeRaceGameMode(Game):
    gm_name = "Time race"
    gm_short = "tr"

    score = 0
    max_game_duration = 0

    _game_start_time = 0
    _pause_start_time = 0
    _pause_duration = 0

    _time_label = None
    score_label = None

    def __init__(self, window, game_map):
        super().__init__(window, game_map)
        self.max_game_duration = game_map["maxGameDuration"]

    def lost_game(self):
        super().lost_game()
        self._modal.append(self.field.create_text(0.5 * self.window_width, 0.440 * self.window_height,
                                                  text="Time's up!", fill='white',
                                                  font=('ArialBold', int(0.01 * self.window_height))))

    def _open_menu(self):
        self._pause_start_time = time.time()
        super()._open_menu()

    def _close_menu(self):
        super()._close_menu()
        self._pause_duration += time.time() - self._pause_start_time
        self._pause_start_time = 0

    def _gui_init(self):
        self.score_label = self.field.create_text(40, self.window_height / 40, text='Score: 0', fill='white',
                                                  font=('ArialBold', self.window_height // 50), anchor='w')

        self._time_label = self.field.create_text(self.window_width - 40, self.window_height / 40,
                                                  text='Time left: ' + str(self.max_game_duration // 60) + ':' +
                                                       str(float(self.max_game_duration % 60)),
                                                  fill='white', font=('ArialBold', self.window_height // 50),
                                                  anchor='e')

        self.field.create_text(self.window_width / 2, self.window_height - self.window_height / 110,
                               text='Menu -- "Esc"',
                               fill='white', font=('ArialBold', self.window_height // 90), anchor='center')

    def _reset_properties(self):
        self.process = 'game'
        self.score = 0
        self._game_start_time = time.time()

    def _game_rules(self):
        game_time = self.max_game_duration - (time.time() - self._game_start_time - self._pause_duration)

        if game_time < 0:
            self.pac.die()
        elif 0 == self.dot_num:
            self.score += round(game_time * 1000)
            self.won_game()
        else:
            time_m = game_time // 60
            time_s = game_time % 60

            if self.process == 'game':
                self.field.itemconfig(self._time_label,
                                      text='Time left: ' + str(int(time_m)) + ':' + str(round(time_s, 1)))


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

