import tkinter as tk
import typing

from classes.gui.widgets import Frame, Label

class MiniView(Frame):
    def __init__(
            self,
            master: tk.Misc,
            game_map: dict,
            player_name: str,
            x: int,
            y: int,
            anchor: typing.Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"]="nw",
            **kwargs
    ):
        self._outer_frame = Frame(master, **kwargs)
        self._outer_frame.place(x=x, y=y, anchor=anchor)
        self._outer_frame.update()

        frame_width = self._outer_frame.winfo_width()
        frame_height = self._outer_frame.winfo_height()

        self._player_label = Label(self._outer_frame, text=player_name, fontsize=frame_height//30)
        super().__init__(self._outer_frame, highlightthickness=0)

        self._player_label.pack(side='top')
        self.pack(side='top', fill='both', expand=True)

        map_width = len(game_map["gameMap"][0])
        map_height = len(game_map["gameMap"])

        self._cell_size = min(frame_width // map_width, frame_height // map_height)

        self._x_offset = (frame_width - map_width * self._cell_size) // 2
        self._y_offset = (frame_height - map_height * self._cell_size) // 2

        self._canvas = tk.Canvas(
            self._outer_frame,
            width=frame_width,
            height=frame_height,
            background='black',
            highlightthickness=0
        )
        self._canvas.pack(fill='both', expand=True)

        self._pac_state = None
        self._dot_positions = set()
        self._dot_ids = {}
        self._wall_ids = set()
        self._game_state = "game"
        self._pac_id: typing.Optional[int] = None
        self._gs_label: typing.Optional[Label] = None

        self._build_from_map(game_map["gameMap"])

    def apply_state(self, state):
        new_game_state = state.get("game_state")
        if new_game_state != self._game_state:
            self._game_state = new_game_state
            if new_game_state == "game":
                self._remove_game_state_label()
            else:
                self._create_game_state_label()

        new_pac = state.get("pac_state")
        if new_pac != self._pac_state:
            pac_pos = new_pac["pos"]
            pac_dir = new_pac["direction"]
            if hasattr(self, '_pac_id') and self._pac_id:
                self._canvas.delete(self._pac_id)
            if new_pac:
                x, y = pac_pos
                px = self._x_offset + x * self._cell_size
                py = self._y_offset + y * self._cell_size
                arc_size = 270
                self._pac_id = self._canvas.create_arc(
                    px,
                    py,
                    px + self._cell_size,
                    py + self._cell_size,
                    fill='yellow',
                    start=pac_dir - arc_size / 2,
                    extent=arc_size
                )
            self._pac_state = new_pac

        for dot in state.get("eaten_dots", []):
            dot = tuple(dot)
            if dot in self._dot_ids:
                self._canvas.delete(self._dot_ids[dot])
                del self._dot_ids[dot]

    def _build_from_map(self, game_map):
        self._canvas.delete("all")
        self._dot_positions.clear()
        self._dot_ids.clear()
        self._wall_ids.clear()

        for y, row in enumerate(game_map):
            for x, cell in enumerate(row):
                px = self._x_offset + x * self._cell_size
                py = self._y_offset + y * self._cell_size

                if cell == '#':
                    self._wall_ids.add(
                        self._canvas.create_rectangle(px, py,
                                                      px + self._cell_size, py + self._cell_size,
                                                      fill='purple')
                    )
                elif cell == '.':
                    dot_id = self._canvas.create_rectangle(px + 0.4 * self._cell_size, py + 0.4 * self._cell_size,
                                                           px + 0.6 * self._cell_size, py + 0.6 * self._cell_size,
                                                           fill='white')
                    self._dot_positions.add((x, y))
                    self._dot_ids[(x, y)] = dot_id

    def _create_game_state_label(self):
        if self._game_state == "menu":
            label_text = "Paused"
        elif self._game_state == "game_ended":
            label_text = "Game Ended"
        else:
            return

        self._gs_label = Label(
            self._canvas,
            text=label_text,
            fontsize=self._canvas.winfo_height()//25,
            highlightthickness=5,
            highlightbackground="purple"
        )
        self._gs_label.place(x=self._canvas.winfo_width()//2, y=self._canvas.winfo_height()//2, anchor='center')

    def _remove_game_state_label(self):
        if self._gs_label:
            self._gs_label.destroy()
