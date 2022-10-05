import os

import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import savgol_filter

from methods.interpolations.generate_interpolations import generate_interpolation


def interpolations_glacials(age_min=2400, age_max=3400, window=40, save_fig=False):
    # Load the datasets
    site_1208 = pd.read_csv('data/cores/1208_cibs.csv')
    site_1209 = pd.read_csv('data/cores/1209_cibs.csv')

    # We use a simple 1D interpolation, with a density of "freq"
    freq = 0.1
    interp_1208, age_array = generate_interpolation(site_1208, fs=freq, start=age_min, end=age_max, pchip=False)
    interp_1209, _ = generate_interpolation(site_1209, fs=freq, start=age_min, end=age_max, pchip=False)

    threshold = 3.0
    glacials = (interp_1208 > threshold)

    # Filter interpolation function over "window" ka, with a polynomial function of order "n"
    n = 3
    filtered_diff = savgol_filter((interp_1208 - interp_1209), int(window / freq + 1), n)

    # Generate a plot to display this
    num_plots = 3
    fig, axs = plt.subplots(num_plots, sharex="all", figsize=(15, 10))
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    # Plot the oxygen isotope records from 1208 and 1209
    axs[0].plot(age_array, interp_1208, label="1208", c='k')
    axs[0].fill_between(age_array, interp_1208, threshold, fc='b', ec=None, alpha=0.2)
    axs[0].set(ylabel='Benthic {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[0].plot([age_min, age_max], [threshold, threshold], '--', color='k', linewidth=1.0,
                label='Threshold = {} {}'.format(threshold, u"\u2030"))

    # Plot the oxygen isotope records from 1208 and 1209
    axs[1].plot(site_1208.age_ka, site_1208.d18O_unadj, label="ODP 1208", marker='+')
    axs[1].plot(site_1209.age_ka, site_1209.d18O_unadj, label="ODP 1209", marker='+')
    axs[1].set(ylabel='Benthic {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))

    # Plot the difference between the isotope records
    axs[2].plot(age_array, (interp_1208 - interp_1209), label="Difference", c='m')
    axs[2].plot(age_array, filtered_diff, label="Rolling mean ({} ka)".format(window), c='k')
    axs[2].set(xlabel="Age (ka)", ylabel="Difference in {} ({})".format(r'$\delta^{18}$O', u"\u2030"),
               xlim=[age_min, age_max], ylim=[-0.8, 0.2])

    # Fills in the gap between the line and the 0 axis
    # axs[1].fill_between(age_array, (interp_1208 - interp_1209), 0, color='m', alpha=0.2)
    # axs[1].fill_between(age_array, filtered_diff, 0, color='k', alpha=0.2)

    # Label the position of the glacials
    axs[2].fill_between(age_array, ((glacials * -10) + 0.25), 0.25, fc='b', ec=None, alpha=0.1, label="Glacial periods")

    # Remove the various axes to clean up the plot
    for q in range(num_plots):

        axs[q].invert_yaxis()
        axs[q].legend(frameon=False, shadow=False)
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

    # Show the plot
    if save_fig:
        plt.savefig("figures/interpolations/figure_01.png", format='png', dpi=300)
    else:
        plt.show()


def interpolations_productivity(age_min=2400, age_max=3400, window=40, save_fig=False):
    # Load the datasets
    site_1208 = pd.read_csv('data/cores/1208_cibs.csv')
    site_1209 = pd.read_csv('data/cores/1209_cibs.csv')

    # Load the productivity dataset
    site_882 = pd.read_csv('data/cores/882_opal.csv')

    # We use a simple 1D interpolation, with a density of "freq"
    freq = 0.1
    interp_1208, age_array = generate_interpolation(site_1208, fs=freq, start=age_min, end=age_max, pchip=False)
    interp_1209, _ = generate_interpolation(site_1209, fs=freq, start=age_min, end=age_max, pchip=False)

    # Filter interpolation function over "window" ka, with a polynomial function of order "n"
    n = 3
    filtered_diff = savgol_filter((interp_1208 - interp_1209), int(window / freq + 1), n)

    # Generate a plot to display this
    num_plots = 3
    fig, axs = plt.subplots(num_plots, sharex="all", figsize=(15, 10))
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    # Plot the productivity records
    axs[0].plot(site_882.age_ka, site_882.opal_acc_rate, label="ODP 882", marker="+", c='g')
    axs[0].set(ylabel='Opal acc. rate ({})'.format(r'g cm$^{-2}$ kyr$^{-1}$'))

    # Plot the oxygen isotope records from 1208 and 1209
    axs[1].plot(site_1208.age_ka, site_1208.d18O_unadj, label="ODP 1208", marker='+')
    axs[1].plot(site_1209.age_ka, site_1209.d18O_unadj, label="ODP 1209", marker='+')
    axs[1].set(ylabel='Benthic {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[1].invert_yaxis()

    # Plot the difference between the isotope records
    axs[2].plot(age_array, (interp_1208 - interp_1209), label="Difference", c='m')
    axs[2].plot(age_array, filtered_diff, label="Rolling mean ({} ka)".format(window), c='k')
    axs[2].set(xlabel="Age (ka)", ylabel="Difference in {} ({})".format(r'$\delta^{18}$O', u"\u2030"),
               xlim=[age_min, age_max], ylim=[-0.8, 0.2])
    axs[2].invert_yaxis()

    # Remove the various axes to clean up the plot
    for q in range(num_plots):

        axs[q].legend(frameon=False, shadow=False)
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

    # Show the plot
    if save_fig:
        plt.savefig("figures/interpolations/figure_03.png", format='png')
    else:
        plt.show()


def interpolations_te(age_min=2400, age_max=3400, window=40, save_fig=False):
    # Load the datasets
    site_1208 = pd.read_csv('data/cores/1208_cibs.csv')
    site_1209 = pd.read_csv('data/cores/1209_cibs.csv')

    # Load the te dataset
    te_1208 = pd.read_csv('data/cores/1208_te.csv')
    te_1209 = pd.read_csv('data/cores/1209_te.csv')

    # We use a simple 1D interpolation, with a density of "freq"
    freq = 0.1
    interp_1208, age_array = generate_interpolation(site_1208, fs=freq, start=age_min, end=age_max, pchip=False)
    interp_1209, _ = generate_interpolation(site_1209, fs=freq, start=age_min, end=age_max, pchip=False)

    # Filter interpolation function over "window" ka, with a polynomial function of order "n"
    n = 3
    filtered_diff = savgol_filter((interp_1208 - interp_1209), int(window / freq + 1), n)

    # Generate a plot to display this
    num_plots = 3
    fig, axs = plt.subplots(num_plots, sharex="all", figsize=(15, 10))
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    # Plot the oxygen isotope records from 1208 and 1209
    axs[0].plot(site_1208.age_ka, site_1208.d18O_unadj, label="ODP 1208", marker='+')
    axs[0].plot(site_1209.age_ka, site_1209.d18O_unadj, label="ODP 1209", marker='+')
    axs[0].set(ylabel='Benthic {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[0].invert_yaxis()

    # Plot the difference between the isotope records
    axs[1].plot(age_array, (interp_1208 - interp_1209), label="Difference", c='m')
    axs[1].plot(age_array, filtered_diff, label="Rolling mean ({} ka)".format(window), c='k')
    axs[1].set(xlabel="Age (ka)", ylabel="Difference in {} ({})".format(r'$\delta^{18}$O', u"\u2030"),
               ylim=[-0.8, 0.2])
    axs[1].invert_yaxis()

    axs[2].plot(te_1208.age_ka, te_1208.MgCa, label="ODP 1208", marker="+")
    axs[2].plot(te_1209.age_ka, te_1209.MgCa, label="ODP 1209", marker="+")
    axs[2].set(ylabel='Mg/Ca ({})'.format('mmol/mol'))

    # Remove the various axes to clean up the plot
    for q in range(num_plots):

        axs[q].legend(frameon=False, shadow=False)
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

    # Show the plot
    if save_fig:
        plt.savefig("figures/interpolations/figure_05.png", format='png')
    else:
        plt.show()


if __name__ == "__main__":
    os.chdir('../..')
    interpolations_glacials(save_fig=True)
