import tkinter as tk
from tkinter import ttk
from .config import BG_FRAME, FG_TEXT, SECTION_FONT, ACCENT, topframeheight


def create_pipeline_frame(parent, engine):
    # Grund-Frame-------------------------------------------------------
    frame = tk.Frame(parent, bg=BG_FRAME)
    frame.grid(row=0, column=1, sticky="nsew", padx=10)

    #Frame-Größe fixieren
    frame.grid_propagate(False)
    frame.pack_propagate(False)

    #Frame-Höhe einstellen
    frame.configure(height=topframeheight)

    tk.Label(
        frame,
        text="Processing Pipeline",
        font=SECTION_FONT,
        bg=BG_FRAME,
        fg=FG_TEXT
    ).pack(anchor="w", padx=10, pady=10)


    # Filter-Auswahl Dropdown----------------------------------------
    filter_var = tk.StringVar(value="Low Pass")

    tk.Label(frame, text="Filter", bg=BG_FRAME, fg=FG_TEXT)\
        .pack(anchor="w", padx=10)

    filter_cb = ttk.Combobox(
        frame,
        values=["Low Pass", "High Pass", "Band Pass", "SinSig", "Equalizer"],
        textvariable=filter_var,
        state="readonly"
    )
    filter_cb.pack(fill="x", padx=10, pady=5)


    # Container für dynamische Filter--------------------------------
    filter_container = tk.Frame(
        frame,
        bg=BG_FRAME,
        height=450
    )
    filter_container.pack(fill="x", padx=10, pady=10)
    filter_container.pack_propagate(False)

    # LOWPASS--------------------------------------------------------
    lowpass_active = False

    lp_frame = tk.Frame(filter_container, bg=BG_FRAME)

    tk.Label(lp_frame, text="Lowpass Cutoff [Hz]", bg=BG_FRAME, fg=FG_TEXT)\
        .pack(anchor="w")

    lp_cutoff = tk.Entry(lp_frame)
    lp_cutoff.insert(0, "20")
    lp_cutoff.pack(fill="x")

    def toggle_lowpass():
        nonlocal lowpass_active
        lowpass_active = not lowpass_active

        lp_button.config(
            text="Applied" if lowpass_active else "Apply",
            bg="#2E8B57" if lowpass_active else ACCENT
        )

        if lowpass_active:
            print("Lowpass activated:", lp_cutoff.get())
        else:
            print("Lowpass deactivated")

    lp_button = tk.Button(
        lp_frame,
        text="Apply",
        bg=ACCENT,
        fg="white",
        command=toggle_lowpass
    )
    lp_button.pack(pady=5)


    # HIGHPASS--------------------------------------------------------
    highpass_active = False

    hp_frame = tk.Frame(filter_container, bg=BG_FRAME)

    tk.Label(hp_frame, text="Highpass Cutoff [Hz]", bg=BG_FRAME, fg=FG_TEXT)\
        .pack(anchor="w")

    hp_cutoff = tk.Entry(hp_frame)
    hp_cutoff.insert(0, "2000")
    hp_cutoff.pack(fill="x")

    def toggle_highpass():
        nonlocal highpass_active
        highpass_active = not highpass_active

        hp_button.config(
            text="Applied" if highpass_active else "Apply",
            bg="#2E8B57" if highpass_active else ACCENT
        )

        if highpass_active:
            print("Highpass activated:", hp_cutoff.get())
        else:
            print("Highpass deactivated")

    hp_button = tk.Button(
        hp_frame,
        text="Apply",
        bg=ACCENT,
        fg="white",
        command=toggle_highpass
    )
    hp_button.pack(pady=5)


    # BANDPASS--------------------------------------------------
    bandpass_active = False

    bp_frame = tk.Frame(filter_container, bg=BG_FRAME)

    tk.Label(bp_frame, text="Bandpass Low Frequenzy [Hz]", bg=BG_FRAME, fg=FG_TEXT)\
        .pack(anchor="w")
    bp_low = tk.Entry(bp_frame)
    bp_low.insert(0, "300")
    bp_low.pack(fill="x")

    tk.Label(bp_frame, text="Bandpass High Frequenzy [Hz]", bg=BG_FRAME, fg=FG_TEXT)\
        .pack(anchor="w")
    bp_high = tk.Entry(bp_frame)
    bp_high.insert(0, "3000")
    bp_high.pack(fill="x")

    def toggle_bandpass():
        nonlocal bandpass_active
        bandpass_active = not bandpass_active

        bp_button.config(
            text="Applied" if bandpass_active else "Apply",
            bg="#2E8B57" if bandpass_active else ACCENT
        )

        if bandpass_active:
            print("Bandpass activated:", bp_low.get(), "-", bp_high.get())
        else:
            print("Bandpass deactivated")

    bp_button = tk.Button(
        bp_frame,
        text="Apply",
        bg=ACCENT,
        fg="white",
        command=toggle_bandpass
    )
    bp_button.pack(pady=5)


    # SINSIG Filter------------------------------------------------
    sinsig_active = False

    sin_frame = tk.Frame(filter_container, bg=BG_FRAME)

    def toggle_sinsig():
        nonlocal sinsig_active
        sinsig_active = not sinsig_active

        sin_button.config(
            text="Applied" if sinsig_active else "Apply",
            bg="#2E8B57" if sinsig_active else ACCENT
        )

        print("SinSig activated" if sinsig_active else "SinSig deactivated")
    sin_button = tk.Button(
        sin_frame,
        text="Apply",
        bg=ACCENT,
        fg="white",
        command=toggle_sinsig
    )
    sin_button.pack(pady=5)


    # EQUALIZER-------------------------------------------------
    eq_active = False

    eq_frame = tk.Frame(filter_container, bg=BG_FRAME)

    #Equalizer Frequencys
    eq_bands = [
        "31 Hz", "62 Hz", "125 Hz", "250 Hz", "500 Hz",
        "1 kHz", "2 kHz", "4 kHz", "8 kHz", "16 kHz"
    ]

    #Dictionary to hold EQ Gain and Lable Variables
    eq_gains = {}
    eq_labels = {}

    #Slider Container
    sliders_frame = tk.Frame(eq_frame, bg=BG_FRAME)
    sliders_frame.pack(fill="x", pady=5)

    #Band Frames with Sliders
    for band in eq_bands:
        band_frame = tk.Frame(
            sliders_frame,
            bg=BG_FRAME,
            width=38,
            height=260
        )
        band_frame.pack(side="left", padx=3)
        band_frame.pack_propagate(False)

        #Gain Variable
        gain_var = tk.DoubleVar(value=0.0)
        eq_gains[band] = gain_var

        #Gain Value Label
        value_label = tk.Label(
            band_frame,
            text="+0.0 dB",
            bg=BG_FRAME,
            fg=FG_TEXT,
            font=("Helvetica", 8, "bold")
        )
        value_label.pack()
        eq_labels[band] = value_label

        #Update Slider Value Label
        def update_value(val, label=value_label):
            val = float(val)
            label.config(
                text=f"{val:+.1f} dB",
                fg="#3A7CA5" if val >= 0 else "#C94C4C"
            )

        #Slider
        slider = tk.Scale(
            band_frame,
            from_=12,
            to=-12,
            resolution=0.1,
            orient="vertical",
            variable=gain_var,
            length=180,
            width=12,
            sliderlength=18,
            showvalue=False,
            command=update_value
        )
        slider.pack()

        #Double-Click to Reset Gain
        def reset_gain(event, var=gain_var, label=value_label):
            var.set(0.0)
            label.config(text="+0.0 dB", fg=FG_TEXT)

        slider.bind("<Double-Button-1>", reset_gain)

        #Band Label (Frequency)
        tk.Label(
            band_frame,
            text=band,
            bg=BG_FRAME,
            fg=FG_TEXT,
            font=("Helvetica", 8)
        ).pack()


    # Reset ALL EQ Bands Button
    def reset_all_eq():
        for band, var in eq_gains.items():
            var.set(0.0)
            eq_labels[band].config(text="+0.0 dB", fg=FG_TEXT)
            

    reset_button = tk.Button(
        eq_frame,
        text="Reset EQ",
        bg="#555555",
        fg="white",
        padx=6,
        pady=2,
        font=("Helvetica", 9),
        command=reset_all_eq
    )
    reset_button.pack(pady=(0, 6))


    # Apply / Toggle Button
    def toggle_eq():
        nonlocal eq_active
        eq_active = not eq_active

        eq_button.config(
            text="Applied" if eq_active else "Apply",
            bg="#2E8B57" if eq_active else ACCENT
        )

    eq_button = tk.Button(
        eq_frame,
        text="Apply",
        bg=ACCENT,
        fg="white",
        command=toggle_eq
    )
    eq_button.pack(pady=(8, 4))


    # Umschalten der sichtbaren Filter---------------------------------
    def update_filter_ui():
        for child in filter_container.winfo_children():
            child.pack_forget()

        selection = filter_var.get()

        if selection == "Low Pass":
            lp_frame.pack(fill="x")
        elif selection == "High Pass":
            hp_frame.pack(fill="x")
        elif selection == "Band Pass":
            bp_frame.pack(fill="x")
        elif selection == "SinSig":
            sin_frame.pack(fill="x")
        elif selection == "Equalizer":
            eq_frame.pack(fill="x")

    filter_cb.bind("<<ComboboxSelected>>", lambda e: update_filter_ui())
    update_filter_ui()

    return frame
