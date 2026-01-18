import tkinter as tk
from .config import BG_MAIN

def create_main_window():
    root = tk.Tk()
    root.title("Audio Signal Processing 2")
    root.geometry("1400x700")
    root.configure(bg=BG_MAIN)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=1)

    return root
