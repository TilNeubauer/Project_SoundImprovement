import tkinter as tk
from .config import BG_MAIN

def create_main_content(parent):
    frame = tk.Frame(parent, bg=BG_MAIN)
    frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

    frame.columnconfigure((0, 1, 2), weight=1)

    return frame
