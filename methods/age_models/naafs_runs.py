import os

import pandas as pd
import matplotlib.pyplot as plt

from objects.core_data.isotopes import iso_1208, iso_1209
from objects.core_data.psu import psu_1208, psu_1209
import objects.args_brewer as args

from methods.figures.tick_dirs import tick_dirs
from methods.age_models.age_model import def_age_model


def naafs_runs():

    if not os.path.isdir("data/cores"):
        os.chdir('../..')

    naf_1208 = pd.read_csv("data/comparisons/1208_Naafs.csv")
    age_model_1208 = def_age_model(site="1208")
    naf_1208["age_ka"] = age_model_1208(naf_1208["Top depth CSF-B (m)"])

    naf_1209 = pd.read_csv("data/comparisons/1209_Naafs.csv")
    age_model_1209 = def_age_model(site="1209")
    naf_1209["age_ka"] = age_model_1209(naf_1209["Top depth CSF-B (m)"])

    x_min = 1500
    x_max = 3400
    n_rows = 2

    fig, axs = plt.subplots(
        nrows=n_rows,
        ncols=1,
        sharex="all",
        figsize=(12, 8)
    )

    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)
    # Name the Plot
    fig.suptitle("Samples Requested compared to 1208 {}\n{} - {} ka".format(r'$\delta^{18}$O', x_min, x_max))

    axs[0].scatter(naf_1208.age_ka, naf_1208['Site'].astype(str), label='1208', marker='+', color='r')
    axs[0].scatter(naf_1209.age_ka, naf_1209['Site'].astype(str), label='1209', marker='+', color='b')

    # -- Plot the 1208 data --
    # d18O original data
    axs[1].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args.args_1208)

    axs[0].set(ylabel="Site")
    axs[1].set(ylabel="1208 {} (VPDB {})".format(r'$\delta^{18}$O', u"\u2030"))

    axs[1].invert_yaxis()
    tick_dirs(axs, n_rows, x_min, x_max)

    plt.show()


if __name__ == "__main__":

    naafs_runs()
