from src_gui.main_window import create_main_window
from src_gui.header import create_header
from src_gui.main_content import create_main_content
from src_gui.input_frame import create_input_frame
from src_gui.pipeline_frame import create_pipeline_frame
from src_gui.output_frame import create_output_frame
from src_gui.analysis import create_analysis_section

def main():
    root = create_main_window()

    create_header(root)

    main_content = create_main_content(root)
    create_input_frame(main_content)
    create_pipeline_frame(main_content)
    create_output_frame(main_content)

    create_analysis_section(root)

    root.mainloop()

if __name__ == "__main__":
    main()
