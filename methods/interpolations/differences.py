import os

import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import savgol_filter

from methods.interpolations.isotope_interpolations import generate_interpolation


def simple_interpolation(age_min=2400, age_max=3400):
    # Load the datasets
    site_1208 = pd.read_csv('data/cores/1208_cibs.csv')
    site_1209 = pd.read_csv('data/cores/1209_cibs.csv')

    # We use a simple 1D interpolation, with a density of "freq"
    freq = 0.1
    interp_1208, age_array = generate_interpolation(site_1208, fs=freq, start=age_min, end=age_max, pchip=False)
    interp_1209, _ = generate_interpolation(site_1209, fs=freq, start=age_min, end=age_max, pchip=False)

    # Filter interpolation function over "window" ka, with a polynomial function of order "n"
    window = 40  # in ka
    n = 3
    filtered_diff = savgol_filter((interp_1208 - interp_1209), int(window / freq + 1), n)

    # Generate a plot to display this
    fig, axs = plt.subplots(2, sharex="all")
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    # Plot the oxygen isotope records from 1208 and 1209
    axs[0].plot(site_1208.age_ka, site_1208.d18O_unadj, label="ODP 1208", marker='+')
    axs[0].plot(site_1209.age_ka, site_1209.d18O_unadj, label="ODP 1209", marker='+')
    axs[0].set(ylabel='Benthic {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[0].invert_yaxis()
    axs[0].spines['right'].set_visible(False)
    axs[0].spines['top'].set_visible(False)
    axs[0].spines['bottom'].set_visible(False)
    axs[0].legend()

    # Plot the difference between the isotope records
    axs[1].plot(age_array, (interp_1208 - interp_1209), label="Difference", c='m')
    axs[1].plot(age_array, filtered_diff, label="Filtered Difference", c='k')
    axs[1].set(xlabel="Age (ka)", ylabel="Difference in {} ({})".format(r'$\delta^{18}$O', u"\u2030"),
               xlim=[age_min, age_max])

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


if __name__ == "__main__":
    os.chdir('../..')
    simple_interpolation()
