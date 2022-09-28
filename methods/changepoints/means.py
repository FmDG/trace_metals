import os

import pandas as pd
import matplotlib.pyplot as plt

from methods.interpolations.te_changepoints import age_split
from objects.colours import colours, colours_04


def change_point_means():
    # Edit the 1209 te dataset
    te_1209_data = pd.read_csv("data/cores/1209_te.csv")
    te_1209_data = te_1209_data[te_1209_data.age_ka < 2900]

    # Load the datasets
    te_1209 = {
                  "data": te_1209_data,
                  "changepoint": 2702.9,
                  "value": "MgCa",
                  "axis": "Mg/Ca",
                  "label": '1209 Mg/Ca',
                  "invert": False,
    }
    te_1208 = {
                  "data": pd.read_csv("data/cores/1208_te.csv"),
                  "changepoint": 2687.2,
                  "value": "MgCa",
                  "axis": "Mg/Ca",
                  "label": '1208 Mg/Ca',
                  "invert": False,
    }

    iso_1209 = {
                  "data": pd.read_csv("data/cores/1209_cibs.csv"),
                  "changepoint": 2729.5,
                  "value": "d18O_unadj",
                  "axis": r'$\delta^{18}$O',
                  "label": '1209 {}'.format(r'$\delta^{18}$O'),
                  "invert": True,
    }
    iso_1208 = {
                  "data": pd.read_csv("data/cores/1208_cibs.csv"),
                  "changepoint": 2729.5,
                  "value": "d18O_unadj",
                  "axis": r'$\delta^{18}$O',
                  "label": '1208 {}'.format(r'$\delta^{18}$O'),
                  "invert": True,
    }

    items = [te_1208, te_1209, iso_1208, iso_1209]

    # Plot up the data
    fig, axs = plt.subplots(
        nrows=2,
        ncols=2,
        sharex='all',
        figsize=(12, 8)
    )
    # Remove horizontal space between axes
    fig.subplots_adjust(
        hspace=0,
        wspace=0
    )

    i, j = 0, 0
    c = 0

    for x in items:
        # Return the means and standard deviations
        after_mean, after_error, before_mean, before_error = age_split(x['data'], x['changepoint'], x['value'])

        axs[i, j].plot(
            x['data'].age_ka, x['data'][x['value']],
            marker='+',
            color=colours_04[c],
            label=x['label']
        )
        c += 1

        axs[i, j].plot(
            [x['data'].age_ka.min(), x['changepoint']], [after_mean, after_mean],
            label=f'Post-{x["changepoint"]} kyr = {after_mean:.2} ± {after_error:.1}',
            color=colours[1]
        )
        axs[i, j].fill_between(
            [x['data'].age_ka.min(), x['changepoint']],
            [after_mean - after_error, after_mean - after_error],
            [after_mean + after_error, after_mean + after_error],
            alpha=0.1,
            color=colours[1]
        )
        axs[i, j].plot(
            [x['changepoint'], x['data'].age_ka.max()],
            [before_mean, before_mean],
            label=f'Pre-{x["changepoint"]} kyr = {before_mean:.2} ± {before_error:.1}',
            color=colours[2]
        )
        axs[i, j].fill_between(
            [x['changepoint'], x['data'].age_ka.max()],
            [before_mean - before_error, before_mean - before_error],
            [before_mean + before_error, before_mean + before_error],
            alpha=0.1,
            color=colours[2]
        )

        axs[i, j].set(
            ylabel=x['axis'],
            xlabel='Age (ka)',
            xlim=[2400, 3400]
        )

        if x['invert']:
            axs[i, j].invert_yaxis()

        axs[i, j].axvline(x['changepoint'], color='r', ls='--')
        axs[i, j].legend(
            frameon=False,
            shadow=False
        )

        j += 1
        if j > 1:
            j = 0
            i += 1

    for ax in axs.flat:
        ax.label_outer()

    plt.show()


if __name__ == "__main__":
    os.chdir("../..")
    change_point_means()
