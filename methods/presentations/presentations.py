import methods.presentations.plots as plotting
import matplotlib.pyplot as plt
from methods.figures.highlight_mis import highlight_all_mis_greyscale
from methods.figures.tick_dirs import tick_dirs, tick_dirs_single


def iso_1208_1209_figure(save_fig: bool = False) -> None:
    fig, ax = plt.subplots(
        nrows=1,
        sharex="all",
        figsize=(10, 5)
    )

    highlight_all_mis_greyscale(ax)

    ax = plotting.isotope_plot(ax)
    tick_dirs_single(ax, 2800, 3200, True)

    if save_fig:
        plt.savefig("figures/presentations/Figure_1209_1208_d18O.png", format="png", dpi=300)
    else:
        plt.show()


def psu_1208_1209_figure(save_fig: bool = False) -> None:
    n_plots = 3
    fig, axs = plt.subplots(
        nrows=n_plots,
        sharex="all",
        figsize=(8, 6)
    )
    fig.subplots_adjust(hspace=0)

    for ax in axs:
        highlight_all_mis_greyscale(ax)


    axs[0] = plotting.isotope_plot(axs[0])
    axs[1] = plotting.psu_bwt_plot(axs[1])
    axs[2] = plotting.psu_d18sw_plot(axs[2])

    tick_dirs(axs, n_plots, 2500, 2900, False)
    # axs[0].legend(frameon=False)

    if save_fig:
        plt.savefig("figures/presentations/Figure_1209_1208_psu_all.png", format="png", dpi=300)
    else:
        plt.show()


def probstack_figure(save_fig: bool = False) -> None:
    fig, ax = plt.subplots(
        nrows=1,
        sharex="all",
        figsize=(8, 4)
    )

    ax = plotting.probStack_plot(ax)
    tick_dirs_single(ax, 0, 4000, False)

    if save_fig:
        plt.savefig("figures/presentations/Figure_probstack_d18O.png", format="png", dpi=300)
    else:
        plt.show()


if __name__ == "__main__":
    iso_1208_1209_figure(save_fig=False)
    # psu_1208_1209_figure(save_fig=True)
    # probstack_figure(save_fig=False)
