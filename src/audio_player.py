import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment
import numpy as np


class AudioPlayer:
    #Initialisierung
    def __init__(self):
        self.data = None
        self.samplerate = None
        self.position = 0
        self.stream = None
        self.playing = False

    #Audio-Datei laden
    def load(self, filepath):
        if filepath.lower().endswith(".mp3"):
            audio = AudioSegment.from_mp3(filepath)

            self.samplerate = audio.frame_rate
            samples = np.array(audio.get_array_of_samples())

            if audio.channels == 2:
                samples = samples.reshape((-1, 2))
            else:
                samples = samples.reshape((-1, 1))

            # Normierung auf [-1, 1] für sounddevice
            self.data = samples.astype(np.float32) / (2 ** 15)

        else:
            # WAV / FLAC
            self.data, self.samplerate = sf.read(filepath, always_2d=True)

        self.position = 0
        self.duration = len(self.data) / self.samplerate

    #Callback-Funktion für sounddevice
    def _callback(self, outdata, frames, time, status):
        if not self.playing or self.data is None:
            outdata[:] = 0
            return

        end = self.position + frames
        chunk = self.data[self.position:end]

        if len(chunk) < frames:
            outdata[:len(chunk)] = chunk
            outdata[len(chunk):] = 0
            self.pause()
        else:
            outdata[:] = chunk

        self.position = end

    #Start der Wiedergabe
    def play(self):
        if self.data is None:
            print("No audio loaded – play ignored")
            return

        if self.stream is None:
            self.stream = sd.OutputStream(
                samplerate=self.samplerate,
                channels=self.data.shape[1],
                callback=self._callback
            )
            self.stream.start()

        self.playing = True

    #Pause der Wiedergabe
    def pause(self):
        self.playing = False

    #Position auf bestimmte Zeit setzen
    def seek(self, seconds):
        if self.data is None:
            return
        self.position = int(seconds * self.samplerate)
        self.position = max(0, min(self.position, len(self.data)))

    #Wiedergabezeit abrufen
    def get_time(self):
        if self.samplerate is None:
            return 0.0
        return self.position / self.samplerate
    
    #Speichern der Audiodatei
    def save_to_file(self, filepath):
        if self.data is None:
            print("No audio data to save")
            return

        sf.write(filepath, self.data, self.samplerate)

    

