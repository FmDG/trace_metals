import os

import matplotlib.pyplot as plt
import pandas as pd


def simple_calibrations():
    data_607 = pd.read_csv("data/comparisons/607_te.csv")
    data_1209 = pd.read_csv("data/1209_TraceMetals.csv")
    data_1208 = pd.read_csv("data/1208_TraceMetals.csv")
    data_1313 = pd.read_csv("data/comparisons/U1313_te.csv")

    # Equations
    # Woodard: Mg/Ca = 0.067 * T
    # or BWT = 14.925 MgCa
    # Sosdian: Mg/Ca = 0.15 × BWT + 1.16;
    # Jakob: BWT = ((ln(Mg/Ca)/1.008)/0.114)

    num_plots = 2
    min_age = 2400
    max_age = 2900

    # Add some colours
    colours = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3']

    fig, axs = plt.subplots(num_plots, 1, sharex=True)
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)
    # Name the Plot
    fig.suptitle("Comparison of Sites 607/1208/1209/1313\n ({} - {} ka)".format(min_age, max_age))

    # Plot the modelled temperature
    axs[0].plot(data_607.age_ka, data_607.BWT, color=colours[0], linestyle='-', label="607")
    axs[0].plot(data_1313.age_ka, data_1313.BWT, color=colours[1], linestyle='-', label="U1313")
    axs[0].plot(data_1208.age_ka, (data_1208.MgCa * 14.925), color=colours[2], linestyle='-', label="1208")
    axs[0].plot(data_1209.age_ka, (data_1209.MgCa * 14.925), color=colours[3], linestyle='-', label="1208")
    axs[0].set(ylabel='Inferred {} ({})'.format('Temperatures', u'\N{DEGREE SIGN}C'))
    axs[0].legend()

    axs[1].plot(data_607.age_ka, data_607.d18O_sw, color=colours[0], linestyle='-', label="607")
    axs[1].plot(data_1313.age_ka, data_1313.d18O_sw, color=colours[1], linestyle='-', label="U1313")
    axs[1].set(ylabel='Modelled {} ({})'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))

    # For each of the plots
    for q in range(num_plots):
        # Remove the left/right axes to make the plot look cleaner
        if q % 2 == 1:
            axs[q].yaxis.set(ticks_position="right", label_position='right')
            axs[q].spines['left'].set_visible(False)
        else:
            axs[q].spines['right'].set_visible(False)
        # Remove the top and bottom axes to make it look cleaner
        axs[q].spines['top'].set_visible(False)
        axs[q].spines['bottom'].set_visible(False)

    # Set the bottom axis on and label it with the age.
    axs[(num_plots - 1)].spines['bottom'].set_visible(True)
    axs[(num_plots - 1)].set(xlabel='Age (ka)', xlim=[min_age, max_age])

    plt.show()


if __name__ == "__main__":
    os.chdir("../..")
    simple_calibrations()
