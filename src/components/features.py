import numpy as np

from scipy.fft import fft, fftfreq
from scipy.signal.windows import hann, hamming


def calc_fft(arr, sampling_rate, resolution=None, window=None, x_unit=None, y_unit=None):
    """Calculate the FFT from the data

    args:
        arr (np array): data
        sampling_rate (int): sampling rate
        resolution (int): resolution
        window (str): window function
        x_unit (str): x axis unit
        y_unit (str): y axis unit

    Returns:
        tuple: arr, fft_amplitudes, fft_frequencies
    """
    # Remove trailing zeros from the data
    duration = len(arr) // sampling_rate

    arr = arr[0 : int(duration * sampling_rate)]

    # Check if fMax is greater than sampling rate/2 if yes then limit it to sampling rate/2
    if fMax == None:
        fMax = sampling_rate / 2

    elif fMax > sampling_rate / 2:
        fMax = sampling_rate / 2

    if resolution == None:
        numBins = duration * sampling_rate
    else:
        numBins = int((duration * sampling_rate) / resolution)

    # Calculate the mean value from the data
    mean_value = np.mean(arr)

    # Subtract the mean value from the data (Removing the baseline)
    arr = arr - mean_value

    # Applying the window functions
    if window == "hanning":
        arr *= hann(len(arr), False)
    elif window == "hamming":
        arr *= hamming(len(arr), False)
    
    # FFT
    raw_fft_amplitudes = (2 / numBins * np.abs(fft(arr, n=numBins))[: numBins // 2])

    # If log scale is selected then calculate the log output
    if y_unit == "log":
        raw_fft_amplitudes = 10 * np.log10(raw_fft_amplitudes)

    # Calculate the FFT y axis
    if x_unit == "cpm":
        raw_fft_frequencies = fftfreq(numBins, 1.0 / sampling_rate)[: numBins // 2] * 60
    else:
        raw_fft_frequencies = fftfreq(numBins, 1.0 / sampling_rate)[: numBins // 2]
                  
    # Limit the FFT output to fMax
    fft_amplitudes  = raw_fft_amplitudes[: int(fMax / (sampling_rate / numBins))]
    fft_frequencies = raw_fft_frequencies[: int(fMax / (sampling_rate / numBins))]

    # Create the return data structure
    return arr, fft_amplitudes, fft_frequencies


def calc_rms(arr):
    """Calculate the RMS from the data

    Args:
        arr (np array): data

    Returns:
        float: RMS value
    """
    return np.sqrt(np.mean(np.square(arr)))


def calc_spectrum_features():
    pass


def calc_time_features():
    pass