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

    tk.Label(
        frame,
        text="[ Waveform Placeholder ]",
        bg="#000000",
        fg=FG_TEXT,
        height=8
    ).pack(fill="x", padx=10, pady=(0, 8))

    tk.Label(
        frame,
        text="[ Frequency Spectrum Placeholder ]",
        bg="#000000",
        fg=FG_TEXT,
        height=8
    ).pack(fill="x", padx=10)

    controls = tk.Frame(frame, bg=BG_FRAME)
    controls.pack(fill="x", padx=10, pady=10)

    def import_audio():
        filedialog.askopenfilename(
            filetypes=[("Audio", "*.wav *.mp3 *.flac")]
        )

    tk.Button(
        controls,
        text="Import Audio",
        bg=ACCENT,
        fg="white",
        command=import_audio
    ).pack(side="left")

    tk.Frame(controls, bg=BG_FRAME).pack(side="left", expand=True)

    tk.Button(controls, text="Play").pack(side="left", padx=5)
    tk.Button(controls, text="Pause").pack(side="left", padx=5)

    tk.Frame(controls, bg=BG_FRAME).pack(side="left", expand=True)

    return frame
