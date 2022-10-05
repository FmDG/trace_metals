"""
Plotting up all the figures for the paper.
"""

import os

import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

from methods.interpolations.generate_interpolations import generate_interpolation
from objects.colours import colours_extra as clr


# Define the colours
args_1208 = {'color': clr[0], 'label': "1208", 'marker': '+'}
fill_1208 = {'facecolor': clr[0], 'alpha': 0.1, 'label': r'$\pm 1\sigma$'}
args_1209 = {'color': clr[1], 'label': "1209", 'marker': '+'}
fill_1209 = {'facecolor': clr[1], 'alpha': 0.1, 'label': r'$\pm 1\sigma$'}
args_diff = {'color': clr[4], 'label': "1208 - 1209"}
args_filt = {'color': 'k', 'label': "Rolling mean (30 ka)"}
fill_diff = {'facecolor': 'k', 'alpha': 0.1}
args_607 = {'color': clr[2], 'label': "607", 'marker': '+'}
fill_607 = {'facecolor': clr[2], 'alpha': 0.1, 'label': r'$\pm 1\sigma$'}
args_1313 = {'color': clr[3], 'label': "1313", 'marker': '+'}
fill_1313 = {'facecolor': clr[3], 'alpha': 0.1, 'label': r'$\pm 1\sigma$'}


def figure_one(save_fig: bool = False) -> int:
    """
    The main figure. Showing d18O_b, BWT, and d18O_sw together on one plot for 1209/1208. Highlighting the results that
    I have collected.
    :param save_fig: Boolean - describes if we want to save the figure to folder figures_paper
    :return: True is all is well
    """

    # Error handling
    if not isinstance(save_fig, bool):
        raise ValueError("save_fig must be of type bool")

    # ------------------------ PLOT DATA ---------------------------

    # Plots for d18O_benthic, BWT and d18O_sw.
    num_plots = 3
    min_age, max_age = 2400, 2900

    # Define the figure
    fig, axs = plt.subplots(
        nrows=num_plots,
        ncols=1,
        sharex="all",
        figsize=(8, 8)
    )

    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)
    # Name the Plot
    fig.suptitle("Comparison of Sites 1208 and 1209\n ({} - {} ka)".format(min_age, max_age))

    # -- Plot the 1208 data --
    # d18O original data
    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)

    # PSU BWT estimates
    axs[1].plot(psu_1208.age_ka, psu_1208.temp, **args_1208)
    axs[1].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, **fill_1208)

    # PSU d18O_sw estimates
    axs[2].plot(psu_1208.age_ka, psu_1208.d18O_sw, **args_1208)
    axs[2].fill_between(psu_1208.age_ka, psu_1208.d18O_min1, psu_1208.d18O_plus1, **fill_1208)

    # -- Plot the 1209 data --
    # d18O original data
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)
    # PSU BWT estimates
    axs[1].plot(psu_1209.age_ka, psu_1209.temp, **args_1209)
    axs[1].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, **fill_1209)
    # PSU d18O_sw estimates
    axs[2].plot(psu_1209.age_ka, psu_1209.d18O_sw, **args_1209)
    axs[2].fill_between(psu_1209.age_ka, psu_1209.d18O_min1, psu_1209.d18O_plus1, **fill_1209)

    # -- Define the axes --
    axs[0].set(ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[1].set(ylabel="BWT ({})".format(u'\N{DEGREE SIGN}C'))
    axs[2].set(ylabel='Modelled {} ({} VPDB)'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))

    # Invert the axes with d18O
    axs[0].invert_yaxis()
    axs[2].invert_yaxis()

    for q in range(num_plots):
        # Remove the left/right axes to make the plot look cleaner
        if q % 2 == 1:
            axs[q].yaxis.set(ticks_position="right", label_position='right')
            axs[q].spines['left'].set_visible(False)
        else:
            axs[q].spines['right'].set_visible(False)
        axs[q].spines['top'].set_visible(False)
        axs[q].spines['bottom'].set_visible(False)
        axs[q].legend(shadow=False, frameon=False)

    # Set the bottom axis on and label it with the age.
    axs[(num_plots - 1)].spines['bottom'].set_visible(True)
    axs[(num_plots - 1)].set(xlabel='Age (ka)', xlim=[min_age, max_age])

    # Save the figure if required
    if save_fig:
        plt.savefig("figures/paper/Figure_1.png", format="png", dpi=300)
    else:
        plt.show()

    return 1


def figure_two(save_fig: bool = False) -> int:
    """
    A comparison figure of the BWT at 1208 and 1209 and the Delta d18O - showing how BWT does not explain all the
    difference in d18O and that it also not fully explained by d18O_sw either.
    :param save_fig: bool - save the figure to the folder paper as figure 2
    :return: returns 1 if all is well
    """

    # Error handling
    if not isinstance(save_fig, bool):
        raise ValueError("save_fig must be of type bool")

    # Plots for BWT and Dd18O
    num_plots = 3
    min_age, max_age = 2400, 2900

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

    # --------------------- PLOT THE DATA ------------------------

    fig, axs = plt.subplots(
        nrows=num_plots,
        ncols=1,
        sharex="all",
        figsize=(8, 8)
    )

    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)
    # Name the Plot
    fig.suptitle("Comparison of Sites 1208 and 1209\n ({} - {} ka)".format(min_age, max_age))

    # -- Plot the 1208 data --
    # PSU BWT estimates
    axs[0].plot(psu_1208.age_ka, psu_1208.temp, **args_1208)
    axs[0].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, **fill_1208)
    # PSU d18O_sw estimates
    axs[2].plot(psu_1208.age_ka, psu_1208.d18O_sw, **args_1208)
    axs[2].fill_between(psu_1208.age_ka, psu_1208.d18O_min1, psu_1208.d18O_plus1, **fill_1208)

    # -- Plot the 1209 data --
    # PSU BWT estimates
    axs[0].plot(psu_1209.age_ka, psu_1209.temp, **args_1209)
    axs[0].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, **fill_1209)
    # PSU d18O_sw estimates
    axs[2].plot(psu_1209.age_ka, psu_1209.d18O_sw, **args_1209)
    axs[2].fill_between(psu_1209.age_ka, psu_1209.d18O_min1, psu_1209.d18O_plus1, **fill_1209)

    # Plot the differences in d18O
    axs[1].plot(age_array, differences, **args_diff)
    axs[1].plot(age_array, filtered_diff, **args_filt)
    axs[1].fill_between(age_array, filtered_diff, **fill_diff)

    # -- Define the axes --
    axs[0].set(ylabel="BWT ({})".format(u'\N{DEGREE SIGN}C'))
    axs[1].set(ylabel="{} (VPDB {})".format(r'$\Delta \delta^{18}$O ', u"\u2030"))
    axs[2].set(ylabel='Modelled {} ({} VPDB)'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))

    # Invert the axes with d18O
    axs[1].invert_yaxis()
    axs[2].invert_yaxis()

    for q in range(num_plots):
        # Remove the left/right axes to make the plot look cleaner
        if q % 2 == 1:
            axs[q].yaxis.set(ticks_position="right", label_position='right')
            axs[q].spines['left'].set_visible(False)
        else:
            axs[q].spines['right'].set_visible(False)
        axs[q].spines['top'].set_visible(False)
        axs[q].spines['bottom'].set_visible(False)
        axs[q].legend(shadow=False, frameon=False)

    # Set the bottom axis on and label it with the age.
    axs[(num_plots - 1)].spines['bottom'].set_visible(True)
    axs[(num_plots - 1)].set(xlabel='Age (ka)', xlim=[min_age, max_age])

    # Save the figure if required
    if save_fig:
        plt.savefig("figures/paper/Figure_2.png".format(min_age, max_age), format="png", dpi=300)
    else:
        plt.show()

    return 1


def figure_three(save_fig: bool = False) -> int:
    """
    A global context for these results, comparing the BWT in the North Atlantic (U1308/607) and the North Pacific.
    :param save_fig: bool - save the figure to the folder paper as figure 3
    :return: returns 1 if all is well
    """

    # Error handling
    if not isinstance(save_fig, bool):
        raise ValueError("save_fig must be of type bool")

    # BWT across N. Atlantic and Pacific as well as d18O, and d18O_sw
    num_plots = 2
    min_age, max_age = 2400, 2900

    # --------------------- PLOT THE DATA ------------------------

    fig, axs = plt.subplots(
        nrows=num_plots,
        ncols=1,
        sharex="all",
        figsize=(8, 8)
    )

    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)
    # Name the Plot
    fig.suptitle("Global Context\n ({} - {} ka)".format(min_age, max_age))

    # -- Plot the 1208 data --
    # PSU BWT estimates
    axs[0].plot(psu_1208.age_ka, psu_1208.temp, **args_1208)
    axs[0].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, **fill_1208)
    # d18O isotope plot
    axs[1].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)

    # -- Plot the 1209 data --
    # PSU BWT estimates
    axs[0].plot(psu_1209.age_ka, psu_1209.temp, **args_1209)
    axs[0].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, **fill_1209)
    # d18O isotope plot
    axs[1].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)

    # -- Plot the 607 data --
    # PSU BWT estimates
    axs[0].plot(psu_607.age_ka, psu_607.temp, **args_607)
    axs[0].fill_between(psu_607.age_ka, psu_607.temp_min1, psu_607.temp_plus1, **fill_607)
    # d18O isotope plot
    axs[1].plot(iso_607.age_ka, iso_607.d18O, **args_607)

    # -- Define the axes --
    axs[0].set(ylabel="BWT ({})".format(u'\N{DEGREE SIGN}C'))
    axs[1].set(ylabel="{} (VPDB {})".format(r'$\delta^{18}$O', u"\u2030"))

    # Invert the axes with d18O
    axs[1].invert_yaxis()

    for q in range(num_plots):
        # Remove the left/right axes to make the plot look cleaner
        if q % 2 == 1:
            axs[q].yaxis.set(ticks_position="right", label_position='right')
            axs[q].spines['left'].set_visible(False)
        else:
            axs[q].spines['right'].set_visible(False)
        axs[q].spines['top'].set_visible(False)
        axs[q].spines['bottom'].set_visible(False)
        axs[q].legend(shadow=False, frameon=False)

    # Set the bottom axis on and label it with the age.
    axs[(num_plots - 1)].spines['bottom'].set_visible(True)
    axs[(num_plots - 1)].set(xlabel='Age (ka)', xlim=[min_age, max_age])

    # Save the figure if required
    if save_fig:
        plt.savefig("figures/paper/Figure_3.png".format(min_age, max_age), format="png", dpi=300)
    else:
        plt.show()

    return 1


def figure_s1(save_fig: bool = False) -> int:
    """
    A global context for these results, comparing the BWT in the North Atlantic (U1308/607) and the North Pacific.
    :param save_fig: bool - save the figure to the folder paper as figure 3
    :return: returns 1 if all is well
    """

    # Error handling
    if not isinstance(save_fig, bool):
        raise ValueError("save_fig must be of type bool")

    # BWT across N. Atlantic and Pacific as well as d18O, and d18O_sw
    num_plots = 2
    min_age, max_age = 2400, 2900

    # --------------------- PLOT THE DATA ------------------------

    fig, axs = plt.subplots(
        nrows=num_plots,
        ncols=1,
        sharex="all",
        figsize=(8, 12)
    )

    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)
    # Name the Plot
    fig.suptitle("Global Context\n ({} - {} ka)".format(min_age, max_age))

    # -- Plot the 1208 data --
    # PSU BWT estimates
    axs[0].plot(psu_1208.age_ka, psu_1208.temp, **args_1208)
    axs[0].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, **fill_1208)
    # d18O isotope plot
    axs[1].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)

    # -- Plot the 1209 data --
    # PSU BWT estimates
    axs[0].plot(psu_1209.age_ka, psu_1209.temp, **args_1209)
    axs[0].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, **fill_1209)
    # d18O isotope plot
    axs[1].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)

    # -- Plot the 607 data --
    # PSU BWT estimates
    axs[0].plot(psu_607.age_ka, psu_607.temp, **args_607)
    axs[0].fill_between(psu_607.age_ka, psu_607.temp_min1, psu_607.temp_plus1, **fill_607)
    # d18O isotope plot
    axs[1].plot(iso_607.age_ka, iso_607.d18O, **args_607)

    # -- Plot the U1313 data --
    # PSU BWT estimates
    axs[0].plot(psu_1313.age_ka, psu_1313.temp, **args_1313)
    axs[0].fill_between(psu_1313.age_ka, psu_1313.temp_min1, psu_1313.temp_plus1, **fill_1313)
    # d18O isotope plot
    axs[1].plot(iso_1313.age_ka, (iso_1313.d18O - 0.64), **args_1313)

    # -- Define the axes --
    axs[0].set(ylabel="BWT ({})".format(u'\N{DEGREE SIGN}C'))
    axs[1].set(ylabel="{} (VPDB {})".format(r'$\delta^{18}$O', u"\u2030"))

    # Invert the axes with d18O
    axs[1].invert_yaxis()

    for q in range(num_plots):
        # Remove the left/right axes to make the plot look cleaner
        if q % 2 == 1:
            axs[q].yaxis.set(ticks_position="right", label_position='right')
            axs[q].spines['left'].set_visible(False)
        else:
            axs[q].spines['right'].set_visible(False)
        axs[q].spines['top'].set_visible(False)
        axs[q].spines['bottom'].set_visible(False)
        axs[q].legend(shadow=False, frameon=False)

    # Set the bottom axis on and label it with the age.
    axs[(num_plots - 1)].spines['bottom'].set_visible(True)
    axs[(num_plots - 1)].set(xlabel='Age (ka)', xlim=[min_age, max_age])

    # Save the figure if required
    if save_fig:
        plt.savefig("figures/paper/Figure_S1.png".format(min_age, max_age), format="png", dpi=300)
    else:
        plt.show()

    return 1


if __name__ == "__main__":
    os.chdir("../..")

    # Load the datasets
    # Load the PSU datasets
    psu_1208 = pd.read_csv("data/cores/1208_psu.csv").dropna()
    psu_1209 = pd.read_csv("data/cores/1209_psu_02.csv").dropna()
    psu_607 = pd.read_csv("data/cores/607_psu.csv").dropna()
    psu_1313 = pd.read_csv("data/cores/U1313_psu.csv").dropna()

    # Load the Oxygen Isotope datasets
    iso_1208 = pd.read_csv("data/cores/1208_cibs.csv")
    iso_1209 = pd.read_csv('data/cores/1209_cibs.csv')
    iso_607 = pd.read_csv("data/cores/607_cibs.csv")
    iso_1313 = pd.read_csv("data/cores/U1313_cibs_adj.csv")

    figure_one(save_fig=False)
    figure_two(save_fig=False)
    figure_three(save_fig=False)
    figure_s1(save_fig=False)
