"""
Plotting up all the figures for the paper.
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

import objects.args_Nature as args_Nat
from methods.figures.tick_dirs import tick_dirs
from methods.figures.highlight_mis import highlight_mis
from objects.core_data.isotopes import iso_607, iso_1208, iso_1209
from objects.core_data.psu import psu_1208, psu_1209, psu_607


def figure_1(save_fig: bool = False):
    """
    First figure. Showing d18O_c for 1208 and 1209 between 2400 - 3600 ka.
    Highlighted are MIS G4 (blue) and MIS 99 (red).
    :param save_fig: Decision to save the figure as Figure_1.svg
    :return: No return
    """

    # ------------- INIT FIGURE ----------------
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=(13, 7)
    )

    # ------------- HIGHLIGHT MIS ---------------
    # Highlight MIS G4 (2.681 - 2.69 Ma)
    ax.axvspan(
        xmin=2681,
        xmax=2690,
        ec=None,
        fc="blue",
        alpha=0.1
    )

    # ------------- PLOT DATA -------------------
    # d18O original data
    ax.plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_Nat.args_1208)
    ax.plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_Nat.args_1209)

    # ------------- FORMAT AXES ----------------
    # -- Label the axis --
    ax.set(
        ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"),
        xlabel="Age (ka)",
        xlim=[2400, 3600]
    )
    # Invert the axis
    ax.invert_yaxis()

    # Add a legend
    ax.legend(shadow=False, frameon=False)

    # Add the spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_minor_locator(AutoMinorLocator(20))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))

    # Save the figure or show it
    if save_fig:
        plt.savefig("figures/paper/Figure_1.pdf", transparent=True)
    else:
        plt.show()


def figure_2(save_fig: bool = False):
    """
    Second figure. Showing d18O_c, BWT, and d18O_sw for 1208 and 1209 between 2400 - 2900 ka.
    Highlighted are MIS G4 (blue) and MIS 99 (red).
    :param save_fig: Decision to save the figure as Figure_2.svg
    :return: No return
    """

    # ------------- INIT FIGURE ----------------
    fig, axs = plt.subplots(
        nrows=3,
        ncols=1,
        sharex="all",
        figsize=(7, 12)
    )

    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    # ------------- HIGHLIGHT MIS ---------------
    highlight_mis(axs)

    # ------------- PLOT DATA -------------------
    # d18O original data
    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_Nat.args_1208)
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_Nat.args_1209)

    # PSU BWT estimates
    axs[1].plot(psu_1208.age_ka, psu_1208.temp, **args_Nat.args_1208)
    axs[1].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, **args_Nat.fill_1208)
    axs[1].plot(psu_1209.age_ka, psu_1209.temp, **args_Nat.args_1209)
    axs[1].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, **args_Nat.fill_1209)

    # PSU d18O_sw estimates
    axs[2].plot(psu_1208.age_ka, psu_1208.d18O_sw, **args_Nat.args_1208)
    axs[2].fill_between(psu_1208.age_ka, psu_1208.d18O_min1, psu_1208.d18O_plus1, **args_Nat.fill_1208)
    axs[2].plot(psu_1209.age_ka, psu_1209.d18O_sw, **args_Nat.args_1209)
    axs[2].fill_between(psu_1209.age_ka, psu_1209.d18O_min1, psu_1209.d18O_plus1, **args_Nat.fill_1209)

    # ------------- FORMAT AXES ----------------
    # -- Label the axis --
    axs[0].set(ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[1].set(ylabel='BWT Estimate ({})'.format(u'\N{DEGREE SIGN}C'))
    axs[2].set(ylabel='Derived {} ({} VPDB)'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))

    # Invert the axes
    axs[0].invert_yaxis()
    axs[2].invert_yaxis()

    tick_dirs(axs=axs, num_plots=3, min_age=2400, max_age=2900, legend=False)

    # Add a legend
    axs[0].legend(shadow=False, frameon=False)

    # Save the figure or show it
    if save_fig:
        plt.savefig("figures/paper/Figure_2.pdf", transparent=False)
    else:
        plt.show()


# THIRD FIGURE IS A SCHEMATIC MADE IN INKSCAPE

def figure_4(save_fig: bool = False):
    """
    Fourth figure. Showing d18O_c and BWT for 1208, 1209 and 607 between 2400 - 2900 ka.
    Highlighted are MIS G4 (blue) and MIS 99 (red).
    :param save_fig: Decision to save the figure as Figure_4.svg
    :return: No return
    """

    # ------------- INIT FIGURE ----------------
    fig, axs = plt.subplots(
        nrows=2,
        ncols=1,
        sharex="all",
        figsize=(7, 7)
    )

    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    # ------------- HIGHLIGHT MIS ---------------
    highlight_mis(axs)

    # ------------- PLOT DATA -------------------
    # d18O original data
    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_Nat.args_1208)
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_Nat.args_1209)
    axs[0].plot(iso_607.age_ka, iso_607.d18O, **args_Nat.args_607)

    # PSU BWT estimates
    axs[1].plot(psu_1208.age_ka, psu_1208.temp, **args_Nat.args_1208)
    axs[1].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, **args_Nat.fill_1208)
    axs[1].plot(psu_1209.age_ka, psu_1209.temp, **args_Nat.args_1209)
    axs[1].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, **args_Nat.fill_1209)
    axs[1].plot(psu_607.age_ka, psu_607.temp, **args_Nat.args_607)
    axs[1].fill_between(psu_607.age_ka, psu_607.temp_min1, psu_607.temp_plus1, **args_Nat.fill_607)

    # ------------- FORMAT AXES ----------------
    # -- Label the axis --
    axs[0].set(ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[1].set(ylabel='BWT Estimate ({})'.format(u'\N{DEGREE SIGN}C'))

    # Invert the axes
    axs[0].invert_yaxis()

    tick_dirs(axs=axs, num_plots=2, min_age=2400, max_age=2900, legend=False)

    # Add a legend
    axs[0].legend(shadow=False, frameon=False)

    # Save the figure or show it
    if save_fig:
        plt.savefig("figures/paper/Figure_4.pdf", transparent=False)
    else:
        plt.show()


if __name__ == "__main__":
    figure_1(save_fig=True)
    figure_2(save_fig=True)
    figure_4(save_fig=True)
