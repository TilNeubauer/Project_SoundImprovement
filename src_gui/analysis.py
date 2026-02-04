import tkinter as tk
from .config import BG_FRAME, FG_TEXT


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
        ).pack(anchor="w", padx=5)

        tk.Label(
            box,
            text="[ Plot Placeholder ]",
            bg="#000000",
            fg=FG_TEXT,
            height=6
        ).pack()

  
    # Analysis container LEFT----------------------------
    analysis_box(frame, "Frequenzspektrum", 0)


    # Scrubber / Timeline container (MITTELTEIL)-----------------------
    scrubber_frame = tk.Frame(frame, bg="#000000")
    scrubber_frame.grid(row=0, column=1, sticky="nsew", padx=10)

    tk.Label(
        scrubber_frame,
        text="Timeline Scrubber",
        bg="#000000",
        fg=FG_TEXT
    ).pack(anchor="w", padx=5, pady=5)

    time_label = tk.Label(
        scrubber_frame,
        text="00:00.000 / 00:00.000",
        bg="#000000",
        fg=FG_TEXT,
        font=("Helvetica", 10, "bold")
    )
    time_label.pack(pady=(10, 5))

    timeline = tk.Scale(
        scrubber_frame,
        from_=0.0,
        to=1.0,            # wird später durch main_gui gesetzt
        orient="horizontal",
        resolution=0.001,  # Millisekunden
        length=350,
        showvalue=False
    )
    timeline.pack(fill="x", padx=10, pady=15)


    # Analysis container RIGHT---------------------------
    analysis_box(frame, "Frequenzspektrum", 2)

    # WICHTIG: klare Rückgabe
    return frame, timeline, time_label
