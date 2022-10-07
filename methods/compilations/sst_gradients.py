import os

import pandas as pd
import matplotlib.pyplot as plt

from objects.colours import colours_04


def show_sst_gradients(save_fig: bool = False, min_age: int = 2200, max_age: int = 3500):

    # Error handling
    if not isinstance(save_fig, bool):
        raise ValueError("save_fig must be of type bool")

    # ---------- LOAD DATA ----------
    sst_846 = pd.read_csv("data/comparisons/alkenones/846_alkenones.csv")
    sst_1012 = pd.read_csv("data/comparisons/alkenones/1012_alkenones.csv")
    sst_1417 = pd.read_csv("data/comparisons/alkenones/1417_alkenones.csv")
    sst_1208 = pd.read_csv("data/comparisons/alkenones/1208_alkenones.csv")

    # ---------- SET PLOT ARGS ----------
    args_846 = {"color": colours_04[0], 'marker': '+', 'label': '846 (E Eq. Pacific)'}
    args_1012 = {"color": colours_04[1], 'marker': '+', 'label': '1012 (NE Pacific)'}
    args_1417 = {"color": colours_04[2], 'marker': '+', 'label': '1417 (Gulf of Alaska)'}
    args_1208 = {"color": colours_04[3], 'marker': '+', 'label': '1208 (NW Pacific)'}

    # ---------- DEFINE FIGURE ----------
    # Plots for SST and error_plus
    num_plots = 1

    fig, ax = plt.subplots(
        nrows=num_plots,
        ncols=1,
        sharex="all",
        figsize=(8, 8)
    )

    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)
    # Name the Plot
    fig.suptitle("Comparison of Pacific SST Records\n ({} - {} ka)".format(min_age, max_age))

    # PLOT 846
    ax.plot(sst_846.age_ka, sst_846.temp, **args_846)
    ax.fill_between(sst_846.age_ka, sst_846.temp_min1, sst_846.temp_plus1, color=colours_04[0], alpha=0.1)
    ax.fill_between(sst_846.age_ka, sst_846.temp_min2, sst_846.temp_plus2, color=colours_04[0], alpha=0.1)

    # PLOT 1012
    ax.plot(sst_1012.age_ka, sst_1012.temp, **args_1012)
    ax.fill_between(sst_1012.age_ka, sst_1012.temp_min1, sst_1012.temp_plus1, color=colours_04[1], alpha=0.1)
    ax.fill_between(sst_1012.age_ka, sst_1012.temp_min2, sst_1012.temp_plus2, color=colours_04[1], alpha=0.1)

    # PLOT 1417
    ax.plot(sst_1417.age_ka, sst_1417.temp, **args_1417)
    ax.fill_between(sst_1417.age_ka, sst_1417.temp_min1, sst_1417.temp_plus1, color=colours_04[2], alpha=0.1)
    ax.fill_between(sst_1417.age_ka, sst_1417.temp_min2, sst_1417.temp_plus2, color=colours_04[2], alpha=0.1)

    # PLOT 1208
    ax.plot(sst_1208.age_ka, sst_1208.SST, **args_1208)

    ax.legend(shadow=False, frameon=False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set(xlabel='Age (ka)', xlim=[min_age, max_age])

    # Save the figure if required
    if save_fig:
        plt.savefig("figures/paper/SST_01.png", format="png", dpi=300)
    else:
        plt.show()


if __name__ == '__main__':
    os.chdir("../..")
    show_sst_gradients(
        save_fig=False,
        max_age=3600,
        min_age=2200
    )
