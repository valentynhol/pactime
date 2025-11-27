import tkinter as tk
from typing import List


class MenuAnimation:
    def __init__(
            self,
            master: tk.Misc,
            x: int,
            y: int,
            height: int
    ):
        self.height = height
        self.width = height*3
        self._cycle = 0
        self._canvas: tk.Canvas
        self._pac_id: int
        self._dot_ids: List[int] = []

        canvas = tk.Canvas(master, height=height, width=self.width, bg='black', highlightthickness=0)
        canvas.place(x=x, y=y, anchor='center')
        canvas.update()
        self._canvas = canvas

        for dot_num in range(3):
            self._dot_ids.append(canvas.create_rectangle(
                ((dot_num+1)*height - 0.09*height, 0.41*height),
                ((dot_num+1)*height + 0.09*height, 0.59*height),
                fill='white'
            ))

        self._pac_id = canvas.create_arc((0, 0), (height, height), fill='yellow', start=-45, extent=-270)

        self._canvas.after(8, self._next_frame)

    def _next_frame(self):
        cycle = self._cycle
        canvas = self._canvas

        if cycle % 40 < 20:
            arc_size = -280 - (cycle%40)*4
        else:
            arc_size = -280 - (39 - cycle%40)*4

        for dot_num in range(3):
            if cycle == dot_num*40 + 20:
                canvas.move(self._dot_ids[dot_num], self.height*3, 0)
            canvas.move(self._dot_ids[dot_num], -0.025*self.height, 0)

        canvas.itemconfig(self._pac_id, start=-180 - arc_size / 2, extent=arc_size)

        self._cycle = 0 if cycle == 119 else cycle + 1

        self._canvas.after(8, self._next_frame)

    def destroy(self):
        self._canvas.destroy()
