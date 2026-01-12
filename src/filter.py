import numpy as np
import matplotlib.pyplot as plt

from sinSig import gen_sin_sig, add_noise
from plot import plot_sig_fft_2x

def auto_threshold(fft_sig, n=0.005) -> float:

  ts = max(np.abs(fft_sig)) * n

  return ts


def denoise_fft(noisy_signal, threshold=0):
  """Denoises a signal using FFT.
  
Args:
    noisy_signal: The noisy signal.
    threshold: The threshold for filtering frequency components. | How offten a freq musst occur -> if lower freq component gets removed 
    
    Returns:
        A numpy array representing the denoised signal.
  """  
  fft_signal = np.fft.fft(noisy_signal)

  if threshold == 0:
     threshold = auto_threshold(fft_signal)
  fft_signal[np.abs(fft_signal) < threshold] = 0

  denoised_signal = np.real(np.fft.ifft(fft_signal))

  return denoised_signal




if __name__ == "__main__":
    # Generate a signal
    signal_length = 1
    signal_freq = 50
    sr = 1024
    signal = gen_sin_sig(signal_length, signal_freq, sr)

    # Add noise
    noise_level = 0.5
    noisy_signal = add_noise(signal, noise_level)  # Denoise using FFT

    threshold = 100
    denoised_signal = denoise_fft(noisy_signal, threshold)  # Plot the results

    plot_sig_fft_2x(noisy_signal, sr, denoised_signal, sr)



