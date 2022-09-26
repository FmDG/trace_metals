import os

import pandas as pd
import scipy.interpolate as interpol
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, periodogram

# Colours
colours = ['#fbb4ae', '#b3cde3', '#ccebc5']


def generate_interpolation(dataseries, fs=1.0, start=2400, end=3400, pchip=False):
    # Define the age array
    age_array = np.arange(start, end, fs)

    # Drop any N/A values
    dataseries = dataseries.dropna(subset=["d18O_unadj", "age_ka"])

    # Drop any duplicate values and sort the dataset in ascending order
    dataseries = dataseries.sort_values(by="age_ka")
    dataseries = dataseries.drop_duplicates(subset='age_ka')

    if pchip:
        # Interpolate across the dataset using the pChip interpolator
        interpolated_dataset = interpol.pchip_interpolate(xi=dataseries.age_ka, yi=dataseries.d18O_unadj, x=age_array)
    else:
        function_int = interpol.interp1d(x=dataseries.age_ka, y=dataseries.d18O_unadj, fill_value="extrapolate")
        # Interpolate across this age array
        interpolated_dataset = function_int(age_array)

    return interpolated_dataset, age_array


def interpolate_isotopes(plot_interpol=False):

    # Age limits
    start = 2400
    stop = 3400

    # Load the datasets
    site_1208 = pd.read_csv('data/cores/1208_cibs.csv')
    site_1209 = pd.read_csv('data/cores/1209_cibs.csv')

    # We can use two different interpolation techniques - the first is a simple 1D interpolation, the second is a
    # PChip interpolation

    interp_1208, age_array = generate_interpolation(site_1208, fs=0.1, start=start, end=stop, pchip=False)
    interp_1209, _ = generate_interpolation(site_1209, fs=0.1, start=start, end=stop, pchip=False)

    # Filter pchip function
    filtered_diff = savgol_filter((interp_1208-interp_1209), 301, 3)

    fig, axs = plt.subplots(2, sharex="all")
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    axs[0].plot(site_1208.age_ka, site_1208.d18O_unadj, label="ODP 1208", marker='+')
    axs[0].plot(site_1209.age_ka, site_1209.d18O_unadj, label="ODP 1209", marker='+')
    axs[0].set(ylabel='Benthic {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[0].invert_yaxis()
    axs[0].spines['right'].set_visible(False)
    axs[0].spines['top'].set_visible(False)
    axs[0].spines['bottom'].set_visible(False)
    axs[0].legend()

    axs[1].plot(age_array, (interp_1208 - interp_1209), label="Difference", c='m')
    axs[1].plot(age_array, filtered_diff, label="Filtered Difference", c='k')
    axs[1].set(xlabel="Age (ka)", ylabel="Difference in {} ({})".format(r'$\delta^{18}$O', u"\u2030"), xlim=[start, stop])

    # Adds horizontal 0 line
    # axs[1].axhline(0, ls='--', color='m')

    # Adds ± 2 and 4 sig.diff bars
    # axs[1].fill_between(age_array, -0.12, 0.12, color='m', alpha=0.2, label=r'$\pm 2 \sigma$')
    # axs[1].fill_between(age_array, -0.24, 0.24, color='m', alpha=0.1, label=r'$\pm 4 \sigma$')

    # Fills in the gap between the line and the 0 axis
    # axs[1].fill_between(age_array, (pchip_1208 - pchip_1209), 0, color='m', alpha=0.2)
    axs[1].fill_between(age_array, filtered_diff, 0, color='k', alpha=0.2)

    # Fill between regions where d18O goes higher than 2.9 per mil

    axs[1].invert_yaxis()
    axs[1].legend()
    axs[1].yaxis.set(ticks_position="right", label_position='right')
    axs[1].spines['left'].set_visible(False)
    axs[1].spines['top'].set_visible(False)

    plt.show()


def show_interpolation(num_interpolation=1.0):
    site_1208 = pd.read_csv('data/cores/1208_cibs.csv')
    site_1209 = pd.read_csv('data/cores/1209_cibs.csv')

    start = 2400
    stop = 3400

    pchip_1208, age_array = generate_interpolation(site_1208, fs=0.1, start=start, end=stop, pchip=True)
    pchip_1209, _ = generate_interpolation(site_1209, fs=0.1, start=start, end=stop, pchip=True)

    # Interpolate across this age array
    interpolated_1208, _ = generate_interpolation(site_1208, fs=0.1, start=start, end=stop, pchip=False)
    interpolated_1209, _ = generate_interpolation(site_1209, fs=0.1, start=start, end=stop, pchip=False)

    fig, axs = plt.subplots(2, sharex="all")
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    axs[0].plot(age_array, interpolated_1208, label="1208 Interpolated")
    axs[0].plot(age_array, pchip_1208, label="1208 pCHIP")
    axs[0].scatter(site_1208.age_ka, site_1208.d18O_unadj, label="1208 True", marker='+', c='k')
    axs[0].set(ylabel='{} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[0].invert_yaxis()
    axs[0].legend()

    axs[1].plot(age_array, interpolated_1209, label="1209 Interpolated")
    axs[1].plot(age_array, pchip_1209, label="1209 pCHIP")
    axs[1].scatter(site_1209.age_ka, site_1209.d18O_unadj, label="1209 True", marker='+', c='k')
    axs[1].set(ylabel='{} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"), xlim=[start, stop])
    axs[1].invert_yaxis()
    axs[1].legend()

    plt.show()


def time_series_analysis():

    # Load the datasets
    site_1208 = pd.read_csv('data/cores/1208_cibs.csv')
    site_1209 = pd.read_csv('data/cores/1209_cibs.csv')

    # Define the age array
    start = 2400
    stop = 3600
    ts = 0.1

    interpolated_1208, age_array = generate_interpolation(site_1208, fs=ts, start=start, end=stop)
    interpolated_1209, _ = generate_interpolation(site_1209, fs=ts, start=start, end=stop)

    freq_1208, psd_1208 = periodogram(interpolated_1208, fs=1)
    freq_1209, psd_1209 = periodogram(interpolated_1209, fs=1)
    freq_diff, psd_diff = periodogram((interpolated_1208 - interpolated_1209), fs=1)

    fig, axs = plt.subplots(nrows=1, ncols=2)

    axs[0].semilogy(freq_1208, psd_1208, color=colours[0])
    axs[0].set(ylim=[1e-8, 1e2], xlabel='frequency [1/kyr]', ylabel=r'PSD [$V^{2}$/kyr]', title="1208")
    axs[1].semilogy(freq_1209, psd_1209, color=colours[1])
    axs[1].set(ylim=[1e-8, 1e2], xlabel='frequency [1/kyr]', ylabel=r'PSD [$V^{2}$/kyr]', title="1209")

    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.semilogy(freq_diff, psd_diff, color=colours[2])
    ax.set(ylim=[1e-8, 1e2], xlabel='frequency [1/kyr]', ylabel=r'PSD [$V^{2}$/kyr]', title="Difference")
    plt.show()




if __name__ == "__main__":
    os.chdir('../..')
    interpolate_isotopes()
