from numpy.typing import NDArray
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import librosa
import librosa.display
from scipy.signal import stft



# ------------------ Plot-Funktionen: jetzt "subplot-fähig" ------------------

def plot_AudioSig(sig: NDArray[np.floating], sr, ax=None, title="Waveform (librosa)", max_points=10000):
    if ax is None:
        ax = plt.gca()

    # librosa zeichnet auf die "current axes" – daher setzen wir ax aktiv
    plt.sca(ax)
    librosa.display.waveshow(sig, sr=sr, max_points=max_points, axis='time')

    ax.set_title(title)
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Amplitude")
    ax.grid(True)


def plot_AudioSig_2(sig, sr, ax=None, title="Waveform (matplotlib)"):
    if ax is None:
        ax = plt.gca()

    t = np.arange(len(sig)) / sr
    ax.plot(t, sig)
    ax.set_title(title)
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Amplitude")
    ax.set_ylim(-3, 2.2)
    ax.grid(True)


def plot_fft(sig, sr, ax=None, db=False, normResult=False, title="FFT Spectrum"):
    if ax is None:
        ax = plt.gca()

    N = len(sig)

    # FFT
    X = np.fft.fft(sig)

    # Frequenzachse
    freqs = np.fft.fftfreq(N, d=1/sr)

    # Nur positive Frequenzen (einseitig)
    pos = freqs >= 0
    freqs_pos = freqs[pos]
    #mag = np.abs(X[pos]) #* 2 / N   # Amplituden-Normierung (einseitig)

    if normResult:
        mag = np.abs(X[pos]) * 2 / N
    else:
        mag = np.abs(X[pos])


    if db:
        #mag = 20 * np.log10(np.maximum(mag, 1e-12))  # dB, avoid log(0)
        mag = 20*np.log10(mag)

    ax.plot(freqs_pos, mag)
    ax.set_title(title + (" (dB)" if db else ""))
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude (dB)" if db else "Magnitude")
    ax.set_xlim(0, sr/2)
    #ax.set_xlim(0, 20)
    ax.grid(True)


def plot_spectogram(sig, sr, ax=None, title="Mel Spectrogram", n_mels=64):
    if ax is None:
        ax = plt.gca()

    S1 = librosa.feature.melspectrogram(y=sig, sr=sr, n_mels=n_mels)
    D1 = librosa.power_to_db(S1, ref=np.max)

    # specshow nutzt auch current axes → ax setzen
    plt.sca(ax)
    img = librosa.display.specshow(D1, sr=sr, x_axis='time', y_axis='mel')
    ax.set_title(title)

    # Optional: Colorbar pro Achse (macht das Layout etwas voller)
    plt.colorbar(img, ax=ax, format="%+2.0f dB")


def plot_spectogram_2(sig, sr, ax=None, title="STFT Spectrogram", n_mels=64,
                    n_fft=2048, hop_length=512, window="hann",
                    fmax=None, db=False, db_range=80, ref="max"):
    """
    STFT-Spektrogramm (SciPy) statt Mel-Spektrogramm (librosa).

    db:
      - True  -> dB Anzeige, typischerweise 0 bis -db_range (z.B. -80 dB)
      - False -> linear Magnitude

    ref (nur relevant wenn db=True):
      - "max": 0 dB entspricht dem Maximum im Spektrum
      - Zahl: 0 dB entspricht diesem Referenzwert (z.B. 1.0)
    """
    if ax is None:
        ax = plt.gca()

    noverlap = n_fft - hop_length

    # STFT berechnen (onesided)
    f, t, Z = stft(
        sig, fs=sr, window=window,
        nperseg=n_fft, noverlap=noverlap, nfft=n_fft,
        boundary="zeros", padded=True, return_onesided=True
    )

    mag = np.abs(Z)  # linear magnitude

    # Frequenzbereich begrenzen (optional)
    if fmax is not None:
        idx = f <= fmax
        f = f[idx]
        mag = mag[idx, :]

    # Anzeige: dB oder linear
    if db:
        eps = 1e-12

        # Referenz bestimmen
        if ref == "max":
            ref_val = np.max(mag) + eps      # 0 dB = Maximum
        else:
            ref_val = float(ref)             # 0 dB = ref

        data = 20 * np.log10((mag + eps) / ref_val)  # dB

        # Clip auf [-db_range, 0]
        data = np.clip(data, -db_range, 0.0)

        img = ax.pcolormesh(t, f, data, shading="gouraud")
        ax.set_ylabel("Frequency [Hz]")
        ax.set_xlabel("Time [s]")
        ax.set_title(f"{title} (dB)")
        plt.colorbar(img, ax=ax, format="%+2.0f dB")
    else:
        data = mag  # linear
        img = ax.pcolormesh(t, f, data, shading="gouraud")
        ax.set_ylabel("Frequency [Hz]")
        ax.set_xlabel("Time [s]")
        ax.set_title(f"{title} (linear)")
        plt.colorbar(img, ax=ax)

    return f, t, Z  # optional praktisch, falls du später noch etwas damit machen willst


#-------------------------Noice Floor ------------------------------------------------------
def plot_noise_profile(f, noise_profile, ax=None, title="Noise floor (linear magnitude)", xlim=None, logy=False):
    """
    Args:
        f: freq bins | ndarray
        noise_profile: typ freq for each freq bin| ndarray
    """
    
    if ax is None:
        ax = plt.gca()
    
    ax.plot(f, noise_profile)
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("Magnitude (linear)")
    ax.set_title(title)
    if xlim is not None:
        ax.set_xlim(xlim)
    if logy:
        ax.set_yscale("log")
    ax.grid(True)


# ----------------------- Master-Plot-Funktion ---------------------------------------------

def plot_sig_fft_noiseProfile(sig1, sr1, sig_noice, sr_noice, f, noise_profile, sig2, sr2):
 
  
    fig, axs = plt.subplots(2, 3, figsize=(16, 8))
    plot_AudioSig_2(sig1, sr1, ax=axs[0, 0], title="Sig 1 (time)")
    plot_fft(sig1, sr1, ax=axs[1, 0], db=False, normResult=True, title="Sig 1 (FFT)")

    plot_AudioSig_2(sig_noice, sr_noice, ax=axs[0, 1], title="noise (time)")
    plot_noise_profile(f, noise_profile, ax=axs[1, 1], title="Noise profile (linear magnitude)", xlim=None, logy=False)

    plot_AudioSig_2(sig2, sr2, ax=axs[0, 2], title="Sig 3 (time)")
    plot_fft(sig2, sr2, ax=axs[1, 2], db=False, normResult=True, title="Sig 3 (FFT)")

    fig.tight_layout()
    plt.show()



def plot_sig_fft_spec_noiseProfile(sig1, sr1, sig_noice, sr_noice, f, noise_profile, sig2, sr2, sig3, sr3):
 
  
    fig, axs = plt.subplots(3, 4, figsize=(16, 8))

    plot_AudioSig_2(sig1, sr1, ax=axs[0, 0], title="Sig (time)")
    plot_fft(sig1, sr1, ax=axs[1, 0], db=False, normResult=True, title="Sig (FFT)")
    plot_spectogram(sig1, sr1, ax=axs[2, 0], title="Sig (Spec)")

    plot_AudioSig_2(sig_noice, sr_noice, ax=axs[0, 1], title="Noise (time)")
    plot_noise_profile(f, noise_profile, ax=axs[1, 1], title="Noise profile (linear magnitude)", xlim=None, logy=False)
    plot_spectogram(sig_noice, sr_noice, ax=axs[2, 1], title="Noise (Spec)")

    plot_AudioSig_2(sig2, sr2, ax=axs[0, 2], title="Sig + Noise (time)")
    plot_fft(sig2, sr2, ax=axs[1, 2], db=False, normResult=True, title="Sig + Noise (FFT)")
    plot_spectogram(sig2, sr1, ax=axs[2, 2], title="Sig + Noise (Spec)")
    
    plot_AudioSig_2(sig3, sr3, ax=axs[0, 3], title="Sig Denoised (time)")
    plot_fft(sig3, sr3, ax=axs[1, 3], db=False, normResult=True, title="Sig Denoised (FFT)")
    plot_spectogram(sig3, sr3, ax=axs[2, 3], title="Sig Denoised (Spec)")

    fig.tight_layout()
    plt.show()


def plot_sig_fft_spec_3x(sig1, sr1, sig2, sr2, sig3, sr3):
    """
    Zeigt mehrere Plots in EINEM Fenster.
    - sig: clean signal
    - noisy: optional noisy signal
    """
  
    fig, axs = plt.subplots(3, 3, figsize=(16, 8))
    plot_AudioSig_2(sig1, sr1, ax=axs[0, 0], title="Sig 1 (time)")
    plot_fft(sig1, sr1, ax=axs[1, 0], db=False, normResult=True, title="Sig 1 (FFT)")
    plot_spectogram(sig1, sr1, ax=axs[2, 0], title="Spec 1 (time)")

    plot_AudioSig_2(sig2, sr2, ax=axs[0, 1], title="Sig 2 (time)")
    plot_fft(sig2, sr2, ax=axs[1, 1], db=False, normResult=True, title="Sig 2 (FFT)")
    plot_spectogram(sig2, sr2, ax=axs[2, 1], title="Spec 2 (time)")

    plot_AudioSig_2(sig3, sr3, ax=axs[0, 2], title="Sig 3 (time)")
    plot_fft(sig3, sr3, ax=axs[1, 2], db=False, normResult=True, title="Sig 3 (FFT)")
    plot_spectogram(sig3, sr3, ax=axs[2, 2], title="Spec 3 (time)")

    fig.tight_layout()
    plt.show()


def plot_sig_fft_spec_2x(sig1, sr1, sig2, sr2):
    """
    Zeigt mehrere Plots in EINEM Fenster.
    - sig: clean signal
    - noisy: optional noisy signal
    """
  
    fig, axs = plt.subplots(3, 2, figsize=(16, 8))
    plot_AudioSig_2(sig1, sr1, ax=axs[0, 0], title="Sig 1 (time)")
    plot_fft(sig1, sr1, ax=axs[1, 0], db=False, normResult=True, title="Sig 1 (FFT)")
    plot_spectogram(sig1, sr1, ax=axs[2, 0], title="Signal (time)")

    plot_AudioSig_2(sig2, sr2, ax=axs[0, 1], title="Sig 2 (time)")
    plot_fft(sig2, sr2, ax=axs[1, 1], db=False, normResult=True, title="Sig 2 (FFT)")
    plot_spectogram(sig2, sr2, ax=axs[2, 1], title="Signal (time)")


    fig.tight_layout()
    plt.show()


def plot_sig_fft_3x(sig1, sr1, sig2, sr2, sig3, sr3, db=False, normResult=True):
    """
    Zeigt mehrere Plots in EINEM Fenster.
    - sig: clean signal
    - noisy: optional noisy signal
    """
  
    fig, axs = plt.subplots(2, 3, figsize=(16, 8))
    plot_AudioSig_2(sig1, sr1, ax=axs[0, 0], title="Sig 1 (time)")
    plot_fft(sig1, sr1, ax=axs[1, 0], db=db, normResult=normResult, title="Sig 1 (FFT)")

    plot_AudioSig_2(sig2, sr2, ax=axs[0, 1], title="Sig 2 (time)")
    plot_fft(sig2, sr2, ax=axs[1, 1], db=db, normResult=normResult, title="Sig 2 (FFT)")

    plot_AudioSig_2(sig3, sr3, ax=axs[0, 2], title="Sig 3 (time)")
    plot_fft(sig3, sr3, ax=axs[1, 2], db=db, normResult=normResult, title="Sig 3 (FFT)")

    fig.tight_layout()
    plt.show()


def plot_sig_fft_2x(sig1, sr1, sig2, sr2):
    """
    Zeigt mehrere Plots in EINEM Fenster.
    - sig: clean signal
    - noisy: optional noisy signal
    """
  
    fig, axs = plt.subplots(2, 2, figsize=(16, 8))
    plot_AudioSig_2(sig1, sr1, ax=axs[0, 0], title="Sig 1 (time)")
    plot_fft(sig1, sr1, ax=axs[1, 0], db=False, normResult=True, title="Sig 1 (FFT)")

    plot_AudioSig_2(sig2, sr2, ax=axs[0, 1], title="Sig 2 (time)")
    plot_fft(sig2, sr2, ax=axs[1, 1], db=False, normResult=True, title="Sig 2 (FFT)")

    fig.tight_layout()
    plt.show()


def plot_sig_fft(sig, sr):
    fig, axs = plt.subplots(2, 1, figsize=(16, 8))

    plot_AudioSig_2(sig, sr, ax=axs[0], title="Signal (time)")
    plot_fft(sig, sr, ax=axs[1], db=False, normResult=False, title="FFT (signal)")

    fig.tight_layout()
    plt.show()


def plot_only_sig(sig, sr):
    fig, ax = plt.subplots(1, 1, figsize=(16, 4))
    plot_AudioSig_2(sig, sr, ax=ax, title="Signal (time)")
    fig.tight_layout()
    plt.show()


def plot_only_spec(sig, sr):
    fig, ax = plt.subplots(1, 1, figsize=(16, 4))
    plot_spectogram(sig, sr, ax=ax, title="Signal (time)")
    fig.tight_layout()
    plt.show()




#Waveform-Plot
def plot_waveform(parent, signal, samplerate):
    """
    Erstellt einen Waveform-Plot in einem Tkinter-Frame
    """
    fig, ax = plt.subplots(figsize=(5, 2), dpi=100)
    fig.patch.set_facecolor("#000000")
    ax.set_facecolor("#000000")

    if signal.ndim > 1:
        signal = signal[:, 0]  # nur linker Kanal

    t = np.arange(len(signal)) / samplerate
    ax.plot(t, signal, color="white", linewidth=0.6)

    ax.set_xlabel("Time [s]", color="white")
    ax.set_ylabel("Amplitude", color="white")
    ax.tick_params(colors="white")
    ax.spines[:].set_color("white")

    #Plotgröße
    fig.subplots_adjust(
        left=0.2,
        right=0.93,
        top=0.91,
        bottom=0.3
    )

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="x", expand=True)

    return canvas

#Specrum Plot
def plot_spectrum(parent, signal, samplerate):
    """
    Erstellt ein Frequenzspektrum (FFT) in einem Tkinter-Frame
    """
    fig, ax = plt.subplots(figsize=(5, 2), dpi=100)
    fig.patch.set_facecolor("#000000")
    ax.set_facecolor("#000000")

    if signal.ndim > 1:
        signal = signal[:, 0]

    N = len(signal)
    fft = np.abs(np.fft.rfft(signal))
    freqs = np.fft.rfftfreq(N, 1 / samplerate)

    ax.plot(freqs, fft, color="white", linewidth=0.6)
    ax.set_xlim(0, samplerate / 2)

    ax.set_xlabel("Frequency [Hz]", color="white")
    ax.set_ylabel("Magnitude", color="white")
    ax.tick_params(colors="white")
    ax.spines[:].set_color("white")

    #Plotgröße
    fig.subplots_adjust(
        left=0.2,
        right=0.93,
        top=0.91,
        bottom=0.3
    )

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="x", expand=True)

    return canvas

