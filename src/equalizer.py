import matplotlib.pyplot as plt
import numpy as np 
from scipy.interpolate import UnivariateSpline, PchipInterpolator


def plot_eq_points_and_fit(freqs, gains_db, xs, ys_db, ax=None, title="EQ", show=True):
    """
    Plottet EQ-Punkte (in dB) und die gefittete Kurve (in dB) in einem Plot.
    freqs: (N,) Hz
    gains_db: (N,) dB
    xs: (M,) Hz
    ys_db: (M,) dB
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(freqs, gains_db, "o", label="Punkte")
    ax.plot(xs, ys_db, "-", label="Fit")

    ax.set_xscale("log")
    ax.set_xlabel("Frequenz [Hz]")
    ax.set_ylabel("Gain [dB]")
    ax.set_title(title)
    ax.axhline(0, linewidth=1)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)
    ax.legend()

    if show:
        plt.tight_layout()
        plt.show()

    return ax


def eq_fkt(e32=0, e64=0, e125=0, e250=0, e500=0, e1k=0, e2k=0, e4k=0, e8k=0, e16k=0,
            do_plot=True, ax=None, title="EQ Punkte", show=True):
    """
    Erstellt 10 EQ-Punkte und plottet sie optional.
    Returns: Liste von (freq, gain)
    """
    
    points_db = np.array([
        [31,    e32],
        [62,    e64],
        [125,   e125],
        [250,   e250],
        [500,   e500],
        [1000,  e1k],
        [2000,  e2k],
        [4000,  e4k],
        [8000,  e8k],
        [16000, e16k]
    ], dtype=float)

    freqs = points_db[:, 0]   # erste Spalte
    gains_db = points_db[:, 1] # zweite Spalte

    gains_lin = 10 ** (gains_db / 20.0)
    points_lin = np.column_stack([freqs, gains_lin])



    # ---- Fit-fkt -----
    # Lin/logspace erstellen
    xs = np.logspace(np.log10(32), np.log10(20000), 512)

    # PchipInterpolator
    freqs_log = np.log10(freqs)
    pchip = PchipInterpolator(freqs_log, gains_db)
    ys_db = pchip(np.log10(xs))
    ys = 10 ** (ys_db / 20.0)

    # UnivariateSpline fit
    #spl = UnivariateSpline(freqs, gains_lin)
    #spl.set_smoothing_factor(0.1)
    #ys = spl(xs)

    if do_plot:
        plot_eq_points_and_fit(freqs, gains_db, xs, ys_db)

    return xs, ys

def apply_eq_1(sig, sr, xs, ys, clamp_outside="hold"):
    """
    Wendet eine EQ-fkt (xs Frequenzen in Hz, ys Gain linear) im Frequenzbereich zeit sig an 
    
    Args:
        sig:      1D numpy array (zeit sig )
        sr:       Sample-Rate (Hz)
        xs:       Frequenz (Hz) von eq_fkt
        ys:       Gain (linear, nicht dB!!), gleiche Länge wie xs von eq_fkt

        clamp_outside:
            "hold" -> außerhalb [min(xs), max(xs)] Gain am Rand halten
            "one"  -> außerhalb Gain = 1.0

    Returns:
        eq_sig:   Zeitsignal nach EQ 
    """

    sig = np.asarray(sig, dtype=float)
    n = len(sig)

    # Real-FFT (phase muss nicht beachtet werden)
    X = np.fft.rfft(sig)
    freqs = np.fft.rfftfreq(n, d=1.0/sr)  # Frequenzen der FFT-Bins

    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)

    # EQ-Kurve auf FFT-Bins interpolieren
    #    Dein xs ist logspace -> Interpolation auf log-Frequenz ist sinnvoll.
    f = freqs.copy()
    gains = np.ones_like(f)

    # DC (0 Hz) separat behandeln, weil log10(0) nicht geht
    gains[0] = 1.0
    mask = f > 0 #!!! wil log(0) nicht geht 
    f_pos = f[mask] # alles außer 0Hz

    gains_pos = np.interp(np.log10(f_pos), np.log10(xs), ys, left=1.0, right=1.0)

    # fertige maske aus eq_fkt
    gains[mask] = gains_pos

    # Anwenden
    Y = X * gains

    # Zurück in Zeitbereich
    eq_sig = np.fft.irfft(Y, n=n)

    return eq_sig

def apply_eq(signal, sr, xs, ys):
    """
    signal: np.ndarray (N,) oder (N, 2)
    xs: Frequenzen
    ys: Gain (linear)
    """

    # Mono → (N,1)
    if signal.ndim == 1:
        signal = signal[:, np.newaxis]

    N, channels = signal.shape
    out = np.zeros_like(signal)

    for ch in range(channels):
        x = signal[:, ch]

        # FFT
        X = np.fft.rfft(x)

        freqs = np.fft.rfftfreq(len(x), 1 / sr)

        # Gain-Kurve auf FFT-Bins interpolieren
        gains = np.interp(freqs, xs, ys)

        # Anwenden
        Y = X * gains

        # IFFT
        out[:, ch] = np.fft.irfft(Y, n=len(x))

    # Mono wieder zurückgeben
    if out.shape[1] == 1:
        return out[:, 0]

    return out



#if __name__ == "__main__":
#    eq_fkt(e32=0, e500=-12, e4k=6)
    