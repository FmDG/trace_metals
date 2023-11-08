import os

import matplotlib.pyplot as plt
import pandas as pd


def core_top_comparison():
    os.chdir("../../data/comparisons")
    combined = pd.read_csv("core_top_combined.csv")
    combined = combined.sort_values(by="age_ka_mbsf")

    fig, axs = plt.subplots(nrows=2, sharex="all", figsize=(12, 7))
    fig.suptitle("Comparison of 1208 and 1209 with Bordiga et al., (2023) age model")
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    axs[0].scatter(combined.age_ka_mbsf, combined.d18O_1208, label="1208", marker="+")
    axs[0].scatter(combined.age_ka_mbsf, combined.d18O_1209, label="1209", marker="+")
    axs[0].set(ylabel="Uvigerina {} ({})".format(r'$\delta^{18}$O', u"\u2030"))
    axs[0].legend(frameon=False)
    axs[0].invert_yaxis()

    axs[1].scatter(combined.age_ka_mbsf, combined.MgCa_1208, label="1208", marker="+")
    axs[1].scatter(combined.age_ka_mbsf, combined.MgCa_1209, label="1209", marker="+")
    axs[1].set(ylabel="Uvigerina Mg/Ca (mmol/mol)", xlabel="Age (ka)")

    plt.savefig("core_top_comparison.png", dpi=300)


if __name__ == "__main__":
    core_top_comparison()
