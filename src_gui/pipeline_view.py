import tkinter as tk
from tkinter import ttk
from .config import *

def create_pipeline_frame(parent):
    frame = tk.Frame(parent, bg=BG_FRAME)
    frame.grid(row=0, column=1, sticky="nsew", padx=10)

    tk.Label(
        frame,
        text="Processing Pipeline",
        font=SECTION_FONT,
        bg=BG_FRAME,
        fg=FG_TEXT
    ).pack(anchor="w", padx=10, pady=10)

    def dropdown(label, values):
        tk.Label(
            frame,
            text=label,
            bg=BG_FRAME,
            fg=FG_TEXT
        ).pack(anchor="w", padx=10)

        cb = ttk.Combobox(frame, values=values, state="readonly")
        cb.current(0)
        cb.pack(fill="x", padx=10, pady=5)

    dropdown("Filter", ["Low Pass", "High Pass", "Band Pass"])
    dropdown("Normalisierung", ["-1 dB", "-3 dB", "-6 dB"])
    dropdown("Effekt", ["None", "Echo", "Reverb"])
    dropdown("Format", ["WAV", "MP3", "FLAC"])

    tk.Button(
        frame,
        text="Anwenden",
        bg=ACCENT,
        fg="white",
        padx=20,
        pady=8
    ).pack(pady=20)

    return frame
