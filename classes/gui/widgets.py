import tkinter as tk
from tkinter import ttk
from typing import Callable


class Button(tk.Button):
    def __init__(
            self,
            master: tk.Misc,
            action: Callable = None,
            fontfamily: str = 'Arial',
            fontsize: int = 14,
            fontstyle: str = 'bold',
            **kwargs
    ):
        self._cycle: int = 0
        self._size: int = fontsize
        self._current_size: int = fontsize
        self._action: Callable = action
        self._animation_step: int = fontsize // 40
        self._fontfamily = fontfamily
        self._fontstyle = fontstyle

        kwargs.setdefault('font', (fontfamily, fontsize, fontstyle))
        kwargs.setdefault('fg', 'purple')
        kwargs.setdefault('bg', 'black')
        kwargs.setdefault('bd', 0)
        kwargs.setdefault('activebackground', 'purple')
        kwargs.setdefault('activeforeground', 'black')
        kwargs.setdefault('highlightthickness', 5)
        kwargs.setdefault('highlightbackground', 'purple')
        kwargs.setdefault('relief', 'flat')
        kwargs.setdefault('cursor', 'hand2')
        super().__init__(master, **kwargs)

        self.bind('<Button-1>', lambda e: self.after(0, self._next_frame))

    def _next_frame(self):
        cycle = self._cycle

        if cycle == 0:
            self.config(cursor='watch', bg='purple', fg='black')

        if cycle <= 5 or cycle > 15:
            self._current_size -= self._animation_step
        else:
            self._current_size += self._animation_step

        self.config(font=(self._fontfamily, self._current_size, self._fontstyle))

        if cycle == 19:
            self.config(cursor='hand2', bg='black', fg='purple')
            self._cycle = 0
            self._action()
        else:
            self._cycle += 1
            self.after(8, self._next_frame)


class Entry(tk.Entry):
    def __init__(
            self,
            master: tk.Misc,
            fontfamily: str = 'Arial',
            fontsize: int = 14,
            fontstyle: str = 'bold',
            **kwargs,
    ):
        kwargs.setdefault('font', (fontfamily, fontsize, fontstyle))
        kwargs.setdefault('fg', 'purple')
        kwargs.setdefault('bg', 'black')
        kwargs.setdefault('bd', 0)
        kwargs.setdefault('highlightcolor', 'purple')
        kwargs.setdefault('highlightthickness', 5)
        kwargs.setdefault('highlightbackground', 'purple')
        kwargs.setdefault('relief', 'flat')
        kwargs.setdefault('cursor', 'hand2')
        kwargs.setdefault('selectbackground', 'purple')
        kwargs.setdefault('insertbackground', 'purple')
        kwargs.setdefault('insertwidth', 5)
        super().__init__(master, **kwargs)


class TextBox(tk.Text):
    def __init__(
            self,
            master: tk.Misc,
            fontfamily: str = 'Arial',
            fontsize: int = 14,
            fontstyle: str = 'bold',
            **kwargs
    ):
        kwargs.setdefault('font', (fontfamily, fontsize, fontstyle))
        kwargs.setdefault('fg', 'purple')
        kwargs.setdefault('bg', 'black')
        kwargs.setdefault('bd', 0)
        kwargs.setdefault('highlightcolor', 'purple')
        kwargs.setdefault('highlightthickness', 5)
        kwargs.setdefault('highlightbackground', 'purple')
        kwargs.setdefault('relief', 'flat')
        kwargs.setdefault('cursor', 'hand2')
        kwargs.setdefault('selectbackground', 'purple')
        kwargs.setdefault('insertbackground', 'purple')
        kwargs.setdefault('insertwidth', 5)
        kwargs.setdefault('wrap', 'none')
        kwargs.setdefault('height', 1)
        super().__init__(master, **kwargs)

    def disable(self):
        self.configure(state='disabled')

    def end_insert(self, text):
        super().insert(tk.END, text)


class Label(tk.Label):
    def __init__(
            self,
            master: tk.Misc,
            fontfamily: str = 'Arial',
            fontsize: int = 14,
            fontstyle: str = 'bold',
            **kwargs
    ):
        kwargs.setdefault('font', (fontfamily, fontsize, fontstyle))
        kwargs.setdefault('fg', 'purple')
        kwargs.setdefault('bg', 'black')
        super().__init__(master, **kwargs)


class Scrollbar(ttk.Scrollbar):
    def __init__(
            self,
            master: tk.Misc,
            width: int,
            **kwargs
    ):
        style = ttk.Style(master)
        style.layout(
            'Custom.Vertical.TScrollbar',
            [(
                'Vertical.Scrollbar.trough',
                {'sticky': 'ns', 'children': [('Vertical.Scrollbar.thumb', {'sticky': 'nswe'})]}
            )]
        )
        style.configure(
            'Custom.Vertical.TScrollbar',
            width=width,
            arrowsize=width,
            troughcolor='black',
            outline='purple',
            borderwidth=0
        )
        style.map(
            'Custom.Vertical.TScrollbar',
            background=[('', 'purple')]
        )

        kwargs.setdefault('cursor', 'hand1')
        kwargs.setdefault('style', 'Custom.Vertical.TScrollbar')
        super().__init__(master, **kwargs)


class Frame(tk.Frame):
    def __init__(
            self,
            master: tk.Misc,
            **kwargs
    ):
        kwargs.setdefault('bg', 'black')
        kwargs.setdefault('highlightthickness', 5)
        kwargs.setdefault('highlightcolor', 'purple')
        kwargs.setdefault('highlightbackground', 'purple')
        super().__init__(master, **kwargs)


class ScrollFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        kwargs.setdefault('bg', 'black')

        self._canvas = tk.Canvas(master, bg=kwargs['bg'], highlightthickness=0)
        self._scrollbar = Scrollbar(master, width=int(0.01 * master.winfo_width()), command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=self._scrollbar.set)

        self._scrollbar.pack(side='right', fill='y', padx=5, pady=5)
        self._canvas.pack(side="left", fill="both", expand=True)

        super().__init__(self._canvas, **kwargs)

        self.update()
        self._window_id = self._canvas.create_window((0, 0), window=self, anchor="nw", width=self._canvas.winfo_width())

        self.bind("<Configure>", lambda e: self._canvas.config(scrollregion=self._canvas.bbox("all")))

        # Scroll for Linux
        self.bind_all("<Button-4>", lambda e: self._canvas.yview_scroll(-1, "units"))
        self.bind_all("<Button-5>", lambda e: self._canvas.yview_scroll(1, "units"))
