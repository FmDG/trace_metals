# This file is designed to generate one large file describing the Mg/Ca ratio, the BWT estimate, and the d18O_sw
# estimate for the cores 1208, 1209, U1313, and 849 for the poster for the EGU conference. There is a secondary aim
# which is to generate a plot for the meeting with Heather and David on the week of the 6th August which summaries
# where I am so far with my results.

import pandas as pd
import os
import matplotlib.pyplot as plt
from cleaning_functions import clean_and_sort


def poster_plot(save_fig=False):
    """
    This is the file that generates the plot for the poster mentioned above.
    :return:
    """
    # Load the Trace Metal datasets
    te_1209 = clean_and_sort(pd.read_csv("data/cores/1209_te.csv"), "MgCa")
    te_1208 = clean_and_sort(pd.read_csv("data/cores/1208_te.csv"), "MgCa")
    te_1313 = clean_and_sort(pd.read_csv("data/cores/U1313_te.csv"), "MgCa")
    te_849 = clean_and_sort(pd.read_csv("data/cores/849_te.csv"), "MgCa")

    # Load the PSU datasets
    psu_1208 = clean_and_sort(pd.read_csv("data/cores/1208_psu.csv"), "temp")
    psu_1209 = clean_and_sort(pd.read_csv("data/cores/1209_psu.csv"), 'temp')
    psu_1313 = clean_and_sort(pd.read_csv("data/cores/U1313_psu.csv"), 'temp')

    # Load the colours
    colour_1208 = '#66c2a5'
    colour_1209 = '#fc8d62'
    colour_1313 = '#8da0cb'
    colour_849 = '#e78ac3'

    # 3 plots; Mg/Ca, d18O_sw, and BWT
    num_plots = 3
    pos_mg_ca, pos_d18o, pos_bwt = 2, 1, 0
    age_min, age_max = 2400, 2900

    fig, axs = plt.subplots(nrows=num_plots, ncols=1, figsize=(19.6, 16.7), sharex=True)
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    # Dictionaries of axis markings
    dict_1209 = {"marker": "o", 'mfc': [0, 0, 0, 0], "color": colour_1209, "mec": colour_1209, "label": '1209'}
    dict_1208 = {"marker": "^", 'mfc': [0, 0, 0, 0], "color": colour_1208, "mec": colour_1208, "label": '1208'}
    dict_1313 = {"marker": "s", 'mfc': [0, 0, 0, 0], "color": colour_1313, "mec": colour_1313, "label": 'U1313'}
    dict_849 = {"marker": "D", 'mfc': [0, 0, 0, 0], "color": colour_849, "mec": colour_849, "label": '849'}

    # The Mg/Ca plot
    axs[pos_mg_ca].plot(te_1209.age_ka, te_1209.MgCa, **dict_1209)
    axs[pos_mg_ca].plot(te_1208.age_ka, te_1208.MgCa, **dict_1208)
    # axs[pos_mg_ca].plot(te_1313.age_ka, te_1313.MgCa, **dict_1313)
    # axs[pos_mg_ca].plot(te_849.age_ka, te_849.MgCa, **dict_849)
    axs[pos_mg_ca].legend()

    # The BWT plot
    axs[pos_bwt].plot(psu_1209.age_ka, psu_1209.temp, **dict_1209)
    axs[pos_bwt].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, alpha=0.1,
                              facecolor=colour_1209)
    axs[pos_bwt].plot(psu_1208.age_ka, psu_1208.temp, **dict_1208)
    axs[pos_bwt].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, alpha=0.1,
                              facecolor=colour_1208)
    axs[pos_bwt].plot(te_1313.age_ka, te_1313.BWT, **dict_1313)
    axs[pos_bwt].plot(te_849.age_ka, te_849.BWT, **dict_849)
    axs[pos_bwt].legend()

    # The d18O_sw plot
    axs[pos_d18o].plot(psu_1209.age_ka, psu_1209.d18O_sw, **dict_1209)
    axs[pos_d18o].fill_between(psu_1209.age_ka, psu_1209.d18O_min1, psu_1209.d18O_plus1, alpha=0.1,
                               facecolor=colour_1209)
    axs[pos_d18o].plot(psu_1208.age_ka, psu_1208.d18O_sw, **dict_1208)
    axs[pos_d18o].fill_between(psu_1208.age_ka, psu_1208.d18O_min1, psu_1208.d18O_plus1, alpha=0.1,
                               facecolor=colour_1208)
    axs[pos_d18o].plot(te_1313.age_ka, te_1313.d18O_sw, **dict_1313)
    axs[pos_d18o].legend()
    axs[pos_d18o].invert_yaxis()

    # Label the y-axes for the various plots
    axs[pos_bwt].set(ylabel="BWT ({})".format(u'\N{DEGREE SIGN}C'))
    axs[pos_d18o].set(ylabel='Modelled {} ({})'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))
    axs[pos_mg_ca].set(ylabel="Mg/Ca ({})".format('mol/mol'))

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

    if save_fig:
        plt.savefig("figures/poster/trace_metals_fill.svg", format='svg')
    else:
        plt.show()


def meeting_plot(save_fig=True):
    # Load the isotope datasets
    iso_1209 = clean_and_sort(pd.read_csv("data/cores/1209_cibs.csv"), "d18O")
    iso_1208 = clean_and_sort(pd.read_csv("data/cores/1208_cibs.csv"), "d18O")
    iso_1313 = clean_and_sort(pd.read_csv("data/cores/U1313_cibs_adj.csv"), "d18O")
    iso_849 = clean_and_sort(pd.read_csv("data/cores/849_cibs_adj.csv"), "d18O")
    iso_607 = clean_and_sort(pd.read_csv("data/cores/607_cibs_adj.csv"), "d18O")

    # Load the Trace Metal datasets
    te_1209 = clean_and_sort(pd.read_csv("data/cores/1209_te.csv"), "MgCa")
    te_1208 = clean_and_sort(pd.read_csv("data/cores/1208_te.csv"), "MgCa")
    te_1313 = clean_and_sort(pd.read_csv("data/cores/U1313_te.csv"), "MgCa")
    te_849 = clean_and_sort(pd.read_csv("data/cores/849_te.csv"), "MgCa")
    te_607 = clean_and_sort(pd.read_csv("data/cores/607_te.csv"), "MgCa")

    # Load the PSU datasets
    psu_1208 = clean_and_sort(pd.read_csv("data/cores/1208_psu.csv"), "temp")
    psu_1209 = clean_and_sort(pd.read_csv("data/cores/1209_psu.csv"), 'temp')
    psu_1313 = clean_and_sort(pd.read_csv("data/cores/U1313_psu.csv"), 'temp')

    # Load the colours
    colour_1208 = '#66c2a5'
    colour_1209 = '#fc8d62'
    colour_1313 = '#8da0cb'
    colour_849 = '#e78ac3'


if __name__ == "__main__":
    # Change to parent directory
    os.chdir("../..")
    # Plot the relevant graphs
    meeting_plot(save_fig=False)
