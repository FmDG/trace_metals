import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

from methods.interpolations.generate_interpolations import generate_interpolation
from objects.colours import colours_04


def plot_SST_error_bars(ax: plt.Axes, datafile: pd.DataFrame, label: str = None, colour=colours_04[0]):
    ax.plot(datafile.age_ka, datafile.temp, marker="+", color=colour, alpha=0.7, label=label)
    ax.fill_between(datafile.age_ka, datafile.temp_min1, datafile.temp_plus1, color=colour, alpha=0.05)
    ax.fill_between(datafile.age_ka, datafile.temp_min2, datafile.temp_plus2, color=colour, alpha=0.05)
    return ax


def add_trendlines(ax: plt.Axes, age_array, value_array, colour=colours_04[0]):
    trendline = np.polyfit(age_array, value_array, 1)
    plotline = np.poly1d(trendline)
    # add trend line to plot
    ax.plot(age_array, plotline(age_array), label=None, marker=None, color=colour, ls=":")
    return ax


def show_sst_gradients(save_fig: bool = False, min_age: int = 2200, max_age: int = 3500):

    # Error handling
    if not isinstance(save_fig, bool):
        raise ValueError("save_fig must be of type bool")

    # ---------- LOAD DATA ----------
    sst_846 = pd.read_csv("data/comparisons/alkenones/846_alkenones.csv")
    sst_1012 = pd.read_csv("data/comparisons/alkenones/1012_alkenones.csv")
    sst_1417 = pd.read_csv("data/comparisons/alkenones/1417_alkenones.csv")
    sst_1208 = pd.read_csv("data/comparisons/alkenones/1208_alkenones.csv")

    # -------- INTERPOLATE DATA ------------
    interp_846, age_array = generate_interpolation(sst_846, fs=1.0, start=min_age, end=max_age, pchip=False, value="temp")
    interp_1012, _ = generate_interpolation(sst_1012, fs=1.0, start=min_age, end=max_age, pchip=False, value="temp")
    interp_1417, _ = generate_interpolation(sst_1417, fs=1.0, start=min_age, end=max_age, pchip=False, value="temp")
    interp_1208, _ = generate_interpolation(sst_1208, fs=1.0, start=min_age, end=max_age, pchip=False, value="temp")

    # -------- DEFINE PLOT AREA -------------
    num_plots = 2
    fig, axs = plt.subplots(1, num_plots, sharey="all", sharex="all")
    # Name the Plot
    fig.suptitle("Comparison of Pacific Alkenone SST Records\n ({} - {} ka)".format(min_age, max_age))
    fig.subplots_adjust(left=0.10, right=0.90, bottom=0.10, top=0.90, wspace=0.05)

    # -------- PLOT VALUES -----------
    axs[0] = plot_SST_error_bars(axs[0], sst_846, "846 (E Eq. Pacific)", colours_04[0])
    axs[0] = plot_SST_error_bars(axs[0], sst_1012, "1012 (NE Pacific)", colours_04[1])
    axs[0] = plot_SST_error_bars(axs[0], sst_1208, "1208 (NW Pacific)", colours_04[2])
    axs[0] = plot_SST_error_bars(axs[0], sst_1417, "U1417 (Gulf of Alaska)", colours_04[3])

    # ------------ ADD TRENDLINES --------------
    axs[0] = add_trendlines(axs[0], age_array, interp_846, colours_04[0])
    axs[0] = add_trendlines(axs[0], age_array, interp_1012, colours_04[1])
    # axs[0] = add_trendlines(axs[0], age_array, interp_1208, colours_04[2])
    axs[0] = add_trendlines(axs[0], age_array, interp_1417, colours_04[3])

    # ---------- PLOT INTERPOLATIONS -----------
    axs[1].plot(age_array, (interp_1012 - interp_1417), marker=None, color=colours_04[0], label="1012 - U1417")
    axs[1].plot(age_array, (interp_846 - interp_1012), marker=None, color=colours_04[1], label="846 - 1012")
    axs[1].plot(age_array, (interp_846 - interp_1417), marker=None, color=colours_04[2], label="846 - U1417")

    # ------------ ADD TRENDLINES --------------
    axs[1] = add_trendlines(axs[1], age_array, (interp_1012 - interp_1417), colours_04[0])
    axs[1] = add_trendlines(axs[1], age_array, (interp_846 - interp_1012), colours_04[1])
    axs[1] = add_trendlines(axs[1], age_array, (interp_846 - interp_1417), colours_04[2])

    for ax in axs:
        ax.legend(frameon=False, shadow=False)
        ax.spines['top'].set_visible(False)
        ax.xaxis.set_minor_locator(AutoMinorLocator(20))
        ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    axs[0].set(ylabel="SST ({})".format(u'\N{DEGREE SIGN}C'), xlabel="Age (ka)", title="Absolute SSTs")
    axs[1].set(ylabel="{}SST ({})".format(r'$\Delta$', u'\N{DEGREE SIGN}C'), xlabel="Age (ka)", xlim=(min_age, max_age), title="SST gradients")
    axs[0].spines['right'].set_visible(False)
    axs[1].spines['left'].set_visible(False)
    axs[1].yaxis.set(ticks_position="right", label_position='right')


    # Save the figure if required
    if save_fig:
        plt.savefig("figures/paper/SST_01.png", format="png", dpi=300)
    else:
        plt.show()


if __name__ == '__main__':
    os.chdir("../..")
    show_sst_gradients(
        save_fig=False,
        max_age=3500,
        min_age=2300
    )
