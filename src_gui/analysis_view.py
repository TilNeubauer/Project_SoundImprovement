import tkinter as tk
from .config import *

def create_analysis_section(parent):
    frame = tk.Frame(parent, bg=BG_FRAME)
    frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

    frame.columnconfigure((0, 1, 2), weight=1)

    def analysis_box(parent, title, col):
        box = tk.Frame(parent, bg="#000000")
        box.grid(row=0, column=col, sticky="nsew", padx=10)

        tk.Label(
            box,
            text=title,
            bg="#000000",
            fg=FG_TEXT
        ).pack(anchor="w", padx=5, pady=5)

        tk.Label(
            box,
            text="[ Plot Placeholder ]",
            bg="#000000",
            fg=FG_TEXT,
            height=6
        ).pack(fill="both", expand=True, padx=5, pady=5)

    analysis_box(frame, "Frequenzspektrum", 0)
    analysis_box(frame, "Wellenformvergleich", 1)
    analysis_box(frame, "Frequenzspektrum", 2)

    return frame
