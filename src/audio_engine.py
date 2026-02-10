from .audio_player import AudioPlayer
from .bandpass import butter_bandpass_filter
from .spectral_gate import noise_profile, spectral_gate
from .bandpass import butter_bandpass_filter
from .equalizer import apply_eq


class AudioEngine:
    #Initialisierung
    def __init__(self):
        self.input_player = AudioPlayer()
        self.output_player = AudioPlayer()
        self.current_time = 0.0

        #Signal input
        self.input_signal = None
        self.samperate = None

        #Signal output
        self.output_signal = None

        #Bandpass Status
        self.bandpass_active = False
        self.bandpass_low = None
        self.bandpass_high = None

        #Spectral Gate Status
        self.spectral_gate_active = False
        self.noise_profile = None

        #Equalizer Status
        self.eq_active = False
        self.eq_xs = None       #Frequenzen (HZ)
        self.eq_ys = None       #Gain (dB)

        #Plot-Update Callback
        self.on_update_plots = None


    #Input laden
    def load_input(self, filepath):
        self.input_player.load(filepath)                #Player lädt die Audiodatei

        self.input_signal = self.input_player.data      #Rohdaten des Input-Signals speichern
        self.samplerate = self.input_player.samplerate  #Samplerate des Input-Signals speichern

        self.output_player.data = None                  #Output zurücksetzen

        #Debug-Ausgabe
#        print("=== AudioEngine.load_input ===")
#        print("Path:", filepath)
#        print("Signal shape:", self.input_signal.shape)
#        print("Samplerate:", self.samplerate)
#        print("--------------------------------")

        #Bilden des Output-Signals
        self.build_output_passthrough()                 #Output-Signal auf Input-Signal setzen (Passthrough)
        

    #Output laden
    def load_output(self, filepath):
        self.output_player.load(filepath)

    #Prüfen, ob Input-Signal geladen ist
    def has_output(self):
        return self.output_player.data is not None

    #Start der Wiedergabe des Input-Signals
    def play_input(self):
        self.output_player.pause()
        self.input_player.seek(self.current_time)
        self.input_player.play()

    #Start der Wiedergabe des Output-Signals
    def play_output(self):
        self.input_player.pause()
        self.output_player.seek(self.current_time)
        self.output_player.play()

    #Pause beider Player
    def pause_all(self):
        self.input_player.pause()
        self.output_player.pause()

    #Setzen der Wiedergabezeit
    def seek(self, seconds):
        self.current_time = seconds
        self.input_player.seek(seconds)
        self.output_player.seek(seconds)

    #Wiedergabezeit abrufen
    def get_active_time(self):
        if self.input_player.playing:
            return self.input_player.get_time()
        if self.output_player.playing:
            return self.output_player.get_time()
        return self.current_time
    
    #Speichern der Audiodatei
    def save_output(self, filepath):
        if self.output_player.data is None:
            print("No processed audio to save")
            return
        self.output_player.save_to_file(filepath)

    # Gesamtdauer abrufen (Output hat Priorität)
    def get_duration(self):
        if self.output_player.data is not None:
            return self.output_player.duration
        if self.input_player.data is not None:
            return self.input_player.duration
        return 0.0
    
    # Status abfragen
    def get_state(self):
        if self.input_player.playing:
            return "input_playing"
        if self.output_player.playing:
            return "output_playing"
        return "paused"
    
    #Audio durchgabe bei keinem aktiven Filter
    def build_output_passthrough(self):
        if self.input_signal is None:
            print("No input signal – cannot build output")
            return

        # 1) Signal kopieren (wichtig!)
        self.output_signal = self.input_signal.copy()

        # 2) Output-Player laden
        self.output_player.data = self.output_signal
        self.output_player.samplerate = self.samplerate
        self.output_player.position = 0
        self.output_player.duration = len(self.output_signal) / self.samplerate

        print("Output passthrough built")


    #Bandpass
    def set_bandpass(self, active: bool, low: float = None, high: float = None):
        self.bandpass_active = active

        if low is not None:
            self.bandpass_low = low
        if high is not None:
            self.bandpass_high = high

        print(
            f"Bandpass:",
            "ON" if active else "OFF",
            f"({self.bandpass_low} - {self.bandpass_high} Hz)"
        )

        self.apply_processing()


    #Spectral Gate
    def set_spectral_gate(self, active: bool):
        self.spectral_gate_active = active

        if active and self.noise_profile is None:
            print("No noise profile available yet")

        self.apply_processing()


    #Equalizer
    def set_equalizer(self, active: bool, xs=None, ys=None):
        self.eq_active = active

        if xs is not None and ys is not None:
            self.eq_xs = xs
            self.eq_ys = ys

        print("Equalizer:", "ON" if active else "OFF")

        self.apply_processing()


    #Audio Prozessing anwenden (hier werden die Filter angewendet)
    def apply_processing(self):
        if self.input_signal is None:
            print("No input signal – cannot apply processing")
            return
        
        sig = self.input_signal.copy()

        #Bandpass-Filter anwenden
        if self.bandpass_active:
            sig = butter_bandpass_filter(
                sig,
                self.bandpass_low,
                self.bandpass_high,
                self.samplerate
            )
        #Spectral Gate anwenden
        if self.spectral_gate_active:

            #Sicherheitscheck
            if sig is None or len(sig) < 4096:
                print("Signal too short for spectral gate")
                self.output_signal = sig
                return

            # Noise-Profil einmalig berechnen
            if self.noise_profile is None:
                _, self.noise_profile = noise_profile(
                    sig,
                    self.samplerate
                )

            sig = spectral_gate(
                sig,
                self.samplerate,
                self.noise_profile
                )

        #Equalizer anwenden
        if self.eq_active and self.eq_xs is not None and self.eq_ys is not None:
            sig = apply_eq(
                sig,
                self.samplerate,
                self.eq_xs,
                self.eq_ys
            )


        #Output-Signal aktualisieren
        self.output_signal = sig

        self.output_player.data = sig
        self.output_player.samplerate = self.samplerate
        self.output_player.position = 0
        self.output_player.duration = len(sig) / self.samplerate


        if self.on_output_updated:
            self.on_output_updated()



