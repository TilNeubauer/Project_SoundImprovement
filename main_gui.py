from src_gui.main_window import create_main_window          #Import main window setup
from src_gui.header import create_header                    #Import header setup
from src_gui.main_content import create_main_content        #Import main content setup
from src_gui.input_frame import create_input_frame          #Import input frame setup
from src_gui.pipeline_frame import create_pipeline_frame    #Import pipeline frame setup
from src_gui.output_frame import create_output_frame        #Import output frame setup
from src_gui.analysis import create_analysis_section        #Import analysis section setup
from src.audio_engine import AudioEngine                    #Import audio engine
import tkinter as tk
from src_gui.config import BG_MAIN


def main():
    root = create_main_window()

    engine = AudioEngine()

    # Zentrale Stelle für UI-Reset
    #...

    # Header erstellen
    create_header(root)

    # Hauptinhalt erstellen
    main_content = create_main_content(root)

    # Middle-Container für Pipeline + Analyse
    middle_container = tk.Frame(main_content, bg=BG_MAIN)
    middle_container.grid(row=0, column=1, sticky="nsew")

    # Layout im Middle-Container
    middle_container.rowconfigure(0, weight=3)      # Pipeline (groß)
    middle_container.rowconfigure(1, weight=2)      # Analyse (klein)
    middle_container.columnconfigure(0, weight=1)   # 

    create_input_frame(main_content, engine)
    create_pipeline_frame(middle_container, engine)
    create_output_frame(main_content, engine)

    # Analysebereich erstellen
    analysis_frame, timeline, time_label = create_analysis_section(middle_container)
    slider_internal_update = False

    # Timeline-Callback
    def on_timeline_change(value):
        nonlocal slider_internal_update
        if slider_internal_update:
            return
        engine.seek(float(value))

    timeline.config(command=on_timeline_change)

    # Timeline-Update-Funktion
    def format_time(t):
        minutes = int(t // 60)
        seconds = int(t % 60)
        millis = int((t - int(t)) * 1000)
        return f"{minutes:02d}:{seconds:02d}.{millis:03d}"

    def update_timeline():
        nonlocal slider_internal_update

        duration = engine.get_duration()
        if duration > 0:
            #Slider-Maximum setzen
            if timeline.cget("to") != duration:
                timeline.config(to=duration)

            current = engine.get_active_time()

            slider_internal_update = True
            timeline.set(current)
            slider_internal_update = False

            time_label.config(
                text=f"{format_time(current)} / {format_time(duration)}"
            )

        root.after(50, update_timeline)

    update_timeline()

    root.mainloop()

if __name__ == "__main__":
    main()
