import os

import matplotlib.pyplot as plt
import pandas as pd

from methods.figures.tick_dirs import tick_dirs


def bwt_from_mgca(x):
    return (x - 0.9) / 0.1


def mgca_from_bwt(x):
    return 0.9 + (0.1 * x)


def core_top_comparison(save_fig: bool = False) -> None:
    os.chdir("../..")
    combined = pd.read_csv("data/comparisons/core_top_combined.csv")
    combined = combined.sort_values(by="age_ka_mbsf")

    fig, axs = plt.subplots(nrows=2, sharex="all", figsize=(12, 7))
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    axs[0].scatter(combined.age_ka_mbsf, combined.d18O_1208, label="1208", marker="+")
    axs[0].scatter(combined.age_ka_mbsf, combined.d18O_1209, label="1209", marker="+")
    axs[0].set(ylabel="Uvigerina {} ({})".format(r'$\delta^{18}$O', u"\u2030"))
    axs[0].legend(frameon=False)
    axs[0].invert_yaxis()

    axs[1].scatter(combined.age_ka_mbsf, combined.MgCa_1208, label="1208", marker="o")
    axs[1].scatter(combined.age_ka_mbsf, combined.MgCa_1209, label="1209", marker="o")
    axs[1].set(ylabel="Uvigerina Mg/Ca (mmol/mol)")
    secax = axs[1].secondary_yaxis('left', functions=(bwt_from_mgca, mgca_from_bwt))
    secax.set(ylabel=r'BWT ($\degree$C)')

    tick_dirs(axs, num_plots=2, min_age=0, max_age=80, legend=False)

    if save_fig:
        plt.savefig("figures/paper/core_top_comparison.png", dpi=300)
    else:
        plt.show()

if __name__ == "__main__":
    core_top_comparison(save_fig=True)
