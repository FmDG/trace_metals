import pandas as pd
import os
import matplotlib.pyplot as plt


def basic_calibration():
    # Elderfield Uvigerina calibration
    # Mg/Ca == 0.9 + (0.1 * Temp)
    # Temp = (Mg/Ca - 0.9) * 10

    # Marchitto et al., 2014 - Cibicidoides Temp equation
    # T == 15.75 - (4.46 * (d18O - d18Osw + 0.27));
    # d18O_sw =

    # Load the datasets (1209)
    iso_1209 = pd.read_csv("data/cores/1209_cibs.csv")
    te_1209 = pd.read_csv("data/cores/1209_te.csv")

    # (1208)
    iso_1208 = pd.read_csv("data/cores/1208_cibs.csv")
    te_1208 = pd.read_csv("data/cores/1208_te.csv")

    # Define the temperature (simple)
    te_1208["BWT"] = (te_1208.MgCa - 0.9) * 10
    te_1209["BWT"] = (te_1209["MgCa"] - 0.9) * 10

    # Load the colours
    colour_1208 = '#1b9e77'
    colour_1209 = '#d95f02'
    colour_1313 = '#7570b3'
    colour_607 = '#e7298a'
    colour_849 = '#66a61e'

    # Define num rows
    num_rows = 3

    # Define age limit
    min_age = 2400
    max_age = 2900

    # Set up the figure
    fig, axs = plt.subplots(nrows=num_rows, ncols=1, sharex='all')
    fig.subplots_adjust(hspace=0)

    # Plot the isotopes
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, marker='+', color=colour_1209, label='1209')
    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, marker='+', color=colour_1208, label='1208')
    axs[0].invert_yaxis()

    # Plot the MgCa
    axs[1].plot(te_1209.age_ka, te_1209.MgCa, marker='+', color=colour_1209, label='1209')
    axs[1].plot(te_1208.age_ka, te_1208.MgCa, marker='+', color=colour_1208, label='1208')

    # Plot the BWT
    axs[2].plot(te_1209.age_ka, te_1209.BWT, marker='+', color=colour_1209, label='1209')
    axs[2].plot(te_1208.age_ka, te_1208.BWT, marker='+', color=colour_1208, label='1208')

    # Add legends
    for ax in axs:
        ax.legend(frameon=False, shadow=False)

    # Label the y-axes for the various plots
    axs[0].set(ylabel='Cibicidoides {} ({})'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[1].set(ylabel="Mg/Ca ({})".format('mol/mol'))
    axs[2].set(ylabel="BWT ({})".format(u'\N{DEGREE SIGN}C'))

    # Remove the various axes to clean up the plot
    for q in range(num_rows):
        # Remove the left/right axes to make the plot look cleaner
        if q % 2 == 1:
            axs[q].yaxis.set(ticks_position="right", label_position='right')
            axs[q].spines['left'].set_visible(False)
        else:
            axs[q].spines['right'].set_visible(False)
        axs[q].spines['top'].set_visible(False)
        axs[q].spines['bottom'].set_visible(False)

    # Set the bottom axis on and label it with the age.
    axs[(num_rows - 1)].spines['bottom'].set_visible(True)
    axs[(num_rows - 1)].set(xlabel='Age (ka)', xlim=[min_age, max_age])

    plt.show()


if __name__ == "__main__":
    os.chdir("../..")
    basic_calibration()
