import tkinter as tk
from tkinter import filedialog
from .config import BG_FRAME, FG_TEXT, SECTION_FONT, TEXT_FONT, ACCENT, topframeheight


def create_output_frame(parent, engine):

    frame = tk.Frame(parent, bg=BG_FRAME)
    frame.grid(row=0, column=2, sticky="nsew", padx=10)

    #Frame-Größe fixieren
    frame.grid_propagate(False)
    frame.pack_propagate(False)

    #Frame-Höhe einstellen
    frame.configure(height=topframeheight)

    # Output Label------------------------------------------------
    tk.Label(
        frame,
        text="Output Signal",
        font=SECTION_FONT,
        bg=BG_FRAME,
        fg=FG_TEXT
    ).pack(anchor="w", padx=10, pady=10)

    # Processed Plots---------------------------------------------
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

    # Control Buttons---------------------------------------------
    controls = tk.Frame(frame, bg=BG_FRAME)
    controls.pack(fill="x", padx=10, pady=10)

    # Left Spacer-------------------------------------------------
    tk.Frame(controls, bg=BG_FRAME).pack(side="left", expand=True)

    # Pause Button (links)----------------------------------------
    pause_button = tk.Button(
        controls,
        text="Pause",
        width=8,
        command=engine.pause_all
    )
    pause_button.pack(side="left", padx=5)

    # Play Button (rechts)----------------------------------------
    def play_output():
        if not engine.has_output():
            print("No processed audio available yet")
            return
        engine.play_output()

    play_button = tk.Button(
        controls,
        text="Play",
        width=8,
        command=play_output
    )
    play_button.pack(side="left", padx=5)

    # Right Spacer------------------------------------------------
    tk.Frame(controls, bg=BG_FRAME).pack(side="left", expand=True)

    # Save Button-------------------------------------------------
    def save_audio():
        if not engine.has_output():
            print("No processed audio available to save")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save processed audio",
            defaultextension=".wav",
            filetypes=[("WAV", "*.wav")]
        )

        if not file_path:
            return

        engine.save_output(file_path)
        print("Processed audio saved to:", file_path)

    tk.Button(
        controls,
        text="Save Audio",
        bg=ACCENT,
        fg="white",
        padx=5,
        pady=5,
        command=save_audio
    ).pack(side="left", padx=5)

    # Metadata Labels---------------------------------------------
    tk.Label(
        frame,
        text="Samplerate: 44.1 kHz\nDauer: 00:00",
        font=TEXT_FONT,
        bg=BG_FRAME,
        fg=FG_TEXT,
        justify="left"
    ).pack(anchor="w", padx=10, pady=6)

    tk.Label(
        frame,
        text="[Filename dummy] [Datatype dummy] [filesize dummy]",
        font=TEXT_FONT,
        bg=BG_FRAME,
        fg=FG_TEXT,
        justify="left"
    ).pack(anchor="w", padx=10, pady=(0, 10))

    return frame
