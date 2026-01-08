from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
import librosa



def plot_AudioSig(sig: NDArray[np.floating], sr):
    # Plot the waveform with customization
    plt.figure(figsize=(16, 6))
    librosa.display.waveshow(sig, sr=sr, max_points=10000, axis='time', color='green')
    plt.title('Custom Waveform')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.show()


# Path to src/main.py
BASE_DIR = Path(__file__).resolve().parent

# Go up to project root, then into Sounds -> filename 
# Audio file should be Sounds
audio_path = BASE_DIR.parent / "Sounds" / "RsPaintItBlack_Home.mp3"


# load Audiofile
#   sig: Audio sig | 1D np array
#   sr: sample rate of audio file 
sig, sr = librosa.load(audio_path)

plot_AudioSig(sig, sr)

#print(type(sig))
