import tkinter as tk
from tkinter import filedialog
from .config import *

def create_output_frame(parent):
    frame = tk.Frame(parent, bg=BG_FRAME)
    frame.grid(row=0, column=2, sticky="nsew", padx=10)

    tk.Label(
        frame,
        text="Output Signal",
        font=SECTION_FONT,
        bg=BG_FRAME,
        fg=FG_TEXT
    ).pack(anchor="w", padx=10, pady=10)

    tk.Label(
        frame,
        text="[ Processed Waveform Placeholder ]",
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

    tk.Frame(controls, bg=BG_FRAME).pack(side="left", expand=True)

    tk.Button(controls, text="Play").pack(side="left", padx=5)
    tk.Button(controls, text="Pause").pack(side="left", padx=5)

    tk.Frame(controls, bg=BG_FRAME).pack(side="left", expand=True)

    def save_audio():
        filedialog.askopenfilename(
            title="Save Audio",
            filetypes=[("Audio", "*.wav *.mp3 *.flac")]
        )

    tk.Button(
        controls,
        text="Save Audio",
        bg=ACCENT,
        fg="white",
        padx=5,
        pady=5,
        command=save_audio
    ).pack(side="right")

    tk.Label(
        frame,
        text="Samplerate: 44.1 kHz\nDauer: 00:00",
        font=TEXT_FONT,
        bg=BG_FRAME,
        fg=FG_TEXT,
        justify="right"
    ).pack(anchor="se", padx=10, pady=10)

    tk.Label(
        frame,
        text="[Filename] [Datatype] [Filesize]",
        font=TEXT_FONT,
        bg=BG_FRAME,
        fg=FG_TEXT
    ).pack(anchor="w", padx=10, pady=10)

    return frame
