import tkinter as tk
from tkinter import ttk
from tkinter import filedialog                  #Import filedaten


# Konfiguration----------------------------------------------------------------------
BG_MAIN = "#1E1E1E"
BG_FRAME = "#2A2A2A"
FG_TEXT = "#FFFFFF"
ACCENT = "#3A7CA5"

TITLE_FONT = ("Helvetica", 24, "bold")
SECTION_FONT = ("Helvetica", 14, "bold")
TEXT_FONT = ("Helvetica", 11)


# Main Window-------------------------------------------------------------------
Mainpage = tk.Tk()
Mainpage.title("Audio Signal Processing 2")
Mainpage.geometry("1400x700")
Mainpage.configure(bg=BG_MAIN)

Mainpage.columnconfigure(0, weight=1)
Mainpage.rowconfigure(1, weight=1)
Mainpage.rowconfigure(2, weight=1)


# Header-------------------------------------------------------------------------
header = tk.Frame(Mainpage, bg=BG_FRAME, height=80)
header.grid(row=0, column=0, sticky="ew")
header.columnconfigure(0, weight=1)
header.columnconfigure(1, weight=0)

title_label = tk.Label(
    header,
    text="Audio Signal Processing 2",
    font=TITLE_FONT,
    bg=BG_FRAME,
    fg=FG_TEXT
)
title_label.grid(row=0, column=0, sticky="w", padx=20, pady=20)

#Button (Insert Audio)--------------------------------------------------------------------------
def on_button_click_insertdata():
    file_path = filedialog.askopenfilename(
        title="Wähle eine Audiodatei aus",
        filetypes=[("Audio-Dateien", "*.wav *.mp3 *.flac")]
    )
    if file_path:
        print(f"Ausgewählte Datei: {file_path}")
        # Hier kannst du weitere Verarbeitung hinzufügen, z.B. die Datei laden

load_button = tk.Button(
    header,
    text="Audio Datei laden",
    bg=ACCENT,
    fg="white",
    padx=15,
    pady=5,
    command = on_button_click_insertdata
)
load_button.grid(row=0, column=1, sticky="e", padx=20)


# Main Content---------------------------------------------------------------
main_frame = tk.Frame(Mainpage, bg=BG_MAIN)
main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.columnconfigure(2, weight=1)


# Input Signal----------------------------------------------------------
input_frame = tk.Frame(main_frame, bg=BG_FRAME)
input_frame.grid(row=0, column=0, sticky="nsew", padx=10)

tk.Label(
    input_frame,
    text="Input Signal",
    font=SECTION_FONT,
    bg=BG_FRAME,
    fg=FG_TEXT
).pack(anchor="w", padx=10, pady=10)

tk.Label(
    input_frame,
    text="[ Waveform Placeholder ]",
    bg="#000000",
    fg=FG_TEXT,
    height=8
).pack(fill="x", padx=10)

tk.Label(
    input_frame,
    text="Samplerate: 44.1 kHz\nDauer: 00:00",
    font=TEXT_FONT,
    bg=BG_FRAME,
    fg=FG_TEXT,
    justify="left"
).pack(anchor="w", padx=10, pady=10)

tk.Button(input_frame, text="Abspielen").pack(pady=10)


# Processing Pipeline---------------------------------------------------------
pipeline_frame = tk.Frame(main_frame, bg=BG_FRAME)
pipeline_frame.grid(row=0, column=1, sticky="nsew", padx=10)

tk.Label(
    pipeline_frame,
    text="Processing Pipeline",
    font=SECTION_FONT,
    bg=BG_FRAME,
    fg=FG_TEXT
).pack(anchor="w", padx=10, pady=10)

def dropdown(parent, label, values):
    tk.Label(parent, text=label, bg=BG_FRAME, fg=FG_TEXT).pack(anchor="w", padx=10)
    cb = ttk.Combobox(parent, values=values, state="readonly")
    cb.current(0)
    cb.pack(fill="x", padx=10, pady=5)

dropdown(pipeline_frame, "Filter", ["Low Pass", "High Pass", "Band Pass"])
dropdown(pipeline_frame, "Normalisierung", ["-1 dB", "-3 dB", "-6 dB"])
dropdown(pipeline_frame, "Effekt", ["None", "Echo", "Reverb"])
dropdown(pipeline_frame, "Format", ["WAV", "MP3", "FLAC"])

tk.Button(
    pipeline_frame,
    text="Anwenden",
    bg=ACCENT,
    fg="white",
    padx=20,
    pady=8
).pack(pady=20)


# Output Signal--------------------------------------------------------------
output_frame = tk.Frame(main_frame, bg=BG_FRAME)
output_frame.grid(row=0, column=2, sticky="nsew", padx=10)

tk.Label(
    output_frame,
    text="Output Signal",
    font=SECTION_FONT,
    bg=BG_FRAME,
    fg=FG_TEXT
).pack(anchor="w", padx=10, pady=10)

tk.Label(
    output_frame,
    text="[ Processed Waveform Placeholder ]",
    bg="#000000",
    fg=FG_TEXT,
    height=8
).pack(fill="x", padx=10)

tk.Label(
    output_frame,
    text="Samplerate: 44.1 kHz\nDauer: 00:00",
    font=TEXT_FONT,
    bg=BG_FRAME,
    fg=FG_TEXT,
    justify="left"
).pack(anchor="w", padx=10, pady=10)

tk.Button(output_frame, text="Abspielen").pack(pady=10)


# Analysis Section-------------------------------------------------------------
analysis_frame = tk.Frame(Mainpage, bg=BG_FRAME)
analysis_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

analysis_frame.columnconfigure((0, 1, 2), weight=1)

def analysis_box(parent, title):
    frame = tk.Frame(parent, bg="#000000")
    tk.Label(frame, text=title, bg="#000000", fg=FG_TEXT).pack(anchor="w", padx=5, pady=5)
    tk.Label(frame, text="[ Plot Placeholder ]", bg="#000000", fg=FG_TEXT, height=6).pack()
    return frame

analysis_box(analysis_frame, "Frequenzspektrum").grid(row=0, column=0, sticky="nsew", padx=10)
analysis_box(analysis_frame, "Wellenformvergleich").grid(row=0, column=1, sticky="nsew", padx=10)
analysis_box(analysis_frame, "Dynamik-Messung").grid(row=0, column=2, sticky="nsew", padx=10)


# Start-------------------------------------------------------------------------
Mainpage.mainloop()
