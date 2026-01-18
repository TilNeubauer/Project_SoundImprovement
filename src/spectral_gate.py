import numpy as np                          # NumPy für Arrays, Mathe, Quantile, Broadcasting
from scipy.signal import stft, istft        # SciPy STFT/ISTFT (Short-Time Fourier Transform)


def _smooth_along_axis(A, k, axis):
    """
    Glättet ein 2D-Array A mit einem Moving-Average (Fensterbreite k)
    entlang einer Achse (axis=0 Frequenz, axis=1 Zeit).
    Das reduziert "musical noise" (zirpende Artefakte).
    """
    if k <= 1:                              # Wenn k=1 (oder kleiner), keine Glättung nötig
        return A

    kernel = np.ones(k, dtype=float) / k    # Moving-average Kernel: [1/k, 1/k, ...] Länge k

    def conv1d(v):
        pad = k // 2                        # Halbe Fensterbreite für symmetrisches Padding
        vp = np.pad(v, (pad, pad), mode="edge")  # Padding mit Randwerten (stabiler als 0-padding)
        return np.convolve(vp, kernel, mode="valid")  # Faltung -> gleiche Länge wie Original

    # Wendet conv1d auf jede 1D-"Zeile" entlang der gewählten Achse an
    return np.apply_along_axis(conv1d, axis, A)


def noise_profile(noise, sr, n_fft=2048, hop_length=512, percentile=0.90, window="hann"):
    """
    Lernt ein Noise-Profil aus einem reinen Rauschsignal (oder Noise-Abschnitt).
    Ergebnis: noise_floor (pro Frequenz-Bin ein typischer Magnitude-Wert).

    percentile=0.90 bedeutet:
    pro Frequenz-Bin nehmen wir das 90%-Quantil der Rausch-Magnituden über alle Frames.
    """
    noverlap = n_fft - hop_length            # Overlap = Fensterlänge - Hop; z.B. 2048-512 = 1536

    """
    STFT vom Noise berechnen:
        Doku.: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.stft.html
    
    Returns:
        f: Frequenzachsenwerte (Hz) | ndarray
        t: Zeitachsenwerte (s) | ndarray
        Z: komplexe STFT-Matrix [freq_bins, frames/Zeitfenster] | ndarray
    """
    f, t, Z = stft(
        noise,                               # input sig: -> rauschem 
        # noch checken ob fs == sr von librosa
        fs=sr,                               # Sampling frequency of the x time 
        window=window,                       # window fkt: 'hnn' -> https://www.audiolabs-erlangen.de/resources/MIR/FMP/C2/C2_STFT-Window.html
        nperseg=n_fft,                       # Fensterlänge in Samples (Segmentlänge)
        noverlap=noverlap,                   # Number of points to overlap between segments
        nfft=n_fft,                          # FFT-Länge (meist = nperseg);<nfft=x^2> dann effizient; für musik <nfft = 2048> 
        boundary="zeros",                    # Am Rand mit Nullen auffüllen (damit STFT sauber startet/endet)
        padded=True,                         
        return_onesided=True                 # If True, return a one-sided spectrum for real data.
    )

    #print(f"{Z = }")
    #print(f"{len(t) = }")
    #print(f"{len(f) = }") 


    mag = np.abs(Z)                          # Magnitude (Betrag) der komplexen STFT: "Lautstärke" pro Bin
    #print(f"{mag = }")

    """
    np.quantile: median quwivalent nit immer 50%
    Args: 
        arr: Input data array.
        q: Quantile(s) to compute (range: 0 to 1): 0.5 == median 
        axis: axis=1: über alles Zeitframes für jeden freq-Bin
    Returns:
        ndarray:
        Interpretation: 
            noise_floor[10] = 0.03 -> im Rauschsignal ist Frequenz-Bin 10 in 90% der Frames ≤ 0.03 stark.
    """
    noise_floor = np.quantile(mag, percentile, axis=1)
    #print(f"{len(noise_floor) = }")

    return f, noise_floor              # Rückgabe: typisches Rauschniveau pro Frequenz-Bin


def spectral_gate(
    noisy, sr, noise_floor,
    n_fft=2048, hop_length=512, window="hann",
    threshold_db=6.0, reduction_db=12.0,
    smooth_bins=5, smooth_frames=3
):
    """
    Entfernt/Reduziert Rauschen aus 'noisy' mithilfe eines Noise-Floors.

    Idee:
    - Wir berechnen STFT von noisy.
    - Für jedes Zeit/Frequenz-Bin vergleichen wir Magnitude mit noise_floor.
    - Wenn Magnitude "nah am Rauschen" liegt -> absenken (z.B. -12 dB).
    - Glätten der Gains reduziert Artefakte.

    threshold_db:
      Wie viel über noise_floor noch als Noise gilt (6 dB ≈ Faktor 2).
    reduction_db:
      Wie stark die als Noise erkannten Bereiche abgesenkt werden (12 dB ≈ Faktor 0.25).
    """
    noverlap = n_fft - hop_length            # Gleiches Overlap wie beim Noise-Profil

    # STFT vom verrauschten Signal berechnen
    f, t, Z = stft(
        noisy,                               # input sig: -> lied mit rauschen
        fs=sr,                               # Sampling frequency of the x time 
        window=window,                       # window fkt: 'hnn' -> https://www.audiolabs-erlangen.de/resources/MIR/FMP/C2/C2_STFT-Window.html
        nperseg=n_fft,                       # Fensterlänge in Samples (Segmentlänge)
        noverlap=noverlap,                   # Number of points to overlap between segments
        nfft=n_fft,                          # FFT-Länge (meist = nperseg);<nfft=x^2> dann effizient; für musik <nfft = 2048> 
        boundary="zeros",                    # Am Rand mit Nullen auffüllen (damit STFT sauber startet/endet)
        padded=True,                                                 
        return_onesided=True                 # If True, return a one-sided spectrum for real data.
    )

    mag = np.abs(Z)                          # Magnitude: wie stark ist jede Frequenz im jeweiligen Frame
    phase = np.exp(1j * np.angle(Z))         # Phase separat speichern (damit wir später rekonstruieren)

    # dB-Schwellen in lineare Faktoren umrechnen:
    # threshold_db=6 => thr ~ 1.995 (≈2.0)
    thr = 10 ** (threshold_db / 20.0)

    # reduction_db=12 => atten ~ 0.251 (≈0.25)
    # (minus, weil wir absenken wollen)
    damp = 10 ** (-reduction_db / 20.0)

    # noise_floor ist shape [freq_bins]
    # Wir machen daraus [freq_bins, 1], damit es über alle Frames broadcasten kann
    nf = noise_floor[:, None]
    #print(f"{nf = }")
    #print(f"{noise_floor = }")


    # Gain-Matrix initialisieren:
    # np.ones_like(mag) -> gleiche shape wie <mag>, alles mit 1 ausgefüllt
    gain = np.ones_like(mag)

    # Maske: wo sig unterhalb (noise_floor * thr)" liegt -> rauschen 
    mask = mag < (nf * thr)

    # An diesen Stellen setzen wir gain auf atten (z.B. 0.25), d.h. wir dämpfen dort
    gain[mask] = damp
    #print(f"{gain = }")


    # Glätten des Gains:
    # 1) entlang Frequenz (axis=0) -> weniger "zerhacktes" Spektrum
    gain = _smooth_along_axis(gain, smooth_bins, axis=0)

    # 2) entlang Zeitframes (axis=1) -> weniger schnelle Gate-Flattern
    gain = _smooth_along_axis(gain, smooth_frames, axis=1)

    # Rekonstruktion eines "bereinigten" Spektrums:
    # Magnitude * gain (dämpft Noise-Bereiche), Phase bleibt erhalten
    Z_clean = (mag * gain) * phase

    # ISTFT zurück in die Zeitdomäne:
    # istft gibt (t_out, y_out) zurück
    _, y_clean = istft(
        Z_clean,                             # bereinigtes STFT
        fs=sr,                               # Samplingrate
        window=window,                       # Fenster
        nperseg=n_fft,                       # muss zu stft passen
        noverlap=noverlap,                   # muss zu stft passen
        nfft=n_fft,                          # muss zu stft passen
        input_onesided=True                  # weil wir onesided STFT hatten
    )

    return y_clean                           # fertiges, entrauschtes Signal
