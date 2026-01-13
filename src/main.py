from pathlib import Path
import librosa
import numpy as np 

import soundfile as sf

from plot import plot_sig_fft_2x, plot_sig_fft, plot_only_spec, plot_sig_fft_spec_2x, plot_sig_fft_3x, plot_sig_fft_spec_3x
from sinSig import gen_sin_sig, add_noise, add_sig
from filter import denoise_fft

def add_mismatch(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a = np.asarray(a)
    b = np.asarray(b)

    # Ergebnis = Kopie vom längeren Array
    if a.size >= b.size:
        out = a.copy()
        out[:b.size] += b
    else:
        out = b.copy()
        out[:a.size] += a

    return out

if __name__ == "__main__":
    # Path to src/main.py
    BASE_DIR = Path(__file__).resolve().parent
    """
    Go up to project root, then into Sounds -> filename 
    Audio file should be in folder Sounds
    """
    audio_path_1 = BASE_DIR.parent / "Sounds" / "RsPaintItBlack_Home.mp3"
    audio_path_orig = BASE_DIR.parent / "Sounds" / "RsPaintItBlack_orig.mp3"
    vinyl_noice_path = BASE_DIR.parent / "Sounds" / "static-vinyl-noise-fx.wav"

    """
    load Audiofile
    sig: Audio sig | 1D np array
    sr: sample rate of audio file 
    """
    #sig1, sr1 = librosa.load(audio_path_1)
    sig_orig, sr_orig = librosa.load(audio_path_orig)
    #print(f'{sr_orig = }')
    #plot_sig_fft_spec_2x(sig1, sr1, sig_orig, sr_orig)

    sig_vinyl_noice, sr_vinyl_noice = librosa.load(vinyl_noice_path)
    #print(f'{sr_vinyl_noice = }')
    #plot_sig_fft(sig_vinyl_noice, sr_vinyl_noice)

    sig = add_mismatch(sig_orig, sig_vinyl_noice*3)

    #sf.write("audio_test.wav", sig, sr_orig)
    #plot_sig_fft(sig, sr_vinyl_noice)

    #plot_sig_fft(sig1, sr1)
    noise_sig = denoise_fft(sig)
    denoice_sig = sig - noise_sig
    #noice_sig = noice_sig * 2
    #sf.write("audio_test.wav", denoise_sig, sr1)
    sf.write("orig_noice.wav", sig, sr_orig)
    sf.write("denoice.wav", denoice_sig, sr_orig)
    sf.write("noice.wav", noise_sig, sr_orig)




    #plot_sig_fft(sig2, sr2)
    plot_sig_fft_spec_3x(sig, sr_orig, denoice_sig, sr_orig, noise_sig, sr_orig)
    #plot_sig_fft_spec_2x(sig1, sr1, noice_sig, sr_orig)
    #plot_only_spec(sig1, sr1)

"""
    sr = 10000
    sig = gen_sin_sig(1, 2, sr)
    #noisy = add_noise(sig, 0.2)

    sig2 = add_sig(sig,10, sr)
    sig2 = add_sig(sig2,3.15, sr)
    sig2 = add_sig(sig2,50, sr)
    sig_noisy = add_noise(sig2, 1)
    sig_denoise = denoise_fft(sig_noisy)

    noice = sig_noisy - sig_denoise

    #plot_sig_fft_2x(noisy, sr, sig_denoise, sr)
    #plot_sig_fft_3x(sig_noisy, sr, sig_denoise, sr, noice, sr)
    #plot_sig_fft(sig, sr)
"""