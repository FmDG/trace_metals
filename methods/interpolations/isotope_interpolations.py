import os

import pandas as pd
import scipy.interpolate as interpol
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

def interpolate_isotopes(plot_interpol=False):
    # Load the datasets
    site_1208 = pd.read_csv('data/cores/1208_cibs.csv')
    site_1209 = pd.read_csv('data/cores/1209_cibs.csv')

    # Age array
    start = 2400
    stop = 3600
    age_array = np.arange(start, stop, 0.1)

    # We can use two different interpolation techniques - the first is a simple 1D interpolation, the second is a
    # PChip interpolation

    function_1208 = interpol.interp1d(x=site_1208.age_ka, y=site_1208.d18O_unadj, fill_value="extrapolate")
    function_1209 = interpol.interp1d(x=site_1209.age_ka, y=site_1209.d18O_unadj, fill_value="extrapolate")

    site_1208 = site_1208.dropna(subset=["d18O_unadj", "age_ka"])
    site_1209 = site_1209.dropna(subset=["d18O_unadj", "age_ka"])

    site_1208 = site_1208.sort_values(by="age_ka")
    site_1208 = site_1208.drop_duplicates(subset='age_ka')

    site_1209 = site_1209.sort_values(by="age_ka")
    site_1209 = site_1209.drop_duplicates(subset='age_ka')

    pchip_1208 = interpol.pchip_interpolate(xi=site_1208.age_ka, yi=site_1208.d18O_unadj, x=age_array)
    pchip_1209 = interpol.pchip_interpolate(xi=site_1209.age_ka, yi=site_1209.d18O_unadj, x=age_array)

    # Interpolate across this age array
    interpolated_1208 = function_1208(age_array)
    interpolated_1209 = function_1209(age_array)

    # Filter pchip function
    filtered_diff = savgol_filter((pchip_1208-pchip_1209), 301, 3)

    fig, axs = plt.subplots(2, sharex="all")
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    axs[0].plot(age_array, pchip_1208)
    axs[0].plot(age_array, pchip_1209)
    axs[0].scatter(site_1208.age_ka, site_1208.d18O_unadj, label="ODP 1208", marker='+')
    axs[0].scatter(site_1209.age_ka, site_1209.d18O_unadj, label="ODP 1209", marker='+')
    axs[0].set(ylabel='Interpolated {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[0].invert_yaxis()
    axs[0].spines['right'].set_visible(False)
    axs[0].spines['top'].set_visible(False)
    axs[0].spines['bottom'].set_visible(False)
    axs[0].legend()

    axs[1].plot(age_array, (pchip_1208 - pchip_1209), label="Difference", c='m')
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

    # Age array
    start = 2400
    stop = 3600
    age_array = np.arange(start, stop, num_interpolation)

    # We can use two different interpolation techniques - the first is a simple 1D interpolation, the second is a
    # PChip interpolation

    function_1208 = interpol.interp1d(x=site_1208.age_ka, y=site_1208.d18O_unadj, fill_value="extrapolate")
    function_1209 = interpol.interp1d(x=site_1209.age_ka, y=site_1209.d18O_unadj, fill_value="extrapolate")

    site_1208 = site_1208.dropna(subset=["d18O_unadj", "age_ka"])
    site_1209 = site_1209.dropna(subset=["d18O_unadj", "age_ka"])

    site_1208 = site_1208.sort_values(by="age_ka")
    site_1208 = site_1208.drop_duplicates(subset='age_ka')

    site_1209 = site_1209.sort_values(by="age_ka")
    site_1209 = site_1209.drop_duplicates(subset='age_ka')

    pchip_1208 = interpol.pchip_interpolate(xi=site_1208.age_ka, yi=site_1208.d18O_unadj, x=age_array)
    pchip_1209 = interpol.pchip_interpolate(xi=site_1209.age_ka, yi=site_1209.d18O_unadj, x=age_array)

    # Interpolate across this age array
    interpolated_1208 = function_1208(age_array)
    interpolated_1209 = function_1209(age_array)

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
    age_array = np.arange(start, stop, 0.1)

    # Drop any N/A values
    site_1208 = site_1208.dropna(subset=["d18O_unadj", "age_ka"])
    site_1209 = site_1209.dropna(subset=["d18O_unadj", "age_ka"])

    # Drop any duplicate values and sort the dataset in ascending order
    site_1208 = site_1208.sort_values(by="age_ka")
    site_1208 = site_1208.drop_duplicates(subset='age_ka')

    site_1209 = site_1209.sort_values(by="age_ka")
    site_1209 = site_1209.drop_duplicates(subset='age_ka')

    # Interpolate across the dataset using the pChip interpolator
    pchip_1208 = interpol.pchip_interpolate(xi=site_1208.age_ka, yi=site_1208.d18O_unadj, x=age_array)
    pchip_1209 = interpol.pchip_interpolate(xi=site_1209.age_ka, yi=site_1209.d18O_unadj, x=age_array)

    '''periods = np.logspace(0, 7, 1000, base=2)
    wps = WPS(periods)

    sig = TSeries(age_array, pchip_1208)

    spectrum = wps(sig)

    spectrum.contourf(y="period", extend="min", levels=10)
    wps.plot_coi(hatch="x", color="grey", alpha=0.5)
    plt.yscale("log")
    '''

if __name__ == "__main__":
    os.chdir('../..')
    time_series_analysis()
