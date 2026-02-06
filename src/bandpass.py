from scipy.signal import butter, lfilter

"""
Inspieriert von: https://stackoverflow.com/questions/12093594/how-to-implement-band-pass-butterworth-filter-with-scipy-signal-butter
"""


def butter_bandpass(lowcut, highcut, fs, order=5):
  """
  Args:
    lowcut: low freq for bandpass
    highcut: high freq for bandpass
    fs: sampling frequency
    order: --

  Return: 
    b, a: ndarray
      Numerator (b) and denominator (a) polynomials
  """

  return butter(order, [lowcut, highcut], fs=fs, btype='band')


def butter_bandpass_filter(data, lowcut, highcut, sr, order=10):
  """
  Args:
    data: time series 
    lowcut: low freq for bandpass
    highcut: high freq for bandpass
    sr: sample rate of audio file == fs (sampling frequency)
    order: --

  Return: 
    y: filtered time series
  """

  fs = sr

  b, a = butter_bandpass(lowcut, highcut, fs, order=order)
  y = lfilter(b, a, data)
  return y