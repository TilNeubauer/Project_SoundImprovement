from pathlib import Path
import librosa
import numpy as np 

import soundfile as sf

from plot import plot_sig_fft_2x, plot_sig_fft, plot_only_spec, plot_sig_fft_spec_2x, plot_sig_fft_3x, plot_sig_fft_spec_3x, plot_sig_fft_noiseProfile, plot_sig_fft_spec_noiseProfile, plot_only_sig
from sinSig import gen_sin_sig, add_noise, add_sig
from filter import denoise_fft
from spectral_gate import noise_profile, spectral_gate
from bandpass import butter_bandpass_filter
from equalizer import eq_fkt, apply_eq



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
    #"""
    #sig1, sr1 = librosa.load(audio_path_1)
    sig_orig, sr_orig = librosa.load(audio_path_orig)
    sig_orig = sig_orig[:len(sig_orig)//5]
    #plot_sig_fft_spec_2x(sig1, sr1, sig_orig, sr_orig)

    sig_vinyl_noice, sr_vinyl_noice = librosa.load(vinyl_noice_path)
    sig_vinyl_noice = sig_vinyl_noice * 3
    #plot_sig_fft(sig_vinyl_noice, sr_vinyl_noice)

    sig = add_mismatch(sig_orig, sig_vinyl_noice)

    #"""
    #n_fft = 2048
    #hop = 512

    #Bandpass 
    y_bandpass = butter_bandpass_filter(sig, 60, 6000, sr_orig)

    
    #denoise mit spectral_gate
    f, noise_floor = noise_profile(sig_vinyl_noice, sr_vinyl_noice)            # Noise-Profil lernen
    y_clean = spectral_gate(sig, sr_orig, noise_floor)             # Gate anwenden

    xs, ys = eq_fkt(e32=0, e64=0, e125=0, e250=0, e500=0, e1k=0, e2k=0, e4k=0, e8k=0, e16k=0)
    y_eq = apply_eq(sig, sr_orig, xs, ys)

    #plot_sig_fft_noiseProfile(
    #                            sig1 = sig, 
    #                            sr1 = sr_orig, 
    #                            sig_noice = sig_vinyl_noice, 
    #                            sr_noice = sr_vinyl_noice, 
    #                            f = f, 
    #                            noise_profile = noise_floor, 
    #                            sig2 = y_clean, 
    #                            sr2 = sr_orig
    #                            )


    #plot_sig_fft_spec_noiseProfile(
    #                            sig1 = sig_orig, 
    #                            sr1 = sr_orig, 
    #                            sig_noice = sig_vinyl_noice, 
    #                            sr_noice = sr_vinyl_noice, 
    #                            f = f, 
    #                            noise_profile = noise_floor, 
    #                            sig2 = sig, 
    #                            sr2 = sr_orig,
    #                            sig3 = y_clean,
    #                            sr3 = sr_orig
    #                            )


    #plot_sig_fft_3x(sig, sr_orig, sig_vinyl_noice, sr_vinyl_noice, y_clean, sr_orig)

    #plot_sig_fft_spec_3x(sig, sr_orig, sig_vinyl_noice, sr_vinyl_noice, y_clean, sr_orig)

    #plot_sig_fft_2x(sig, sr_orig, y_bandpass, sr_orig)
    plot_sig_fft_2x(sig, sr_orig, y_eq, sr_orig)


    #sf.write("audio_test.wav", sig, sr_orig)
    #plot_sig_fft(sig, sr_orig)
    
    #noise_sig = denoise_fft(sig)
    #denoice_sig = sig - noise_sig

    sf.write("Sounds_out/orig_noice.wav", sig, sr_orig)

    #sf.write("Sounds_out/denoice.wav", y_clean, sr_orig)
    #sf.write("Sounds_out/bandpass.wav", y_bandpass, sr_orig)
    sf.write("Sounds_out/eq.wav", y_eq, sr_orig)
    #sf.write("Sounds_out/noice.wav", noise_sig, sr_orig)

    #"""

"""
    sr = 1000
    sig10 = gen_sin_sig(1, 10, sr)
    #noisy = add_noise(sig, 0.2)

    sig20 = add_sig(sig10,20, sr)
    #sig3 = filter_freq(sig2, freq=2)
    #sig2 = add_sig(sig2,3.15, sr)
    #sig2 = add_sig(sig2,50, sr)
    #sig_noisy = add_noise(sig2, 1)
    #sig_denoise = denoise_fft(sig_noisy)

    #noice = sig_noisy - sig_denoise

    #plot_only_sig(sig2, sr)

    sig_butter = butter_bandpass_filter(sig20,3,15,sr)

    


    plot_sig_fft_3x(sig10, sr, sig20, sr, sig_butter, sr)
    #plot_sig_fft_3x(sig_noisy, sr, sig_denoise, sr, noice, sr)
    #plot_sig_fft(sig, sr)
"""