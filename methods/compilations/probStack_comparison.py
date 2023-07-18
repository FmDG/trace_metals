import os

import pandas as pd
import matplotlib.pyplot as plt

from objects.core_data.isotopes import iso_1208, iso_1209
from objects.args_egypt import args_1209, args_1208, colour


def probStack_comparison():
    prob_stack = pd.read_csv("data/comparisons/probStack.csv")
    new_age = pd.read_csv("data/comparisons/1209_d18O_cibs_newAges.csv").dropna(subset="age_ka")

    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=(13, 7)
    )
    # Remove horizontal space between axes
    # fig.subplots_adjust(hspace=0)

    # Plot up the oxygen isotope record
    ax.plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)
    ax.plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)

    ax.plot(prob_stack.Age, (prob_stack.d18O - 0.64), marker="+", c=colour[2], label="ProbStack")
    # ax.plot(new_age.age_ka, new_age.d18O_unadj, **args_1208)

    ax.set(title="New Age Model for Site 1209")

    ax.legend(frameon=False)
    ax.set(xlabel="Age (ka)", ylabel="{} (VPDB {})".format(r'$\delta^{18}$O', u"\u2030"), xlim=(2350, 3600))

    # Invert the axes with d18O
    ax.invert_yaxis()

    plt.show()


if __name__ == "__main__":
    probStack_comparison()