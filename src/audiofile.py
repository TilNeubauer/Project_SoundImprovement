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

def plot_spectogram(sig, sr):
    
    S1 = librosa.feature.melspectrogram(y=sig, sr=sr, n_mels=64)
    D1 = librosa.power_to_db(S1, ref=np.max)
    librosa.display.specshow(D1, x_axis='time', y_axis='mel')
    plt.show()


#-------------------------------------------------------------------------------------------------------------------

# Path to src/main.py
BASE_DIR = Path(__file__).resolve().parent

# Go up to project root, then into Sounds -> filename 
# Audio file should be Sounds
audio_path_1 = BASE_DIR.parent / "Sounds" / "RsPaintItBlack_Home.mp3"
audio_path_2 = BASE_DIR.parent / "Sounds" / "RsPaintItBlack_orig.mp3"


# load Audiofile
#   sig: Audio sig | 1D np array
#   sr: sample rate of audio file 
sig1, sr1 = librosa.load(audio_path_1)
sig2, sr2 = librosa.load(audio_path_2)


plot_AudioSig(sig1, sr1)
plot_AudioSig(sig2, sr2)

#plot_spectogram(sig1, sr1)
#plot_spectogram(sig2, sr2)

#print(type(sig))
