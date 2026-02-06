import tkinter as tk
import os                       # Dateiname und Größe
import audioread                # Audio-Metadaten (MP3)
import soundfile as sf          # Audio-Datei laden (WAV / MP3 / FLAC)
from tkinter import filedialog
from .config import (
    BG_FRAME, 
    BTN_ACTIVE, 
    FG_TEXT, 
    SECTION_FONT, 
    TEXT_FONT, 
    ACCENT, 
    topframeheight, 
    BTN_INACTIVE, 
    BTN_PAUSE
)


def create_input_frame(parent, engine):

    frame = tk.Frame(parent, bg=BG_FRAME)
    frame.grid(row=0, column=0, sticky="nsew", padx=10)

    #Frame-Größe fixieren
    frame.grid_propagate(False)
    frame.pack_propagate(False)

    #Frame-Höhe einstellen
    frame.configure(height=topframeheight)

    # Input Label-------------------------------------------------
    tk.Label(
        frame,
        text="Input Signal",
        font=SECTION_FONT,
        bg=BG_FRAME,
        fg=FG_TEXT
    ).pack(anchor="w", padx=10, pady=10)

    # Waveform Diagram--------------------------------------------
    tk.Label(
        frame,
        text="[ Waveform Placeholder ]",
        bg="#000000",
        fg=FG_TEXT,
        height=8
    ).pack(fill="x", padx=10, pady=(0, 8))

    # Frequency Spectrum Diagram----------------------------------
    tk.Label(
        frame,
        text="[ Frequency Spectrum Placeholder ]",
        bg="#000000",
        fg=FG_TEXT,
        height=8
    ).pack(fill="x", padx=10)

    # Frame Control and import Buttons----------------------------
    input_controls_frame = tk.Frame(frame, bg=BG_FRAME)
    input_controls_frame.pack(fill="x", padx=10, pady=10)

    # Import Button logik-----------------------------------------------
    def on_button_click_insertdata():
        file_path = filedialog.askopenfilename(
            title="Select an audio file",
            filetypes=[("Audio-Dateien", "*.wav *.mp3 *.flac")]
        )

        if not file_path:
            return  # Abbrechen, wenn keine Datei ausgewählt wurde

        # Dateiname und Größe-------------------------------------
        filename = os.path.basename(file_path)
        filesize_bytes = os.path.getsize(file_path)
        filesize_mb = filesize_bytes / (1024 * 1024)


        # Audio-Metadaten (WAV / FLAC / MP3)--------------------------
        try:
            if file_path.lower().endswith((".wav", ".flac")):
                with sf.SoundFile(file_path) as audio:
                    samplerate = audio.samplerate
                    frames = len(audio)
                    duration_sec = frames / samplerate

            elif file_path.lower().endswith(".mp3"):
                with audioread.audio_open(file_path) as audio:
                    samplerate = audio.samplerate
                    duration_sec = audio.duration

            else:
                raise ValueError("Nicht unterstütztes Audioformat")

        except Exception as e:
            file_label.config(text="Fehler beim Laden der Audiodatei")
            info_label.config(text="-")
            print("Audio load error:", e)
            return


        minutes = int(duration_sec // 60)
        seconds = int(duration_sec % 60)

        # Labels updaten------------------------------------------
        file_label.config(
            text=f"{filename} | {filesize_mb:.2f} MB"
        )

        info_label.config(
            text=f"Samplerate: {samplerate} Hz\nDauer: {minutes:02d}:{seconds:02d}"
        )

        # Audio in Engine laden
        engine.load_input(file_path)  


        print("Audio geladen:", file_path)

    # Import Button-----------------------------------------------
    tk.Button(
        input_controls_frame,
        text="Import Audio",
        bg=ACCENT,
        fg="white",
        padx=5,
        pady=5,
        command=on_button_click_insertdata
    ).pack(side="left")

    # Left Spacer-------------------------------------------------
    tk.Frame(input_controls_frame, bg=BG_FRAME).pack(side="left", expand=True)

    # Button State------------------------------------------------
    input_playing = False

    def update_buttons():
        play_btn.config(
            bg=BTN_ACTIVE if input_playing else BTN_INACTIVE
        )
        pause_btn.config(
            bg=BTN_PAUSE if not input_playing else BTN_INACTIVE
        )

    def on_play():
        nonlocal input_playing
        engine.play_input()
        input_playing = True
        update_buttons()

    def on_pause():
        nonlocal input_playing
        engine.pause_all()
        input_playing = False
        update_buttons()

    play_btn = tk.Button(
        input_controls_frame,
        text="Play",
        width=8,
        bg=BTN_INACTIVE,
        fg="white",
        command=on_play
    )
    play_btn.pack(side="left", padx=5)

    pause_btn = tk.Button(
        input_controls_frame,
        text="Pause",
        width=8,
        bg=BTN_PAUSE,
        fg="white",
        command=on_pause
    )
    pause_btn.pack(side="left", padx=5)

    # Right Spacer------------------------------------------------
    tk.Frame(input_controls_frame, bg=BG_FRAME).pack(side="left", expand=True)

    # Samplerate and Duration------------------------------------
    info_label = tk.Label(
        frame,
        text="Samplerate: -\nDauer: -",
        font=TEXT_FONT,
        bg=BG_FRAME,
        fg=FG_TEXT,
        justify="left"
    )
    info_label.pack(anchor="w", padx=10, pady=10)

    # Filename and Size------------------------------------------
    file_label = tk.Label(
        frame,
        text="Keine Datei geladen",
        font=TEXT_FONT,
        bg=BG_FRAME,
        fg=FG_TEXT,
        justify="left"
    )
    file_label.pack(anchor="w", padx=10, pady=10)

    return frame
