import numpy as np

def gen_sin_sig(length, freq, sr=10):
    """Generates a sinusoidal signal. 
    Args:
        length: Length of the signal. | in sec
        freq: Frequency of the signal.  
        sr: sample rate |samples per sec 

    Returns:
        A numpy array representing the signal.
    """  
    #t = np.linspace(0, length, num=length*sr, endpoint=True)
    n = int(length * sr)          # Anzahl Samples
    t = np.arange(n) / sr         # exakt 0, 1/sr, 2/sr, ...
    signal = np.sin(2 * np.pi * freq * t)

    return signal


def add_noise(signal, noise_level):
    """Adds noise to a signal.
    Args:
        signal: The original signal.
        noise_level: The level of noise to add. Standard deviation (spread or “width”) of the distribution

    Returns:
        A numpy array representing the noisy signal.
    """  
    noise = np.random.normal(0, noise_level, len(signal))
    noisy_signal = signal + noise

    return noisy_signal

