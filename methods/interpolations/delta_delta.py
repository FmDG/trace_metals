import os

import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import savgol_filter, periodogram

from objects.args_Nature import args_1209, args_1208, args_diff, fill_diff
from methods.figures.tick_dirs import tick_dirs
from generate_interpolations import generate_interpolation


def interpolate_isotopes(age_min: int = 2300, age_max: int = 3600, save_fig: bool = False):

    # Load the datasets
    site_1208 = pd.read_csv('data/cores/1208_cibs.csv')
    site_1209 = pd.read_csv('data/cores/1209_cibs.csv')

    ## Use Pandas rolling function to get a rolling mean of size n ka
    n = 3

    # We can use two different interpolation techniques - the first is a simple 1D interpolation, the second is a
    # PChip interpolation

    interp_1208, age_array = generate_interpolation(site_1208, fs=5, start=age_min, end=age_max, pchip=False)
    interp_1209, _ = generate_interpolation(site_1209, fs=5, start=age_min, end=age_max, pchip=False)

    # Filter pchip function
    filtered_diff = savgol_filter((interp_1208 - interp_1209), 201, 3)

    fig, axs = plt.subplots(2, sharex="all", figsize=(15, 7))
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    axs[0].plot(site_1208.age_ka, site_1208.d18O_unadj, **args_1208)
    axs[0].plot(site_1209.age_ka, site_1209.d18O_unadj, **args_1209)
    axs[0].set(ylabel='Benthic {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))

    axs[1].plot(age_array, (interp_1208 - interp_1209), **args_diff)
    # axs[1].plot(age_array, filtered_diff, label="20 ka Filter", c='k')
    axs[1].set(xlabel="Age (ka)", ylabel="Difference in {} ({})".format(r'$\delta^{18}$O', u"\u2030"),
               xlim=[age_min, age_max])

    tick_dirs(axs, num_plots=2, min_age=age_min, max_age=age_max, legend=True)

    for ax in axs:
        ax.invert_yaxis()

    # Adds horizontal 0 line
    axs[1].axhline(0, ls='--', color='k')

    # Fills in the gap between the line and the 0 axis
    axs[1].fill_between(age_array, (interp_1208 - interp_1209), **fill_diff)
    # axs[1].fill_between(age_array, filtered_diff, 0, color=clr[2], alpha=0.2)


    if save_fig:
        plt.savefig("figures/paper/Figure_S4.png", format="png", dpi=300)
    else:
        plt.show()


if __name__ == "__main__":
    os.chdir('../..')
    interpolate_isotopes(
        age_min=2350,
        age_max=3500,
        save_fig=False
    )
