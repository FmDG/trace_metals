import os

import pandas as pd
import matplotlib.pyplot as plt


def plot_datasets():
    samples = pd.read_csv("data/samples.csv")
    iso_1209 = pd.read_csv("data/cores/1209_cibs.csv")
    iso_1208 = pd.read_csv("data/cores/1208_cibs.csv")

    samples_present = samples[samples.requested == 1]
    samples_absent = samples[samples.requested == 0]

    fig, axs = plt.subplots(nrows=2, figsize=(13, 7), sharex="all")
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    axs[0].scatter(samples_present.age_ka, samples_present.requested, c="r", marker="o", label="Requested")
    axs[0].scatter(samples_absent.age_ka, samples_absent.requested + 1, c="b", marker="+", label="Already sampled")

    axs[0].legend(frameon=False)

    axs[1].plot(iso_1208.age_ka, iso_1208.d18O_unadj, marker="+", label="1208")
    axs[1].plot(iso_1209.age_ka, iso_1209.d18O_unadj, marker="+", label="1209")

    axs[1].legend(frameon=False)
    axs[1].set(xlabel="Age (ka)", ylabel="{} (VPDB {})".format(r'$\delta^{18}$O', u"\u2030"), xlim=(2250, 3750))
    axs[1].invert_yaxis()

    plt.show()


if __name__ == "__main__":
    os.chdir("../..")

    plot_datasets()
