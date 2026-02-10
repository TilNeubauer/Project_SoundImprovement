import tkinter as tk
from .config import BG_FRAME, FG_TEXT


def create_analysis_section(parent):
    frame = tk.Frame(parent, bg=BG_FRAME)
    frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0,10))
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)
    frame.grid_propagate(False)
    frame.configure(height=130)
    


    # Scrubber / Timeline container (MITTELTEIL)-----------------------
    scrubber_frame = tk.Frame(frame, bg="#000000")
    scrubber_frame.grid_propagate(False)    
    scrubber_frame.grid(row=0, column=0, sticky="nsew", padx=10)


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
    timeline.pack(fill="x", expand=True, padx=10, pady=10)


    # WICHTIG: klare Rückgabe
    return frame, timeline, time_label
