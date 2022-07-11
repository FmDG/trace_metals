import os

import matplotlib.pyplot as plt
import pandas as pd


def compare_607_1209_1208(display: object = True, u1313: object = False, save_name="File") -> bool:
    """

    :rtype: bool
    """
    # Load the colour palette
    colours = ['#1b9e77', '#d95f02', '#7570b3', '#e7298a']

    # Set the age limits
    age_min, age_max = 2400, 2900

    # Load the temperature datasets
    temp_1209 = pd.read_csv("data/PSU_Solver/PSU_data_1209.csv")
    temp_1208 = pd.read_csv("data/PSU_Solver/PSU_data_1208.csv")
    te_1209 = pd.read_csv("data/comparisons/1209_te.csv")
    te_1208 = pd.read_csv("data/comparisons/1208_te.csv")
    temp_607 = pd.read_csv("data/comparisons/607_te.csv")

    # Set up the figure
    num_plots = 3

    if display:
        fig, axs = plt.subplots(num_plots, 1, sharex=True)
    else:
        fig, axs = plt.subplots(num_plots, 1, sharex=True, figsize=(8.25, 11.75))
    # Name the Plots
    fig.suptitle("Comparison of Sites 1208/1209/607\n ({} - {} ka)".format(age_min, age_max))

    # Plot the temperature of the three sites
    axs[0].plot(temp_1209.age_ka, temp_1209.temp, marker='+', color=colours[0], label="1209")
    axs[0].plot(temp_1208.age_ka, temp_1208.temp, marker='+', color=colours[1], label="1208")
    axs[0].plot(temp_607.age_ka, temp_607.BWT, marker='+', color=colours[2], label="607")

    # Plot the d18O of the seawater of the three sites
    axs[1].plot(temp_1209.age_ka, temp_1209.d18O_sw, marker='+', color=colours[0], label="1209")
    axs[1].plot(temp_1208.age_ka, temp_1208.d18O_sw, marker='+', color=colours[1], label="1208")
    axs[1].plot(temp_607.age_ka, temp_607.d18O_sw, marker='+', color=colours[2], label="607")

    # Plot the raw Mg/ca ratios of the three sites
    axs[2].plot(te_1209.age_ka, te_1209.MgCa, marker='+', color=colours[0], label="1209")
    axs[2].plot(te_1208.age_ka, te_1208.MgCa, marker='+', color=colours[1], label="1208")
    axs[2].plot(temp_607.age_ka, temp_607.MgCa, marker='+', color=colours[2], label="607")

    # plot U1313 if required
    if u1313:
        temp_u1313 = pd.read_csv("data/comparisons/U1313_te.csv")
        axs[0].plot(temp_u1313.age_ka, temp_u1313.BWT, marker='+', color=colours[3], label="U1313")
        axs[1].plot(temp_u1313.age_ka, temp_u1313.d18O_sw, marker='+', color=colours[3], label="U1313")
        axs[2].plot(temp_u1313.age_ka, temp_u1313.MgCa, marker='+', color=colours[3], label="U1313")

    # Label the y-axes for the various plots
    axs[0].set(ylabel="BWT ({})".format(u'\N{DEGREE SIGN}C'))
    axs[1].set(ylabel='Modelled {} ({})'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))
    axs[2].set(ylabel="Mg/Ca ({})".format('mol/mol'))

    # Remove the various axes to clean up the plot
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
    axs[(num_plots - 1)].set(xlabel='Age (ka)', xlim=[age_min, age_max])

    # Add a legend to the first plot
    axs[0].legend(loc='upper right', shadow=False, frameon=False)

    if display:
        plt.show()
    else:
        # Save the figure the figures folder
        plt.savefig("figures/607_comparison/{}_{}-{}.pdf".format(save_name, age_min, age_max), format="pdf")

    # if all goes well - return True
    return True


# Run the plotting function
if __name__ == "__main__":
    # Change to the correct directory
    os.chdir("../..")
    compare_607_1209_1208()
