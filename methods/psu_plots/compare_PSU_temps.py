import os

import matplotlib.pyplot as plt
import pandas as pd


def compare_psu_temp(save_fig=False, figure_name="PLOT"):

    # Load the PSU data
    psu_1209 = pd.read_csv("data/PSU_Solver/RUN_6/1209_run.csv")
    psu_1208 = pd.read_csv("data/PSU_Solver/RUN_6/1208_run.csv")
    psu_1313 = pd.read_csv("data/PSU_Solver/RUN_6/U1313_run_02.csv")

    # Load the TE data
    te_1208 = pd.read_csv("data/cores/1208_te.csv")
    te_1209 = pd.read_csv("data/cores/1209_te.csv")
    temp_849 = pd.read_csv("data/cores/849_te.csv")
    temp_1313 = pd.read_csv("data/cores/U1313_te.csv")
    temp_607 = pd.read_csv("data/cores/607_te.csv")

    # Load the d18O data
    iso_1208 = pd.read_csv("data/cores/1208_cibs.csv")
    iso_1209 = pd.read_csv("data/cores/1209_cibs.csv")
    iso_1313 = pd.read_csv("data/cores/U1313_cibs_adj.csv")
    iso_849 = pd.read_csv("data/cores/849_cibs_adj.csv")
    iso_607 = pd.read_csv("data/cores/607_cibs_adj.csv")

    # Clean the data
    psu_1208 = psu_1208.dropna()
    psu_1209 = psu_1209.dropna()
    psu_1313 = psu_1313.dropna()
    temp_1313 = temp_1313.dropna()

    num_plots = 4
    min_age = 2450
    max_age = 2850

    colours = ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e']

    # Set up figure
    if save_fig:
        fig, axs = plt.subplots(num_plots, 1, sharex=True, figsize=(8.25, 11.75))
    else:
        fig, axs = plt.subplots(num_plots, 1, sharex=True)
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    # Name the Plot
    fig.suptitle("Comparison of Core Sites (using PSU Solver Calibrations)\n ({} - {} ka)".format(min_age, max_age))

    # Plot the modelled temperature from the PSU_Solver
    # axs[0].plot(psu_1209.age_ka, psu_1209.temp, color=colours[0], linestyle='-', label="1209", marker='+')
    # Fill in the confidence intervals (1 sigma)
    # axs[0].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, alpha=0.1, facecolor=colours[0])
    # Plot the modelled temperature from the PSU_Solver for 1208
    # axs[0].plot(psu_1208.age_ka, psu_1208.temp, color=colours[1], linestyle='-', label="1208", marker='+')
    # axs[0].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, alpha=0.1, facecolor=colours[1])
    # axs[0].plot(psu_1313.age_ka, psu_1313.temp, color=colours[2], linestyle='-', label="U1313", marker='+')
    # axs[0].fill_between(psu_1313.age_ka, psu_1313.temp_min1, psu_1313.temp_plus1, alpha=0.1, facecolor=colours[2])
    axs[0].plot(temp_1313.age_ka, temp_1313.BWT, color=colours[2], linestyle='-', label="U1313", marker='+')
    axs[0].plot(temp_607.age_ka, temp_607.BWT, color=colours[3], linestyle='-', label="607", marker='+')
    # axs[0].plot(temp_849.age_ka, temp_849.BWT, color=colours[4], linestyle='-', label="849", marker='+')

    # Label the y-axis
    axs[0].set(ylabel='Modelled {} ({})'.format('Temperatures', u'\N{DEGREE SIGN}C'))
    axs[0].legend()

    # Plot the modelled d18O_sw from the PSU_Solver
    # axs[1].plot(psu_1209.age_ka, psu_1209.d18O_sw, color=colours[0], linestyle='-', label="1209", marker='+')
    # Fill in the confidence intervals (1 sigma)
    # axs[1].fill_between(psu_1209.age_ka, psu_1209.d18O_min1, psu_1209.d18O_plus1, alpha=0.1, facecolor=colours[0])
    # Plot the modelled temperature from the PSU_Solver for 1208
    # axs[1].plot(psu_1208.age_ka, psu_1208.d18O_sw, color=colours[1], linestyle='-', label="1208", marker='+')
    # axs[1].fill_between(psu_1208.age_ka, psu_1208.d18O_min1, psu_1208.d18O_plus1, alpha=0.1, facecolor=colours[1])
    # axs[1].plot(psu_1313.age_ka, psu_1313.d18O_sw, color=colours[2], linestyle='-', label="U1313", marker='+')
    # axs[1].fill_between(psu_1313.age_ka, psu_1313.d18O_min1, psu_1313.d18O_plus1, alpha=0.1, facecolor=colours[2])
    axs[1].plot(temp_1313.age_ka, temp_1313.d18O_sw, color=colours[2], linestyle='-', label="U1313", marker='+')
    axs[1].plot(temp_607.age_ka, temp_607.d18O_sw, color=colours[3], linestyle='-', label="607", marker='+')
    # Label the y-axis
    axs[1].set(ylabel='Modelled {} ({})'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))
    axs[1].invert_yaxis()
    axs[1].legend()

    # Plot the Cibicidoides d18O from the PSU_Solver
    # axs[2].plot(iso_1209.age_ka, iso_1209.d18O_unadj, color=colours[0], linestyle='-', label="1209", marker='+')
    # axs[2].plot(iso_1208.age_ka, iso_1208.d18O_unadj, color=colours[1], linestyle='-', label="1208", marker='+')
    axs[2].plot(iso_1313.age_ka, (iso_1313.d18O - 0.64), color=colours[2], linestyle='-', label="U1313", marker='+')
    axs[2].plot(iso_607.age_ka, (iso_607.d18O - 0.64), color=colours[3], linestyle='-', label="607", marker='+')
    # axs[2].plot(iso_849.age_ka, (iso_849.d18O - 0.64), color=colours[4], linestyle='-', label="849", marker='+')
    axs[2].set(ylabel='Cibicidoides {} ({})'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[2].invert_yaxis()
    axs[2].legend()

    # Plot the Mg/Ca ratio
    # axs[3].plot(te_1208.age_ka, te_1208.MgCa, color=colours[1], marker='+', linestyle='-', label="1208")
    # axs[3].plot(te_1209.age_ka, te_1209.MgCa, color=colours[0], marker='+', linestyle='-', label="1209")
    axs[3].plot(temp_1313.age_ka, temp_1313.MgCa, color=colours[2], marker='+', linestyle='-', label='U1313')
    axs[3].plot(temp_607.age_ka, temp_607.MgCa, color=colours[3], marker='+', linestyle='-', label='607')
    axs[3].set(ylabel='{} ({})'.format('Mg/Ca', "mmol/mol"))

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
        plt.savefig("figures/BWT_calibrations/{}.pdf".format(figure_name), format="pdf")
    else:
        plt.show()


if __name__ == "__main__":
    # Change to the relevant directory
    os.chdir("../..")
    compare_psu_temp(save_fig=False, figure_name="607_U1313")
