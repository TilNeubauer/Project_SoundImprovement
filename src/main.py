from pathlib import Path
import librosa

from plot import plot_sig_fft_2x, plot_sig_fft
from sinSig import gen_sin_sig, add_noise


if __name__ == "__main__":
    # Path to src/main.py
    BASE_DIR = Path(__file__).resolve().parent
    """
    Go up to project root, then into Sounds -> filename 
    Audio file should be in folder Sounds
    """
    audio_path_1 = BASE_DIR.parent / "Sounds" / "RsPaintItBlack_Home.mp3"
    audio_path_2 = BASE_DIR.parent / "Sounds" / "RsPaintItBlack_orig.mp3"

    """
    load Audiofile
    sig: Audio sig | 1D np array
    sr: sample rate of audio file 
    """
    sig1, sr1 = librosa.load(audio_path_1)
    sig2, sr2 = librosa.load(audio_path_2)

    plot_sig_fft_2x(sig1, sr1, sig2, sr2)
    
    #plot_sig_fft(sig1, sr1)
    #plot_sig_fft(sig2, sr2)



    sr = 10000
    sig = gen_sin_sig(1, 50, sr)
    noisy = add_noise(sig, 0.2)

    #plot_sig_fft_2x(sig, sr, noisy, sr)
    #plot_sig_fft(sig, sr)