import tkinter as tk
from .config import BG_FRAME, FG_TEXT, ACCENT

def create_analysis_section(parent):
    frame = tk.Frame(parent, bg=BG_FRAME)
    frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

    frame.columnconfigure((0, 1, 2), weight=1)

    def analysis_box(parent, title, col):
        box = tk.Frame(parent, bg="#000000")
        box.grid(row=0, column=col, sticky="nsew", padx=10)

        tk.Label(box, text=title, bg="#000000", fg=FG_TEXT).pack(anchor="w", padx=5)
        tk.Label(box, text="[ Plot Placeholder ]",
                 bg="#000000", fg=FG_TEXT, height=6).pack()

    #Analysis container left-----------------------------------------
    analysis_box(frame, "Frequenzspektrum", 0)

    #Scrubber container----------------------------------------------
    # --- Scrubber / Timeline Container ---
    scrubber_frame = tk.Frame(frame, bg="#000000")
    scrubber_frame.grid(row=0, column=1, sticky="nsew", padx=10)

    tk.Label(
        scrubber_frame,
        text="Timeline Scrubber",
        bg="#000000",
        fg=FG_TEXT
    ).pack(anchor="w", padx=5, pady=5)

    scrub_var = tk.DoubleVar(value=0.0)

    #Scrubber Slider
    scrubber = tk.Scale(
        scrubber_frame,
        from_=0,
        to=100,
        orient="horizontal",
        variable=scrub_var,
        length=300,
        showvalue=True,
        bg=ACCENT,
        fg="white",
        troughcolor="#444444",
    )
    scrubber.pack(fill="x", padx=10, pady=20)

    #Scrubber scrub function
    def on_scrub(value):
        position = float(value)
        print(f"Scrub Position: {position:.1f}%")

    scrubber.config(command=on_scrub)



    #Analysis container right-------------------------------------
    analysis_box(frame, "Frequenzspektrum", 2)

    return frame
