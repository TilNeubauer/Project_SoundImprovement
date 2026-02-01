import tkinter as tk
from .config import BG_FRAME, FG_TEXT, TITLE_FONT

def create_header(parent):
    header = tk.Frame(parent, bg=BG_FRAME, height=80)
    header.grid(row=0, column=0, sticky="ew")
    header.grid_propagate(False)

    header.columnconfigure(0, weight=1)

    tk.Label(
        header,
        text="Audio Signal Processing 2",
        font=TITLE_FONT,
        bg=BG_FRAME,
        fg=FG_TEXT
    ).grid(row=0, column=0, sticky="w", padx=20)

    return header
