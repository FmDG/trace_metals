import os

import matplotlib.pyplot as plt
import pandas as pd


def lithium_plots():
    # Load the 1209 and 1208 dataset
    te_1209 = pd.read_csv("data/1209_TraceMetals.csv")
    te_1208 = pd.read_csv("data/1208_TraceMetals.csv")

    # Set the ages
    min_age, max_age = 2400, 2900

    # Decide on the colours for 1208 and 1209
    colour_1209, colour_1208 = "#1b9e77", "#d95f02"

    # Set up the plots
    num_plots = 3
    fig, axs = plt.subplots(num_plots, 1, sharex=True)

    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    # Name the Plots
    fig.suptitle("Comparison of Sites 1208/09\n ({} - {} ka)".format(min_age, max_age))

    axs[0].plot(te_1208.age_ka, te_1208.MgCa, marker='+', color=colour_1208, label="ODP 1208")
    axs[0].plot(te_1209.age_ka, te_1209.MgCa, marker='+', color=colour_1209, label="ODP 1209")
    # Label the y-axis
    axs[0].set(ylabel='{} ({})'.format('Mg/Ca', "mmol/mol"))

    axs[1].plot(te_1209.age_ka, te_1209.LiCa, marker='+', color=colour_1209, label="ODP 1209")
    # Label the y-axis
    axs[1].set(ylabel='{} ({})'.format('Li/Ca', "mmol/mol"))

    te_1209["MgLi"] = (te_1209.MgCa / te_1209.LiCa)

    axs[2].plot(te_1209.age_ka, te_1209.MgLi, marker='+', color=colour_1209, label="ODP 1209")
    # Label the y-axis
    axs[2].set(ylabel='{} ({})'.format('Mg/Li', "mmol/mol"))

    for q in range(num_plots):
        # Remove the left/right axes to make the plot look cleaner
        if q % 2 == 1:
            axs[q].yaxis.set(ticks_position="right", label_position='right')
            axs[q].spines['left'].set_visible(False)
        else:
            axs[q].spines['right'].set_visible(False)
        axs[q].spines['top'].set_visible(False)
        axs[q].spines['bottom'].set_visible(False)

    # Set the bottom axis on and label it with the age.
    axs[(num_plots - 1)].spines['bottom'].set_visible(True)
    axs[(num_plots - 1)].set(xlabel='Age (ka)', xlim=[min_age, max_age])

    # Add a legend to the first plot
    axs[0].legend(loc='upper left', shadow=False, frameon=False)

    plt.show()


if __name__ == "__main__":
    os.chdir("../..")
    lithium_plots()
