import matplotlib.pyplot as plt

from methods.figures.tick_dirs import tick_dirs_single, tick_dirs
from methods.figures.highlight_mis import highlight_mis_single, highlight_mis
from methods.paper.plotting import isotope_plot, iso_607_plot, psu_bwt_plot, psu_d18sw_plot, psu_607_plot


def figure_1(save_fig: bool = False) -> None:
    """First figure. Showing d18O_c for 1208 and 1209 between 2400 - 3600 ka."""
    # ------------- INIT FIGURE ----------------
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=(13, 7)
    )
    highlight_mis_single(ax)
    ax = isotope_plot(ax)
    ax = tick_dirs_single(ax, min_age=2400, max_age=3600, legend=True)

    # Save the figure or show it
    if save_fig:
        plt.savefig("figures/paper/Figure_1.pdf", transparent=True)
    else:
        plt.show()


def figure_2(save_fig: bool = False) -> None:
    """Second figure. Showing d18O_c, BWT, and d18O_sw for 1208 and 1209 between 2400 - 2900 ka."""
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
    axs[0] = isotope_plot(axs[0])

    # PSU BWT estimates
    axs[1] = psu_bwt_plot(axs[1])

    # PSU d18O_sw estimates
    axs[2] = psu_d18sw_plot(axs[2])

    # ------------- FORMAT AXES -------------------
    tick_dirs(axs=axs, num_plots=3, min_age=2400, max_age=2900, legend=False)

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
        figsize=(7, 7)
    )
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    # ------------- HIGHLIGHT MIS ---------------
    highlight_mis(axs)

    # ------------- PLOT DATA -------------------
    # d18O original data
    axs[0] = isotope_plot(axs[0])
    axs[0] = iso_607_plot(axs[0])

    # PSU BWT estimates
    axs[1] = psu_bwt_plot(axs[1])
    axs[1] = psu_607_plot(axs[1])

    # ------------- FORMAT AXES ----------------
    tick_dirs(axs=axs, num_plots=2, min_age=2400, max_age=2900, legend=False)

    # Add a legend
    axs[0].legend(shadow=False, frameon=False)

    # Save the figure or show it
    if save_fig:
        plt.savefig("figures/paper/Figure_4.pdf", transparent=False)
    else:
        plt.show()
