from numpy.typing import NDArray
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display



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
        mag = 20 * np.log10(np.maximum(mag, 1e-12))  # dB, avoid log(0)

    ax.plot(freqs_pos, mag)
    ax.set_title(title + (" (dB)" if db else ""))
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude (dB)" if db else "Magnitude")
    ax.set_xlim(0, sr/2)
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


# ----------------------- Master-Plot-Funktion -----------------------------

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