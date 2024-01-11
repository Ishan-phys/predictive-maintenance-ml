import matplotlib.pyplot as plt  
import numpy as np

from src.components.features import calc_fft
from src.components.data_transformation  import DataTransformation


def plot_fft(ax, fft, freq_cutoff=2000, n_xticks=20, **kwargs):
    """Plots the FFT of the data.

    Args:
        data (dict): Dictionary with the data.
        plot_title (str): Title of the plot.
        plot_xlabel (str): Label of the x axis.
        plot_ylabel (str): Label of the y axis.
    """
    color = kwargs.get('color', 'black')
    label = kwargs.get('label', None)
    alpha = kwargs.get('alpha', 0.8)
    linewidth = kwargs.get('linewidth', 0.9)
    linestyle = kwargs.get('linestyle', '-')

    # Get the frequency and amplitude
    frequency = fft["fftFrequency"]
    amplitude = fft["fftAmplitude"]

    ax.plot(frequency[frequency <= freq_cutoff], amplitude[frequency <= freq_cutoff], linewidth=linewidth, linestyle=linestyle, alpha=alpha, color=color, label=label)
    
    ax.set_title(f"FFT Spectrum", fontsize=14)
    ax.set_xticks(frequency[frequency <= freq_cutoff][::n_xticks])
    ax.tick_params(axis='x', labelsize=10, rotation=90)
    ax.tick_params(axis='y', labelsize=10)
    ax.set_xlabel("frequency(Hz)", fontsize=12)
    ax.set_ylabel(f"ampitude($mm/s^2$)", fontsize=12)

    return None


def plot_freq_info(ax, fft, **kwargs):
    """Plots the frequency information along with the FFT.

    Args:
        ax (_type_): _description_
        fft (_type_): _description_

    Returns:
        _type_: _description_
    """
    rated_rpm  = kwargs.get('rated_rpm', None)
    pole_pairs = kwargs.get('pole_pairs', None)
    fault_freq = kwargs.get('fault_freq', None)
    harmonic   = kwargs.get('harmonic', 1)

    # Get the frequency and amplitude
    frequency = fft["fftFrequency"]
    amplitude = fft["fftAmplitude"]

    supply_freq = frequency[np.argmax(amplitude)]

    ax.axvline(x=supply_freq, ymin=0, ymax=1, label=f'supply frequency {supply_freq}hz', linewidth=0.5, alpha=0.8, color='b', linestyle='--')

    if rated_rpm is not None and pole_pairs is not None:
        rated_supply_freq = 50
        N_sync = (60 * rated_supply_freq) / pole_pairs
        print(f"Synchronous speed: {N_sync} rpm")

        slip = (N_sync - rated_rpm) / N_sync
        print(f"Calculated slip FL: {slip}")

        sideband_freq_pos = supply_freq + 2 * supply_freq * slip
        sideband_freq_neg = supply_freq - 2 * supply_freq * slip
        ax.axvline(x=sideband_freq_pos, ymin=0, ymax=1, label=f'sb +2sf {round(sideband_freq_pos, 2)}hz', linewidth=0.5, alpha=0.8, color='grey', linestyle='--')
        ax.axvline(x=sideband_freq_neg, ymin=0, ymax=1, label=f'sb -2sf {round(sideband_freq_neg, 2)}hz', linewidth=0.5, alpha=0.8, color='grey', linestyle='--')

    if fault_freq is not None:
        ax.axvline(x=supply_freq+harmonic*fault_freq, ymin=0, ymax=1, label=f'{harmonic}*{fault_freq}hz', linewidth=0.5, alpha=0.8, color='grey', linestyle='--')
    
    return None



sampling_rate = 20480
freq_cutoff = 2000
n_xticks = 100

dt = DataTransformation()

healthy_data = dt.extract_data_file(data_filepath='artifacts/data/raw/2nd_test/2004.02.12.11.02.39')[:,0]
unhealthy_data = dt.extract_data_file(data_filepath='artifacts/data/raw/2nd_test/2004.02.19.00.22.39')[:,0]

_, healthy_amps, healthy_freqs = calc_fft(healthy_data, sampling_rate=20480)
_, unhealthy_amps, unhealthy_freqs = calc_fft(unhealthy_data, sampling_rate=20480)


fft_healthy = {
    "fftAmplitude": healthy_amps,
    "fftFrequency": healthy_freqs
}

fft_unhealthy = {
    "fftAmplitude": unhealthy_amps,
    "fftFrequency": unhealthy_freqs
}

plt.style.use('fivethirtyeight')
fig, ax = plt.subplots()
plot_fft(ax, fft_healthy, freq_cutoff=freq_cutoff, n_xticks=n_xticks, alpha=0.6, label='Asset Healthy')
plot_fft(ax, fft_unhealthy, freq_cutoff=freq_cutoff, n_xticks=n_xticks, color='r', alpha=0.5, label='Asset Unhealthy')

ax.legend(loc='upper right', fontsize=10)


plt.show()




