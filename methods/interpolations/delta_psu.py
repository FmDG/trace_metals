import os

import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

from generate_interpolations import generate_interpolation
from objects.colours import colours


def delta_psu(save_fig: bool = False) -> int:

    # Error handling
    if not isinstance(save_fig, bool):
        raise ValueError("save_fig must be of type bool")

    # ------------------- LOAD DATA -------------------
    # PSU Data from 1209 and 1208
    psu_1209 = pd.read_csv("data/cores/1209_psu_02.csv").dropna()
    psu_1208 = pd.read_csv("data/cores/1208_psu.csv").dropna()
    # Oxygen isotope data from 1209 and 1208
    iso_1208 = pd.read_csv('data/cores/1208_cibs.csv')
    iso_1209 = pd.read_csv('data/cores/1209_cibs.csv')

    window_size = 100  # window size in ka

    # Define the colour schemes
    c_1208 = {'color': colours[0], 'label': '1208', 'marker': '+'}
    c_1209 = {'color': colours[1], 'label': '1209', 'marker': '+'}
    c_diff = {'color': colours[2], 'label': '1208 - 1209'}
    c_filt = {'color': 'k', 'label': "Rolling mean ({} ka)".format(window_size)}

    age_min, age_max = 2450, 2900

    # ------------------- GENERATE INTERPOLATIONS -------------------
    # Define the arguments required
    freq = 0.1
    interpolations_args = {'fs': freq, 'start': age_min, 'end': age_max, 'pchip': False}

    # Interpolate the BWT
    bwt_1209, age_array = generate_interpolation(psu_1209, value='temp', **interpolations_args)
    bwt_1208, _ = generate_interpolation(psu_1208, value='temp', **interpolations_args)

    # Interpolate the d18O_sw
    sw_1209, _ = generate_interpolation(psu_1209, value='d18O_sw', **interpolations_args)
    sw_1208, _ = generate_interpolation(psu_1208, value='d18O_sw', **interpolations_args)
    # Interpolate the d18O
    int_1209, _ = generate_interpolation(iso_1209, value='d18O_unadj', **interpolations_args)
    int_1208, _ = generate_interpolation(iso_1208, value='d18O_unadj', **interpolations_args)

    # Find the difference
    diff_bwt = bwt_1208 - bwt_1209
    diff_sw = sw_1208 - sw_1209
    diff_iso = int_1208 - int_1209

    # Run a 3rd order filter with a window defined below
    fill_diff_iso = savgol_filter(diff_iso, (int(window_size/freq) + 1), 3)
    fill_diff_bwt = savgol_filter(diff_bwt, (int(window_size/freq) + 1), 3)
    fill_diff_sw = savgol_filter(diff_sw, (int(window_size/freq) + 1), 3)

    # ------------------- GENERATE PLOTS -------------------
    # Generate a plot to display this
    num_plots = 6
    fig, axs = plt.subplots(num_plots, sharex="all", figsize=(10, 15))
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    # Plot up the 1208 data
    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **c_1208)
    axs[2].plot(psu_1208.age_ka, psu_1208.temp, **c_1208)
    axs[4].plot(psu_1208.age_ka, psu_1208.d18O_sw, **c_1208)

    # Plot up the 1209 data
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **c_1209)
    axs[2].plot(psu_1209.age_ka, psu_1209.temp, **c_1209)
    axs[4].plot(psu_1209.age_ka, psu_1209.d18O_sw, **c_1209)

    # Plot up the difference data
    axs[1].plot(age_array, diff_iso, **c_diff)
    axs[1].plot(age_array, fill_diff_iso, **c_filt)
    axs[1].fill_between(age_array, fill_diff_iso, 0, color='k', alpha=0.2)
    axs[3].plot(age_array, diff_bwt, **c_diff)
    axs[3].plot(age_array, fill_diff_bwt, **c_filt)
    axs[3].fill_between(age_array, fill_diff_bwt, 0, color='k', alpha=0.2)
    axs[5].plot(age_array, diff_sw, **c_diff)
    axs[5].plot(age_array, fill_diff_sw, **c_filt)
    axs[5].fill_between(age_array, fill_diff_sw, 0, color='k', alpha=0.2)

    # Label the axes
    axs[0].set(ylabel='{} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[1].set(ylabel='{} ({} VPDB)'.format(r'$\Delta \delta^{18}$O', u"\u2030"))
    axs[2].set(ylabel="BWT ({})".format(u'\N{DEGREE SIGN}C'))
    axs[3].set(ylabel="{}BWT ({})".format(r'$\Delta$', u'\N{DEGREE SIGN}C'))
    axs[4].set(ylabel='{} ({} VPDB)'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))
    axs[5].set(ylabel='{} ({} VPDB)'.format(r'$\Delta \delta^{18}$O$_{sw}$', u"\u2030"))

    # Invert the axes with d18O
    axs[0].invert_yaxis()
    axs[1].invert_yaxis()
    axs[4].invert_yaxis()
    axs[5].invert_yaxis()

    # Remove the various axes to clean up the plot
    for q in range(num_plots):

        axs[q].legend(frameon=False, shadow=False)
        # Remove the left/right axes to make the plot look cleaner
        if q % 2 == 1:
            axs[q].yaxis.set(ticks_position="right", label_position='right')
            axs[q].spines['left'].set_visible(False)
        else:
            axs[q].spines['right'].set_visible(False)
        axs[q].spines['top'].set_visible(False)
        axs[q].spines['bottom'].set_visible(False)

    # Set the bottom axis on and label it with the age.
    axs[(num_plots - 1)].spines['bottom'].set_visible(True)
    axs[(num_plots - 1)].set(xlabel='Age (ka)', xlim=[age_min, age_max])
    # Set another axis up top because the figure is getting a bit big.
    secax = axs[0].secondary_xaxis('top')
    secax.set_xlabel('Age (ka)')

    # Show the plot
    if save_fig:
        plt.savefig("figures/interpolations/D_BWT_03.png", format='png', dpi=300)
    else:
        plt.show()

    return 1


if __name__ == '__main__':
    os.chdir("../..")
    delta_psu(save_fig=False)
