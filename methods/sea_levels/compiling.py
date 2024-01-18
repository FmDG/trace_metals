import matplotlib.pyplot as plt

from methods.figures.tick_dirs import tick_dirs
from methods.figures.highlight_mis import highlight_all_mis
from methods.sea_levels.plotting import isotope_plot, sea_level_correlation_plot, difference_plot, filtered_difference_plot, sea_level_correlation_significance_plot, sea_level_plot


def sea_level_isotope_comparison(save_fig: bool = False) -> None:
    n_plots = 3
    fig, axs = plt.subplots(nrows=n_plots, figsize=(12, 12), sharex="all")
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    axs[0] = isotope_plot(axs[0])
    axs[1] = filtered_difference_plot(axs[1], colour="k")
    axs[2] = sea_level_plot(axs[2], colour="k")
    tick_dirs(axs, min_age=2400, max_age=3400, legend=True, num_plots=n_plots)
    # Save the figure or show it
    if save_fig:
        plt.savefig("figures/paper/sea_level.pdf", transparent=False)
    else:
        plt.show()


def sea_level_correlation(filter_period: float = 4.0, save_fig: bool = False):
    # --------------- INITIALISE FIGURE ---------------
    num_rows = 5
    fig, axs = plt.subplots(nrows=num_rows, sharex="all", figsize=(12, 16))
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)
    axs[0] = sea_level_plot(axs[0], age_min=2400, age_max=3400, colour="k")
    axs[1] = difference_plot(axs[1], colour="k")
    axs[2] = filtered_difference_plot(axs[2], colour="k")
    axs[3] = sea_level_correlation_plot(axs[3], colour="k")
    axs[4] = sea_level_correlation_significance_plot(axs[4], colour="k")

    tick_dirs(axs, num_plots=num_rows, min_age=2400, max_age=3400, legend=False)

    # --------------- EXPORT FIGURE ---------------
    if save_fig:
        plt.savefig("figures/paper/sea_level_correlation.pdf", format='pdf')
    else:
        plt.show()



if __name__ == "__main__":
    sea_level_isotope_comparison(save_fig=False)
    sea_level_correlation(save_fig=False)