"""
Plotting up all the figures for the paper.
"""

import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

from methods.interpolations.generate_interpolations import generate_interpolation
from methods.figures.tick_dirs import tick_dirs
import objects.figure_arguments as args
from objects.core_data.psu import psu_1208, psu_1209, psu_607
from objects.core_data.isotopes import iso_607, iso_1208, iso_1209


def pres_figures():

    num_plots = 2
    min_age, max_age = 2500, 2850

    # --------------------- DEFINE THE DIFFERENCE IN d18O -------------------

    # Interpolate across the d18O arrays
    freq = 0.1
    interp_1208, age_array = generate_interpolation(iso_1208, fs=freq, start=min_age, end=max_age, pchip=False)
    interp_1209, _ = generate_interpolation(iso_1209, fs=freq, start=min_age, end=max_age, pchip=False)

    # Calculate the differences
    differences = interp_1208 - interp_1209
    # Run a 3rd order filter with a window defined below
    window_size = 30  # window size in ka
    filtered_diff = savgol_filter(differences, (int(window_size/freq) + 1), 3)

    fig, axs = plt.subplots(
        nrows=num_plots,
        ncols=1,
        sharex='all'
    )

    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    # Plot the differences in d18O
    axs[1].plot(age_array, differences, **args.args_diff)
    axs[1].plot(age_array, filtered_diff, **args.args_filt)
    axs[1].fill_between(age_array, filtered_diff, **args.fill_diff)

    # PSU d18O_sw estimates
    axs[0].plot(psu_1208.age_ka, psu_1208.d18O_sw, **args.args_1208)
    axs[0].fill_between(psu_1208.age_ka, psu_1208.d18O_min1, psu_1208.d18O_plus1, **args.fill_1208)

    # PSU d18O_sw estimates
    axs[0].plot(psu_1209.age_ka, psu_1209.d18O_sw, **args.args_1209)
    axs[0].fill_between(psu_1209.age_ka, psu_1209.d18O_min1, psu_1209.d18O_plus1, **args.fill_1209)

    # -- Define the axes --
    axs[0].set(ylabel='Modelled {} ({} VPDB)'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))
    axs[1].set(ylabel="{} (VPDB {})".format(r'$\Delta \delta^{18}$O ', u"\u2030"))

    tick_dirs(
        axs=axs,
        num_plots=num_plots,
        min_age=min_age,
        max_age=max_age,
    )

    axs[0].invert_yaxis()
    axs[1].invert_yaxis()

    plt.show()


if __name__ == "__main__":
    pres_figures()

