import matplotlib.pyplot as plt

from methods.compilations.ceara_rise import colours
from methods.figures.tick_dirs import tick_dirs, tick_dirs_single
from methods.figures.highlight_mis import highlight_mis, highlight_all_mis_greyscale
from methods.paper.plotting import (isotope_plot, iso_607_plot, psu_bwt_plot, psu_d18sw_plot, psu_607_plot, opal_plot,
                                    alkenone_plot, alkenone_gradient_plot, sea_level_plot, filtered_difference_plot,
                                    pearson_significance_plot_sea_level, pearson_correlation_plot_sea_level,
                                    difference_plot_glacials, average_difference_plot, difference_plot,
                                    planktic_difference_plot, isotope_plot_1207,
                                    alkenone_gradient_plot_glacial_interglacials, difference_temperature_plot,
                                    difference_d18Osw_plot, probStack_plot)


def figure_1(save_fig: bool = False) -> None:
    """First figure. Showing d18O_c for 1208 and 1209 between 2400 - 3600 ka."""
    # ------------- INIT FIGURE ----------------
    fig, axs = plt.subplots(
        nrows=2,
        ncols=1,
        figsize=(12, 7.3),
        sharex="all"
    )
    fig.subplots_adjust(hspace=0)
    highlight_all_mis_greyscale(axs[0])
    highlight_all_mis_greyscale(axs[1])
    axs[0] = isotope_plot(axs[0])
    axs[1] = filtered_difference_plot(axs[1], left=1)
    # axs[0].legend(frameon=False)
    tick_dirs(axs, num_plots=2, min_age=2400, max_age=3400, legend=True)

    # Save the figure or show it
    if save_fig:
        plt.savefig("figures/paper/Figure_1.pdf", transparent=False)
    else:
        plt.show()


def figure_1_simple(save_fig: bool = False) -> None:
    """First figure. Showing d18O_c for 1208 and 1209 between 2400 - 3600 ka."""
    # ------------- INIT FIGURE ----------------
    fig, ax = plt.subplots(
        figsize=(12, 5),
        sharex="all"
    )
    fig.subplots_adjust(hspace=0)
    highlight_all_mis_greyscale(ax)
    ax = isotope_plot(ax)
    tick_dirs_single(ax, min_age=2400, max_age=3400, legend=True)

    # Save the figure or show it
    if save_fig:
        plt.savefig("figures/paper/Figure_1_Simple.pdf", transparent=False)
    else:
        plt.show()


def figure_2(save_fig: bool = False) -> None:
    """Second figure. Showing d18O_c, BWT, and d18O_sw for 1208 and 1209 between 2400 - 2900 ka."""
    # ------------- INIT FIGURE ----------------
    n_plots = 3
    fig, axs = plt.subplots(
        nrows=n_plots,
        ncols=1,
        sharex="all",
        figsize=(6, 9)
    )
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    # ------------- HIGHLIGHT MIS ---------------
    for ax in axs:
        highlight_all_mis_greyscale(ax)

    # ------------- PLOT DATA -------------------
    # d18O original data
    axs[0] = isotope_plot(axs[0])

    # PSU BWT estimates
    axs[1] = psu_bwt_plot(axs[1])

    # PSU d18O_sw estimates
    axs[2] = psu_d18sw_plot(axs[2])

    # ------------- FORMAT AXES -------------------
    tick_dirs(axs=axs, num_plots=n_plots, min_age=2450, max_age=2850, legend=False)

    # Add a legend
    axs[0].legend(shadow=False, frameon=False)

    # Save the figure or show it
    if save_fig:
        plt.savefig("figures/paper/Figure_2.pdf", transparent=False)
    else:
        plt.show()


# THIRD FIGURE IS A SCHEMATIC MADE IN INKSCAPE

def figure_4(save_fig: bool = False) -> None:
    """Fourth figure. Showing d18O_c and BWT for 1208, 1209 and 607 between 2400 - 2900 ka."""
    # ------------- INIT FIGURE ----------------
    fig, axs = plt.subplots(
        nrows=2,
        ncols=1,
        sharex="all",
        figsize=(6, 7)
    )
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    # ------------- HIGHLIGHT MIS ---------------
    for ax in axs:
        highlight_all_mis_greyscale(ax)

    # ------------- PLOT DATA -------------------
    # d18O original data
    axs[0] = isotope_plot(axs[0])
    axs[0] = iso_607_plot(axs[0])

    # PSU BWT estimates
    axs[1] = psu_bwt_plot(axs[1])
    axs[1] = psu_607_plot(axs[1])

    # ------------- FORMAT AXES ----------------
    tick_dirs(axs=axs, num_plots=2, min_age=2450, max_age=2850, legend=False)

    # Add a legend
    axs[0].legend(shadow=False, frameon=False)

    # Save the figure or show it
    if save_fig:
        plt.savefig("figures/paper/Figure_4.pdf", transparent=False)
    else:
        plt.show()


def figure_1_opal_variant(save_fig: bool = False) -> None:
    """First figure. Showing d18O_c for 1208 and 1209 between 2400 - 3600 ka."""
    # ------------- INIT FIGURE ----------------
    fig, axs = plt.subplots(
        nrows=2,
        ncols=1,
        figsize=(13, 9),
        sharex="all"
    )
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    highlight_mis(axs)
    axs[0] = isotope_plot(axs[0])
    axs[1] = opal_plot(axs[1], colour="k")
    tick_dirs(axs, num_plots=2, min_age=2400, max_age=3600, legend=True)

    # Save the figure or show it
    if save_fig:
        plt.savefig("figures/paper/Figure_1_opal.pdf", transparent=True)
    else:
        plt.show()

def figure_s4(save_fig: bool = False) -> None:
    """Figure showing the difference in d18O with age"""
    n_plots = 2
    fig, axs = plt.subplots(
        nrows=n_plots,
        ncols=1,
        figsize=(12, 8),
        sharex="all"
    )
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    highlight_mis(axs)
    axs[0] = isotope_plot(axs[0])
    axs[1] = filtered_difference_plot(axs[1], left=1)
    tick_dirs(axs, num_plots=n_plots, min_age=2400, max_age=3400, legend=True)

    # Save the figure or show it
    if save_fig:
        plt.savefig("figures/paper/Figure_S4.pdf", transparent=False)
    else:
        plt.show()


def figure_alkenone_SSTs(save_fig: bool = False) -> None:
    """Figure showing the Alkenone SST gradient"""
    n_plots = 4
    fig, axs = plt.subplots(
        nrows=n_plots,
        ncols=1,
        figsize=(10, 14),
        sharex="all"
    )
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    for ax in axs:
        highlight_all_mis_greyscale(ax)
    axs[0] = alkenone_plot(axs[0])
    axs[1] = alkenone_gradient_plot(axs[1])
    axs[2] = filtered_difference_plot(axs[2], left=2)
    axs[3] = alkenone_gradient_plot_glacial_interglacials(axs[3])
    axs[0].legend(frameon=False)
    tick_dirs(axs, num_plots=n_plots, min_age=2400, max_age=2900, legend=False)

    # Save the figure or show it
    if save_fig:
        plt.savefig("figures/paper/Figure_ALKENONE_SST.pdf", transparent=False)
    else:
        plt.show()


def figure_sea_level_correlation(save_fig: bool = False) -> None:
    # Calculates the rolling correlation between difference in d18O and Sea Levels
    num_rows = 4
    fig, axs = plt.subplots(
        nrows=num_rows,
        sharex="all",
        figsize=(10, 10)
    )
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    # --------------- HIGHLIGHT SECTIONS ---------------
    for ax in axs:
        highlight_all_mis_greyscale(ax)
    # --------------- PLOT FIGURE ---------------
    axs[0] = sea_level_plot(axs[0], colour="k")  # Sea Level Plot
    axs[1] = filtered_difference_plot(axs[1], left=1)  # Filtered difference plot
    axs[2] = pearson_correlation_plot_sea_level(axs[2])  # Correlation Plot
    axs[3] = pearson_significance_plot_sea_level(axs[3])  # Significance Plot

    tick_dirs(axs, num_plots=num_rows, min_age=2400, max_age=3400, legend=False)

    # --------------- EXPORT FIGURE ---------------
    if save_fig:
        plt.savefig("figures/paper/figure_sea_level_correlation.pdf", format='pdf', transparent=False)
    else:
        plt.show()


def figure_glacial_interglacial_diff(save_fig: bool = False) -> None:
    """Showing d18O_c, BWT, and difference for glacials and interglacials for 1208 and 1209 between 2400 - 2900 ka."""
    # ------------- INIT FIGURE ----------------
    fig, axs = plt.subplots(
        nrows=3,
        ncols=1,
        sharex="all",
        figsize=(7, 18)
    )
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    # ------------- HIGHLIGHT MIS ---------------
    for ax in axs:
        highlight_all_mis_greyscale(ax)

    # ------------- PLOT DATA -------------------
    # d18O original data
    axs[0] = isotope_plot(axs[0])

    # PSU BWT estimates
    axs[1] = psu_bwt_plot(axs[1])

    # PSU d18O_sw estimates
    axs[2] = difference_plot_glacials(axs[2], left=2)


    # ------------- FORMAT AXES -------------------
    tick_dirs(axs=axs, num_plots=3, min_age=2450, max_age=2950, legend=False)

    # Add a legend
    axs[0].legend(shadow=False, frameon=False)

    # Save the figure or show it
    if save_fig:
        plt.savefig("figures/paper/Figure_GLACIAL_DIFF.pdf", transparent=False)
    else:
        plt.show()


def figure_average_diff(save_fig: bool = False) -> None:
    """Showing d18O and AVG diff for 1208 and 1209 between 2400 - 3400 ka."""
    # ------------- INIT FIGURE ----------------
    fig, axs = plt.subplots(
        nrows=2,
        ncols=1,
        sharex="all",
        figsize=(12, 8)
    )
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    # ------------- HIGHLIGHT MIS ---------------
    for ax in axs:
        highlight_all_mis_greyscale(ax)

    # ------------- PLOT DATA -------------------
    # d18O original data
    axs[0] = isotope_plot(axs[0])
    # PSU BWT estimates
    axs[1] = average_difference_plot(axs[1], start=2800, end=3300)

    # ------------- FORMAT AXES -------------------
    tick_dirs(axs=axs, num_plots=2, min_age=2400, max_age=3400, legend=True)

    # Save the figure or show it
    if save_fig:
        plt.savefig("figures/paper/Figure_AVERAGE_DIFF.pdf", transparent=False)
    else:
        plt.show()


def figure_bwt_long(save_fig: bool = False) -> None:
    # ------------- INIT FIGURE ----------------
    fig, axs = plt.subplots(
        nrows=2,
        ncols=1,
        sharex="all",
        figsize=(10, 7)
    )
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    # ------------- HIGHLIGHT MIS ---------------
    for ax in axs:
        highlight_all_mis_greyscale(ax)

    # ------------- PLOT FIGURES -------------
    axs[0] = isotope_plot(axs[0])
    axs[1] = psu_bwt_plot(axs[1])

    tick_dirs(axs, 2, min_age=2400, max_age=3400, legend=False)

    # ------------- EXPORT FIGURES -------------
    # Save the figure or show it
    if save_fig:
        plt.savefig("figures/paper/Figure BWT LONG.pdf", transparent=False)
    else:
        plt.show()


def figure_planktics(save_fig: bool = False) -> None:
    # ------------- INIT FIGURE ----------------
    n_plots = 3
    fig, axs = plt.subplots(
        nrows=n_plots,
        ncols=1,
        sharex="all",
        figsize=(10, 7)
    )
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    # ------------- HIGHLIGHT MIS ---------------
    for ax in axs:
        highlight_all_mis_greyscale(ax)

    # ------------- PLOT FIGURES -------------
    axs[0] = isotope_plot(axs[0])
    axs[1] = planktic_difference_plot(axs[1])
    axs[2] = psu_bwt_plot(axs[2])

    tick_dirs(axs, n_plots, min_age=2400, max_age=2900, legend=True)

    # ------------- EXPORT FIGURES -------------
    # Save the figure or show it
    if save_fig:
        plt.savefig("figures/paper/Figure PLANKTICS PSU.pdf", transparent=False)
    else:
        plt.show()


def figure_s8(save_fig: bool = False) -> None:
    # ------------- INIT FIGURE ----------------
    n_plots = 4
    fig, axs = plt.subplots(
        nrows=n_plots,
        ncols=1,
        sharex="all",
        figsize=(10, 8)
    )
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    # ------------- HIGHLIGHT MIS ---------------
    for ax in axs:
        highlight_all_mis_greyscale(ax)

    # ------------- PLOT FIGURES -------------
    axs[0] = psu_bwt_plot(axs[0])
    axs[1] = difference_temperature_plot(axs[1], colour=colours[1])
    axs[2] = psu_d18sw_plot(axs[2])
    axs[3] = difference_d18Osw_plot(axs[3], colour=colours[0])
    tick_dirs(axs, n_plots, min_age=2400, max_age=2900, legend=True)

    # ------------- EXPORT FIGURES -------------
    # Save the figure or show it
    if save_fig:
        plt.savefig("figures/paper/Figure BWT Gradient.pdf", transparent=False)
    else:
        plt.show()



if __name__ == "__main__":
    pass
