import numpy as np

from scipy.fft import fft, fftfreq
from scipy.signal.windows import hann, hamming
from scipy.stats import kurtosis, skew


def calc_fft(arr, sampling_rate, resolution=None, window=None, x_unit=None, y_unit=None, fMax=None):
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
    arr = 9.8 * arr

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


def sign(arr):
    """
    Returns a numpy array containing 1,0 and -1. 1 represents positive numbers,-1 represents negative numbers and 0 represents the number zero.

    INPUT:
        arr: a numpy array
    RETURNS:
        sign_arr: a numpy array of 1s,0s and -1s.

    Eg:
        In: sign(np.array([ 1, 2, -1, -2, 0, -2]))
        Out: array([ 1,  1, -1, -1,  0, -1])

    """
    sign_arr = np.where(arr > 0, 1, np.where(arr < 0, -1, 0))
    return sign_arr


def zero_crossings(data, threshold=0.015):
    """Calculates the no. of zero crossings in given data.

    INPUT:
        data: a 1-D numpy array
        threshold: Required minimum difference between consecutive entries in the data (useful in case of noisy data),default value is 0.015
    RETURNS:
        the no. of zero crossings

    Eg:
        In: data = np.array([1,-1,2,3])
            print(zero_crossings(data))
        Out: 2.0

    """
    a, b = data[:-1], data[1:]

    a1, b1 = sign(a), sign(b)

    diff = abs(a - b)  # Taking difference between consecutive values

    a1, b1 = a1[diff >= threshold], b1[diff >= threshold]

    zc = np.floor(
        np.sum(abs(a1 - b1)) / 2
    )  # Opposite signs get added up to 2 and finally we divide by 2 to get our ans
    return zc


def calc_rms(arr):
    """Calculate the RMS from the data

    Args:
        arr (np array): data

    Returns:
        float: RMS value
    """
    return np.sqrt(np.mean(np.square(arr)))


def calc_spectrum_features(fft_amplitudes):
    """Calculate the spectrum features from the data
    
    Args:
        fft_data (np array): data

    Returns:
        dict: spectrum features
    """
    rms          = calc_rms(fft_amplitudes)
    max_amp      = np.amax(fft_amplitudes)
    crest_Factor = max_amp / rms
    energy      = np.sum(np.square(fft_amplitudes))
    form_factor_absmean = float(rms / (abs(fft_amplitudes).mean()))
    skewness_val = skew(fft_amplitudes)
    kurtosis_val = kurtosis(fft_amplitudes)

    spectrum_features = {
        "frms": rms,
        "fmax_amp": max_amp,
        "fcrest_Factor": crest_Factor,
        "fenergy": energy,
        "fform_factor_absmean": form_factor_absmean,
        "fskewness_val": skewness_val,
        "fkurtosis_val": kurtosis_val,
    }

    return spectrum_features


def calc_time_features(time_data):
    """Calculate the time features from the data

    Args:
        data (np array): data

    Return:
        dict: time domain features
    """
    rms     = calc_rms(time_data)
    max_amp = np.amax(time_data)
    crest_Factor  = max_amp / rms
    zero_crossing = int(zero_crossings(time_data))
    form_factor_absmean = float(rms / (abs(time_data).mean()))
    data_kurt = kurtosis(time_data)
    data_skew = skew(time_data)

    time_features = {
        "trms": rms,
        "tmax_amp": max_amp,
        "tcrest_Factor": crest_Factor,
        "tzero_crossing": zero_crossing,
        "tform_factor_absmean": form_factor_absmean,
        "tkurtosis_val": data_kurt,
        "tskewness_val": data_skew,
    }

    return time_features