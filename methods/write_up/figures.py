"""
Plotting up all the figures for the paper.
"""

import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

import objects.args_brewer as args
from methods.figures.tick_dirs import tick_dirs, tick_dirs_both
from methods.interpolations.generate_interpolations import generate_interpolation
from objects.core_data.isotopes import iso_607, iso_1208, iso_1209
from objects.core_data.psu import psu_1208, psu_1209, psu_607


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
    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args.args_1208)

    # PSU BWT estimates
    axs[1].plot(psu_1208.age_ka, psu_1208.temp, **args.args_1208)
    axs[1].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, **args.fill_1208)

    # PSU d18O_sw estimates
    axs[2].plot(psu_1208.age_ka, psu_1208.d18O_sw, **args.args_1208)
    axs[2].fill_between(psu_1208.age_ka, psu_1208.d18O_min1, psu_1208.d18O_plus1, **args.fill_1208)

    # -- Plot the 1209 data --
    # d18O original data
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args.args_1209)
    # PSU BWT estimates
    axs[1].plot(psu_1209.age_ka, psu_1209.temp, **args.args_1209)
    axs[1].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, **args.fill_1209)
    # PSU d18O_sw estimates
    axs[2].plot(psu_1209.age_ka, psu_1209.d18O_sw, **args.args_1209)
    axs[2].fill_between(psu_1209.age_ka, psu_1209.d18O_min1, psu_1209.d18O_plus1, **args.fill_1209)

    # -- Define the axes --
    axs[0].set(ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[1].set(ylabel="BWT ({})".format(u'\N{DEGREE SIGN}C'))
    axs[2].set(ylabel='Modelled {} ({} VPDB)'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))

    # Invert the axes with d18O
    axs[0].invert_yaxis()
    axs[2].invert_yaxis()

    # Decide which Tick Directions function you want to run.
    # tick_dirs_both(axs, num_plots, min_age, max_age)
    tick_dirs(axs, num_plots, min_age, max_age)

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
    axs[0].plot(psu_1208.age_ka, psu_1208.temp, **args.args_1208)
    axs[0].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, **args.fill_1208)
    # PSU d18O_sw estimates
    axs[2].plot(psu_1208.age_ka, psu_1208.d18O_sw, **args.args_1208)
    axs[2].fill_between(psu_1208.age_ka, psu_1208.d18O_min1, psu_1208.d18O_plus1, **args.fill_1208)

    # -- Plot the 1209 data --
    # PSU BWT estimates
    axs[0].plot(psu_1209.age_ka, psu_1209.temp, **args.args_1209)
    axs[0].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, **args.fill_1209)
    # PSU d18O_sw estimates
    axs[2].plot(psu_1209.age_ka, psu_1209.d18O_sw, **args.args_1209)
    axs[2].fill_between(psu_1209.age_ka, psu_1209.d18O_min1, psu_1209.d18O_plus1, **args.fill_1209)

    # Plot the differences in d18O
    axs[1].plot(age_array, differences, **args.args_diff)
    axs[1].plot(age_array, filtered_diff, **args.args_filt)
    axs[1].fill_between(age_array, filtered_diff, **args.fill_diff)

    # -- Define the axes --
    axs[0].set(ylabel="BWT ({})".format(u'\N{DEGREE SIGN}C'))
    axs[1].set(ylabel="{} (VPDB {})".format(r'$\Delta \delta^{18}$O ', u"\u2030"))
    axs[2].set(ylabel='Modelled {} ({} VPDB)'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))

    # Invert the axes with d18O
    axs[1].invert_yaxis()
    axs[2].invert_yaxis()

    # Decide which Tick Directions function you want to run.
    # tick_dirs_both(axs, num_plots, min_age, max_age)
    tick_dirs(axs, num_plots, min_age, max_age)

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
    # fig.suptitle("Global Context\n ({} - {} ka)".format(min_age, max_age))

    # -- Plot the 1208 data --
    # PSU BWT estimates
    axs[0].plot(psu_1208.age_ka, psu_1208.temp, **args.args_1208)
    axs[0].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, **args.fill_1208)
    # d18O isotope plot
    axs[1].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args.args_1208)

    # -- Plot the 1209 data --
    # PSU BWT estimates
    axs[0].plot(psu_1209.age_ka, psu_1209.temp, **args.args_1209)
    axs[0].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, **args.fill_1209)
    # d18O isotope plot
    axs[1].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args.args_1209)

    # -- Plot the 607 data --
    # PSU BWT estimates
    axs[0].plot(psu_607.age_ka, psu_607.temp, **args.args_607)
    axs[0].fill_between(psu_607.age_ka, psu_607.temp_min1, psu_607.temp_plus1, **args.fill_607)
    # d18O isotope plot
    axs[1].plot(iso_607.age_ka, iso_607.d18O, **args.args_607)

    # -- Define the axes --
    axs[0].set(ylabel="BWT ({})".format(u'\N{DEGREE SIGN}C'))
    axs[1].set(ylabel="{} (VPDB {})".format(r'$\delta^{18}$O', u"\u2030"))

    # Invert the axes with d18O
    axs[1].invert_yaxis()

    # Decide which Tick Directions function you want to run.
    # tick_dirs_both(axs, num_plots, min_age, max_age)
    tick_dirs(axs, num_plots, min_age, max_age)

    # Save the figure if required
    if save_fig:
        plt.savefig("figures/paper/Figure_3.png".format(min_age, max_age), format="png", dpi=300)
    else:
        plt.show()

    return 1


if __name__ == "__main__":
    figure_one(save_fig=False)
    figure_two(save_fig=False)
    figure_three(save_fig=False)
