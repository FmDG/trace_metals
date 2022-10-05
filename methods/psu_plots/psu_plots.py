import os

import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import savgol_filter

from methods.interpolations.generate_interpolations import generate_interpolation
# import colours from colours file
from objects.colours import colours


# ----------------------------------- IMPLEMENTATION ---------------------------------------------


def psu_plots_full(save_fig=False):

    # ------------------------ LOADING DATA ---------------------------

    # Load the PSU datasets
    psu_1208 = pd.read_csv("data/cores/1208_psu.csv").dropna()
    psu_1209 = pd.read_csv("data/cores/1209_psu.csv").dropna()

    # Load the Trace Element datasets
    te_1208 = pd.read_csv("data/cores/1208_te.csv")
    te_1209 = pd.read_csv("data/cores/1209_te.csv")

    # Load the Oxygen Isotope datasets
    iso_1208 = pd.read_csv("data/cores/1208_cibs.csv")
    iso_1209 = pd.read_csv('data/cores/1209_cibs.csv')

    # Define the colours
    args_1208 = {'color': colours[0], 'label': "1208", 'marker': '+'}
    fill_1208 = {'facecolor': colours[0], 'alpha': 0.1, 'label': r'$\pm 1\sigma$'}
    args_1209 = {'color': colours[1], 'label': "1209", 'marker': '+'}
    fill_1209 = {'facecolor': colours[1], 'alpha': 0.1, 'label': r'$\pm 1\sigma$'}
    args_diff = {'color': colours[2], 'label': "1208 - 1209"}
    args_filt = {'color': 'k', 'label': "Rolling mean (40 ka)"}
    fill_diff = {'facecolor': 'k', 'alpha': 0.1}

    # Plots for d18O_sw, BWT, Mg/Ca, and d18O_b
    num_plots = 4
    min_age, max_age = 2400, 2900

    # --------------------- DEFINE THE DIFFERENCE IN d18O -------------------

    # Interpolate across the d18O arrays
    interp_1208, age_array = generate_interpolation(iso_1208, fs=0.1, start=min_age, end=max_age, pchip=False)
    interp_1209, _ = generate_interpolation(iso_1209, fs=0.1, start=min_age, end=max_age, pchip=False)

    # Calculate the differences
    differences = interp_1208 - interp_1209
    filtered_diff = savgol_filter(differences, 301, 3)

    # --------------------- PLOT THE DATA ------------------------

    fig, axs = plt.subplots(
        nrows=num_plots,
        ncols=1,
        sharex="all",
        figsize=(8, 12)
    )

    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)
    # Name the Plot
    fig.suptitle("Comparison of Sites 1208 and 1209\n ({} - {} ka)".format(min_age, max_age))

    # -- Plot the 1208 data --
    # PSU BWT estimates
    axs[0].plot(psu_1208.age_ka, psu_1208.temp, **args_1208)
    axs[0].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, **fill_1208)
    # PSU d18O_sw estimates
    axs[1].plot(psu_1208.age_ka, psu_1208.d18O_sw, **args_1208)
    axs[1].fill_between(psu_1208.age_ka, psu_1208.d18O_min1, psu_1208.d18O_plus1, **fill_1208)
    # d18O original data
    axs[2].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)
    # Mg/Ca original data
    axs[3].plot(te_1208.age_ka, te_1208.MgCa, **args_1208)

    # -- Plot the 1209 data --
    # PSU BWT estimates
    axs[0].plot(psu_1209.age_ka, psu_1209.temp, **args_1209)
    axs[0].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, **fill_1209)
    # PSU d18O_sw estimates
    axs[1].plot(psu_1209.age_ka, psu_1209.d18O_sw, **args_1209)
    axs[1].fill_between(psu_1209.age_ka, psu_1209.d18O_min1, psu_1209.d18O_plus1, **fill_1209)
    # d18O original data
    axs[2].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)
    # Mg/Ca original data
    axs[3].plot(te_1209.age_ka, te_1209.MgCa, **args_1209)

    # Plot the differences in d18O
    # axs[3].plot(age_array, differences, **args_diff)
    # axs[3].plot(age_array, filtered_diff, **args_filt)
    # axs[3].fill_between(age_array, filtered_diff, **fill_diff)

    # -- Define the axes --
    axs[0].set(ylabel="BWT ({})".format(u'\N{DEGREE SIGN}C'))
    axs[1].set(ylabel='Modelled {} ({} VPDB)'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))
    axs[2].set(ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    # axs[3].set(ylabel="{} (VPDB {})".format(r'$\Delta \delta^{18}$O ', u"\u2030"))
    axs[3].set(ylabel="Mg/Ca (mmol/mol)")

    # Invert the axes with d18O
    axs[1].invert_yaxis()
    axs[2].invert_yaxis()
    # axs[3].invert_yaxis()

    for q in range(num_plots):
        # Remove the left/right axes to make the plot look cleaner
        if q % 2 == 1:
            axs[q].yaxis.set(ticks_position="right", label_position='right')
            axs[q].spines['left'].set_visible(False)
        else:
            axs[q].spines['right'].set_visible(False)
        axs[q].spines['top'].set_visible(False)
        axs[q].spines['bottom'].set_visible(False)
        axs[q].legend(shadow=False, frameon=False)

    # Set the bottom axis on and label it with the age.
    axs[(num_plots - 1)].spines['bottom'].set_visible(True)
    axs[(num_plots - 1)].set(xlabel='Age (ka)', xlim=[min_age, max_age])

    # Save the figure if required
    if save_fig:
        plt.savefig("figures/psu_plots/Figure_01_{}-{}.pdf".format(min_age, max_age), format="pdf")
    else:
        plt.show()


if __name__ == "__main__":
    # Change to the relevant directory
    os.chdir("../..")
    # Run the function
    psu_plots_full(save_fig=False)
