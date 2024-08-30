import matplotlib.pyplot as plt

from methods.figures.tick_dirs import tick_dirs
from methods.figures.highlight_mis import highlight_all_mis_greyscale

from methods.paper.analysis import resampled_data, rolling_corr_SST_d18O, resampled_SST_1208


def visualise_data():
    fig, axs = plt.subplots(
        nrows=3,
        sharex='all'
    )
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    for ax in axs:
        highlight_all_mis_greyscale(ax)

    axs[0].plot(resampled_SST_1208.age_ka, resampled_SST_1208.difference_SST)
    axs[1].plot(resampled_data.age_ka, resampled_data.difference_d18O)
    axs[2].plot(rolling_corr_SST_d18O.age_ka, rolling_corr_SST_d18O.r ** 2)

    axs[0].set(ylabel=r'$\Delta$SST')
    axs[1].set(ylabel=r'$\Delta \delta^{18}$O')
    axs[2].set(ylabel=r'$r^{2}$', ylim=[0, 1])

    tick_dirs(axs, 3, 2500, 3300, False)

    plt.show()


if __name__ == "__main__":
    visualise_data()