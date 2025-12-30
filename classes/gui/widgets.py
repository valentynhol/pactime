import tkinter as tk
import tkinter.font as tkfont
import typing
from tkinter import ttk


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
        kwargs.setdefault('inactiveselectbackground', 'purple')
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

        self.bind("<Configure>", self._on_configure)
        self.bind("<Enter>", self._bind_mousewheel)
        self.bind("<Leave>", self._unbind_mousewheel)

    def _on_configure(self, e):
        self.update_idletasks()

        canvas_height = self._canvas.winfo_height()
        content_height = self.winfo_reqheight()

        if content_height <= canvas_height:
            self._canvas.configure(scrollregion=(0, 0, 0, canvas_height))
            self._canvas.yview_moveto(0)
            self._scrollbar.set(0, 1)
        else:
            self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _bind_mousewheel(self, e):
        self._canvas.bind_all("<MouseWheel>", self._on_mousewheel)  # Windows / macOS
        self._canvas.bind_all("<Button-4>", self._on_mousewheel_linux)  # Linux
        self._canvas.bind_all("<Button-5>", self._on_mousewheel_linux)

    def _unbind_mousewheel(self, e):
        self._canvas.unbind_all("<MouseWheel>")
        self._canvas.unbind_all("<Button-4>")
        self._canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):
        self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_linux(self, event):
        if event.num == 4:
            self._canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self._canvas.yview_scroll(1, "units")


class Button(tk.Frame):
    def __init__(
            self,
            master: tk.Misc,
            action: typing.Callable = None,
            text="",
            fontfamily: str = 'Arial',
            fontsize: int = 14,
            fontstyle: typing.Literal["normal", "bold"] = 'bold',
            width: int | None = None,
            **kwargs
    ):
        super().__init__(master, bg=master.cget("bg"))
        self._master = master

        self._cycle = 0
        self._fontfamily = fontfamily
        self._fontstyle = fontstyle
        self._action = action

        self._max_font_size = fontsize
        self._current_scale = 0.9  # Start at 90% size

        frame_padx = kwargs.pop("padx", 0)
        frame_pady = kwargs.pop("pady", 0)

        kwargs.setdefault('fg', 'purple')
        kwargs.setdefault('bg', 'black')
        kwargs.setdefault('bd', 0)
        kwargs.setdefault('activebackground', 'purple')
        kwargs.setdefault('activeforeground', 'black')
        kwargs.setdefault('highlightthickness', 5)
        kwargs.setdefault('highlightbackground', 'purple')
        kwargs.setdefault('relief', 'flat')
        kwargs.setdefault('cursor', 'hand2')

        btn_bd = kwargs.get('bd')
        btn_hl = kwargs.get('highlightthickness')
        btn_internal_pad_x = 1
        btn_internal_pad_y = 1

        overhead_x = 2 * (btn_bd + btn_hl + btn_internal_pad_x + frame_padx)
        overhead_y = 2 * (btn_bd + btn_hl + btn_internal_pad_y + frame_pady)

        f_max = tkfont.Font(family=fontfamily, size=self._max_font_size, weight=fontstyle)

        char_w = f_max.measure("0")
        char_h = f_max.metrics("linespace")

        if width:
            available_w = width - overhead_x
            char_capacity = max(1, available_w // char_w)
            self._frame_width = (char_capacity * char_w) + overhead_x
        else:
            text_w = f_max.measure(text)
            self._frame_width = text_w + overhead_x

        self._frame_height = char_h + overhead_y

        self.config(width=self._frame_width, height=self._frame_height)
        self.pack_propagate(False)

        initial_width = int(self._frame_width * self._current_scale)
        initial_height = int(self._frame_height * self._current_scale)

        initial_fontsize = int(self._max_font_size * self._current_scale)

        kwargs['font'] = (fontfamily, initial_fontsize, fontstyle)

        self._button = tk.Button(self, text=text, **kwargs)
        self._button.place(
            relx=0.5, rely=0.5, anchor="center",
            width=initial_width, height=initial_height
        )
        # noinspection PyTypeChecker
        self._button.bind("<Button-1>", lambda e: self.after(0, self._next_frame))

    def _next_frame(self):
        cycle = self._cycle

        if cycle == 0:
            self._button.config(cursor='watch', bg='purple', fg='black')

        if cycle <= 5:
            self._current_scale -= (0.05 / 6)
        elif cycle <= 15:
            self._current_scale += (0.15 / 10)
        else:
            self._current_scale -= (0.10 / 4)

        new_font_size = int(self._max_font_size * self._current_scale)

        button_width = int(self._frame_width * self._current_scale)
        button_height = int(self._frame_height * self._current_scale)

        self._button.config(font=(self._fontfamily, new_font_size, self._fontstyle))

        self._button.place(
            relx=0.5, rely=0.5, anchor="center",
            width=button_width, height=button_height
        )

        if cycle == 19:
            self._current_scale = 0.9
            reset_w = int(self._frame_width * 0.9)
            reset_h = int(self._frame_height * 0.9)
            reset_f = int(self._max_font_size * 0.9)

            self._button.config(cursor='hand2', bg='black', fg='purple',
                                font=(self._fontfamily, reset_f, self._fontstyle))
            self._button.place(width=reset_w, height=reset_h)

            self._cycle = 0
            if self._action:
                # noinspection PyTypeChecker
                self._master.after(0, self._action)
        else:
            self._cycle += 1
            # noinspection PyTypeChecker
            self.after(8, self._next_frame)
