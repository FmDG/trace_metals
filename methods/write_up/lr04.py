import os

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
import pandas as pd

from objects.args_egypt import colour


os.chdir("../..")


def plot_lr04(save_fig: bool = False):
    # Load the LR04 dataset
    d18O = pd.read_csv("data/comparisons/LR04.csv")

    d18O = d18O[d18O.age_ka.between(0, 5000)]

    # Set up the figure
    fig, ax = plt.subplots(figsize=(14, 8))

    ax.plot(d18O.age_ka, d18O.d18O, color=colour[1])
    ax.axvspan(xmin=2500, xmax=3100, fc=colour[0], ec=None, alpha=0.08)

    ax.invert_yaxis()

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set(xlabel='Age (ka)', xlim=[-10, 5010], ylabel='{} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    ax.xaxis.set_minor_locator(AutoMinorLocator(20))
    ax.yaxis.set_minor_locator(AutoMinorLocator(10))

    plt.tight_layout()
    if save_fig:
        plt.savefig("figures/LR04.png", format="png", dpi=150)
    else:
        plt.show()


if __name__ == "__main__":
    plot_lr04()
