import tkinter as tk
from tkinter import filedialog
from .config import BG_FRAME, FG_TEXT, SECTION_FONT, TEXT_FONT, ACCENT


def create_input_frame(parent):

    frame = tk.Frame(parent, bg=BG_FRAME)
    frame.grid(row=0, column=0, sticky="nsew", padx=10)

    # Input Label
    tk.Label(
        frame,
        text="Input Signal",
        font=SECTION_FONT,
        bg=BG_FRAME,
        fg=FG_TEXT
    ).pack(anchor="w", padx=10, pady=10)

    # Waveform Diagram
    tk.Label(
        frame,
        text="[ Waveform Placeholder ]",
        bg="#000000",
        fg=FG_TEXT,
        height=8
    ).pack(fill="x", padx=10, pady=(0, 8))

    # Frequency Spectrum Diagram
    tk.Label(
        frame,
        text="[ Frequency Spectrum Placeholder ]",
        bg="#000000",
        fg=FG_TEXT,
        height=8
    ).pack(fill="x", padx=10)

    # Frame Control and import Buttons
    input_controls_frame = tk.Frame(frame, bg=BG_FRAME)
    input_controls_frame.pack(fill="x", padx=10, pady=10)

    # Import Button
    def on_button_click_insertdata():
        file_path = filedialog.askopenfilename(
            title="Select an audio file",
            filetypes=[("Audio-Dateien", "*.wav *.mp3 *.flac")]
        )
        if file_path:
            print(f"Ausgewählte Datei: {file_path}")
            # spätere Verarbeitung hier

    tk.Button(
        input_controls_frame,
        text="Import Audio",
        bg=ACCENT,
        fg="white",
        padx=5,
        pady=5,
        command=on_button_click_insertdata
    ).pack(side="left")

    # Left Spacer
    tk.Frame(input_controls_frame, bg=BG_FRAME).pack(side="left", expand=True)

    # Play Button
    tk.Button(
        input_controls_frame,
        text="Play"
    ).pack(side="left", padx=5)

    # Pause Button
    tk.Button(
        input_controls_frame,
        text="Pause"
    ).pack(side="left", padx=5)

    # Right Spacer
    tk.Frame(input_controls_frame, bg=BG_FRAME).pack(side="left", expand=True)

    # Samplerate and Duration
    tk.Label(
        frame,
        text="Samplerate: 44.1 kHz\nDauer: 00:00",
        font=TEXT_FONT,
        bg=BG_FRAME,
        fg=FG_TEXT,
        justify="right"
    ).pack(anchor="se", padx=10, pady=10)

    # Filename and Size
    tk.Label(
        frame,
        text="[Filename dummy] [Datatype dummy] [filesize dummy]",
        font=TEXT_FONT,
        bg=BG_FRAME,
        fg=FG_TEXT,
        justify="left"
    ).pack(anchor="w", padx=10, pady=10)

    return frame
