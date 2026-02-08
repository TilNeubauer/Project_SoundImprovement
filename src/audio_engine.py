from .audio_player import AudioPlayer


class AudioEngine:
    #Initialisierung
    def __init__(self):
        self.input_player = AudioPlayer()
        self.output_player = AudioPlayer()
        self.current_time = 0.0

        self.input_signal = None
        self.samperate = None

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



