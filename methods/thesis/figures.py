import matplotlib.pyplot as plt

from plots import (bwt_plot_1209, d18o_sw_plot_1209, isotope_plot)
from methods.figures.tick_dirs import tick_dirs
from methods.figures.highlight_mis import highlight_all_mis_greyscale
from objects.arguments.args_Nature import colours as colour

def figure_1209_only(save_fig: bool = False) -> None:
    n_plots = 2
    fig, axs = plt.subplots(
        nrows=n_plots,
        sharex="all",
        figsize=(12, 8)
    )

    for ax in axs:
        highlight_all_mis_greyscale(ax)

    fig.subplots_adjust(hspace=0)

    axs[0] = bwt_plot_1209(axs[0], colour=colour[0])
    axs[1] = d18o_sw_plot_1209(axs[1], colour=colour[1])

    tick_dirs(axs, n_plots, min_age=2400, max_age=2850, legend=False)

    if save_fig:
        plt.savefig("figures/thesis/Figure_1209_only.png", format="png", dpi=300)
    else:
        plt.show()


def figure_1209_1208_d18O(save_fig: bool = False) -> None:
    fig, ax = plt.subplots(
        nrows=1,
        sharex="all",
        figsize=(19, 8)
    )

    highlight_all_mis_greyscale(ax)

    ax = isotope_plot(ax)
    ax.set(xlabel="Age (ka)", xlim=[2400, 3600])

    if save_fig:
        plt.savefig("figures/thesis/Figure_1209_1208_d18O.png", format="png", dpi=300)
    else:
        plt.show()


if __name__ == "__main__":
    # figure_1209_only(save_fig=False)
    # figure_1209_1208_d18O(save_fig=True)
    pass