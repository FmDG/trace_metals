import os

import matplotlib.pyplot as plt
import pandas as pd

import objects.met_brewer as mb
from methods.figures.tick_dirs import tick_dirs


colours = mb.Egypt


def ceara_sites(save_fig: bool = False):
    odp_925 = pd.read_csv("data/ceara_rise/925_d18O.csv").sort_values(by="age_ka")
    odp_926 = pd.read_csv("data/ceara_rise/926_d18O.csv").sort_values(by="age_ka")
    odp_927 = pd.read_csv("data/ceara_rise/927_d18O.csv").sort_values(by="age_ka")
    odp_928 = pd.read_csv("data/ceara_rise/928_d18O.csv").sort_values(by="age_ka")
    odp_929 = pd.read_csv("data/ceara_rise/929_d18O.csv").sort_values(by="age_ka")

    age_min, age_max = 2200, 3700

    fig, ax = plt.subplots(
        figsize=(9, 6.5),
        sharex='all'
    )

    ax.fill_between([2500, 2550], [1, 1], [5, 5], fc=colours[1], ec=None, alpha=0.2, label="MIS 100, 99")
    ax.fill_between([3200, 3210], [1, 1], [5, 5], fc=colours[3], ec=None, alpha=0.2, label="MIS KM5c")

    ax.plot(odp_925.age_ka, odp_925.d18O_corr, marker='+', color=colours[0], label='ODP 925')
    ax.plot(odp_929.age_ka, odp_929.d18O_corr, marker='+', color=colours[2], label='ODP 929')

    ax.set(ylabel='{} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"), xlabel='Age (ka)', xlim=[age_min, age_max], ylim=[1, 5])
    ax.invert_yaxis()
    ax.legend(frameon=False, shadow=False)

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.show()


if __name__ == "__main__":
    os.chdir("../..")
    ceara_sites(save_fig=False)
