from src_gui.window import create_main_window
from src_gui.header import create_header
from src_gui.input_view import create_input_frame
from src_gui.pipeline_view import create_pipeline_frame
from src_gui.output_view import create_output_frame
from src_gui.analysis_view import create_analysis_section
import tkinter as tk

def main():
    root = create_main_window()

    create_header(root)

    main_frame = tk.Frame(root)
    main_frame.grid(row=1, column=0, sticky="nsew", padx=20)

    main_frame.columnconfigure((0, 1, 2), weight=1)

    create_input_frame(main_frame)
    create_pipeline_frame(main_frame)
    create_output_frame(main_frame)

    create_analysis_section(root)

    root.mainloop()

if __name__ == "__main__":
    main()
