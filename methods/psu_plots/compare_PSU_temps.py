import os

import matplotlib.pyplot as plt
import pandas as pd


def compare_psu_temp(save_fig=False, figure_name="PLOT"):
    psu_607 = pd.read_csv("data/PSU_Solver/RUN_1/run_607.csv")
    other_607 = pd.read_csv("data/comparisons/607_te.csv")
    num_plots = 2
    min_age = 2400
    max_age = 2900

    colours = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3']

    # Set up figure
    if save_fig:
        fig, axs = plt.subplots(num_plots, 1, sharex=True, figsize=(8.25, 11.75))
    else:
        fig, axs = plt.subplots(num_plots, 1, sharex=True)
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    # Name the Plot
    fig.suptitle("Comparison of Site 607 Temperature Calibrations\n ({} - {} ka)".format(min_age, max_age))

    # Plot the modelled temperature from the PSU_Solver
    axs[0].plot(psu_607.age_ka, psu_607.temp, color=colours[0], linestyle='-', label="PSU Calibration")
    # Fill in the confidence intervals (1 sigma)
    axs[0].fill_between(psu_607.age_ka, psu_607.temp_min1, psu_607.temp_plus1, alpha=0.1, facecolor=colours[0])
    axs[0].plot(other_607.age_ka, other_607.BWT, color=colours[1], linestyle='-', label="Orig. Calibration")
    # Label the y-axis
    axs[0].set(ylabel='Inferred {} ({})'.format('Temperatures', u'\N{DEGREE SIGN}C'))
    axs[0].legend()

    # Plot the modelled temperature from the PSU_Solver
    axs[1].plot(psu_607.age_ka, psu_607.d18O_sw, color=colours[0], linestyle='-', label="PSU Calibration")
    axs[1].fill_between(psu_607.age_ka, psu_607.d18O_min1, psu_607.d18O_plus1, alpha=0.1, facecolor=colours[0])

    axs[1].plot(other_607.age_ka, other_607.d18O_sw, color=colours[1], linestyle='-', label="Orig. Calibration")
    # Label the y-axis
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

    # Save the figure if required
    if save_fig:
        plt.savefig("figures/TE_and_PSU_data/{}_{}-{}.pdf".format(figure_name, min_age, max_age), format="pdf")
    else:
        plt.show()


if __name__ == "__main__":
    # Change to the relevant directory
    os.chdir("../..")
    compare_psu_temp()
