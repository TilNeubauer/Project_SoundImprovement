import tkinter as tk
from .config import BG_MAIN

def create_main_content(parent):
    frame = tk.Frame(parent, bg=BG_MAIN)
    frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

    #Alle Spalten gleichmäßig verteilen
    frame.columnconfigure(0, weight=1, uniform="main")
    frame.columnconfigure(1, weight=1, uniform="main")
    frame.columnconfigure(2, weight=1, uniform="main")
    
    #Zeilenhöhe festlegen
    frame.rowconfigure((0), weight=1)

    return frame
