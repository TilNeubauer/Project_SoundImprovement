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


def add_sig(sig_orig,freq, sr):
    """overlay a Sin on an existing signal.
    Args:
        sig_orig: The original signal.
        sr: sample rate of original signal
        freq: the freq of the new sig
        
    Returns:
        A numpy array with the new signal.
    """  

    l = int(len(sig_orig) / sr)
    sig = gen_sin_sig(l, freq, sr)

    new_sig = sig_orig + sig
    
    return new_sig
