import tkinter as tk
from tkinter import filedialog
from .config import *

def create_input_frame(parent):

    frame = tk.Frame(parent, bg=BG_FRAME)
    frame.grid(row=0, column=0, sticky="nsew", padx=10)

    tk.Label(
        frame,
        text="Input Signal",
        font=SECTION_FONT,
        bg=BG_FRAME,
        fg=FG_TEXT
    ).pack(anchor="w", padx=10, pady=10)

    # Placeholder
    tk.Label(frame, text="[ Waveform Placeholder ]",
             bg="#000000", fg=FG_TEXT, height=8).pack(fill="x", padx=10)

    tk.Label(frame, text="[ Frequency Spectrum Placeholder ]",
             bg="#000000", fg=FG_TEXT, height=8).pack(fill="x", padx=10, pady=8)

    return frame
