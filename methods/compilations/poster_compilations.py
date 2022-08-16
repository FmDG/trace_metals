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


def meeting_plot(save_fig=False, save_title="Figure"):
    # Load the isotope datasets
    iso_1209 = clean_and_sort(pd.read_csv("data/cores/1209_cibs.csv"), "d18O")
    iso_1208 = clean_and_sort(pd.read_csv("data/cores/1208_cibs.csv"), "d18O")
    iso_1313 = clean_and_sort(pd.read_csv("data/cores/U1313_cibs_adj.csv"), "d18O")
    iso_849 = clean_and_sort(pd.read_csv("data/cores/849_cibs_adj.csv"), "d18O")
    iso_607 = clean_and_sort(pd.read_csv("data/cores/607_cibs_adj.csv"), "d18O")
    iso_981 = clean_and_sort(pd.read_csv("data/cores/981_cibs_adj.csv"), "d18O")
    iso_982 = clean_and_sort(pd.read_csv("data/cores/981_cibs_adj.csv"), "d18O")

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
    colour_1208 = '#1b9e77'
    colour_1209 = '#d95f02'
    colour_1313 = '#7570b3'
    colour_607 = '#e7298a'
    colour_849 = '#66a61e'

    # 4 plots; d18O, Mg/Ca, d18O_sw, and BWT
    num_plots = 4
    pos_d18o, pos_mg_ca, pos_sw, pos_bwt = 0, 1, 3, 2
    age_min, age_max = 2400, 2900

    fig, axs = plt.subplots(nrows=num_plots, ncols=1, figsize=(19.6, 16.7), sharex=True)
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    # Dictionaries of axis markings
    dict_1209 = {"marker": '+', "color": colour_1209, "label": '1209'}
    dict_1208 = {"marker": '+', "color": colour_1208, "label": '1208'}
    dict_1313 = {"marker": None, "color": colour_1313, "label": 'U1313'}
    dict_849 = {"marker": None, "color": colour_849, "label": '849'}
    dict_607 = {"marker": None, "color": colour_607, "label": '607'}

    # 1208 data
    axs[pos_mg_ca].plot(te_1208.age_ka, te_1208.MgCa, **dict_1208)
    axs[pos_bwt].plot(psu_1208.age_ka, psu_1208.temp, **dict_1208)
    axs[pos_d18o].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **dict_1208)
    axs[pos_bwt].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, alpha=0.1,
                              facecolor=colour_1208)
    axs[pos_sw].plot(psu_1208.age_ka, psu_1208.d18O_sw, **dict_1208)
    axs[pos_sw].fill_between(psu_1208.age_ka, psu_1208.d18O_min1, psu_1208.d18O_plus1, alpha=0.1, facecolor=colour_1208)

    # 1209 data
    axs[pos_mg_ca].plot(te_1209.age_ka, te_1209.MgCa, **dict_1209)
    axs[pos_bwt].plot(psu_1209.age_ka, psu_1209.temp, **dict_1209)
    axs[pos_bwt].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, alpha=0.1,
                              facecolor=colour_1209)
    axs[pos_sw].plot(psu_1209.age_ka, psu_1209.d18O_sw, **dict_1209)
    axs[pos_sw].fill_between(psu_1209.age_ka, psu_1209.d18O_min1, psu_1209.d18O_plus1, alpha=0.1, facecolor=colour_1209)
    axs[pos_d18o].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **dict_1209)

    # U1313 data
    '''# axs[pos_mg_ca].plot(te_1313.age_ka, te_1313.MgCa, **dict_1313)
    axs[pos_bwt].plot(psu_1313.age_ka, psu_1313.temp, **dict_1313)
    axs[pos_bwt].fill_between(psu_1313.age_ka, psu_1313.temp_min1, psu_1313.temp_plus1, alpha=0.1,
                              facecolor=colour_1313)
    axs[pos_sw].plot(psu_1313.age_ka, psu_1313.d18O_sw, **dict_1313)
    axs[pos_sw].fill_between(psu_1313.age_ka, psu_1313.d18O_min1, psu_1313.d18O_plus1, alpha=0.1, facecolor=colour_1313)
    axs[pos_d18o].plot(iso_1313.age_ka, (iso_1313.d18O - 0.64), **dict_1313)'''

    '''# 849 data
    axs[pos_mg_ca].plot(te_849.age_ka, te_849.MgCa, **dict_849)
    axs[pos_bwt].plot(te_849.age_ka, te_849.BWT, **dict_849)
    axs[pos_d18o].plot(iso_849.age_ka, (iso_849.d18O - 0.64), **dict_849)'''

    '''# 607 data
    axs[pos_mg_ca].plot(te_607.age_ka, te_607.MgCa, **dict_607)
    axs[pos_bwt].plot(te_607.age_ka, te_607.BWT, **dict_607)
    axs[pos_sw].plot(te_607.age_ka, te_607.d18O_sw, **dict_607)
    axs[pos_d18o].plot(iso_607.age_ka, (iso_607.d18O - 0.64), **dict_607)'''

    # Add legends
    for ax in axs:
        ax.legend(frameon=False, shadow=False)

    # Invert the axes of the d18O plots
    axs[pos_sw].invert_yaxis()
    axs[pos_d18o].invert_yaxis()

    # Label the y-axes for the various plots
    axs[pos_bwt].set(ylabel="BWT ({})".format(u'\N{DEGREE SIGN}C'))
    axs[pos_d18o].set(ylabel='Cibicidoides {} ({})'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[pos_sw].set(ylabel='Modelled {} ({})'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))
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
        plt.savefig("figures/meeting/{}.png".format(save_title), format='png')
    else:
        plt.show()


if __name__ == "__main__":
    # Change to parent directory
    os.chdir("../..")
    # Plot the relevant graphs
    meeting_plot(save_fig=False, save_title='Figure_01')

    iso_1313 = clean_and_sort(pd.read_csv("data/cores/U1313_cibs_adj.csv"), "d18O")
    iso_607 = clean_and_sort(pd.read_csv("data/cores/607_cibs_adj.csv"), "d18O")
    te_1313 = clean_and_sort(pd.read_csv("data/cores/U1313_te.csv"), "MgCa")
    te_607 = clean_and_sort(pd.read_csv("data/cores/607_te.csv"), "MgCa")

    fig, axs = plt.subplots(nrows=3, sharex=True)
    fig.subplots_adjust(hspace=0)

    axs[0].plot(iso_1313.age_ka, (iso_1313.d18O - 0.64), marker='+', label='U1313')
    axs[0].plot(iso_607.age_ka, (iso_607.d18O - 0.64), marker='+', label='607')
    axs[0].set(ylabel='Cibicidoides {} ({})'.format(r'$\delta^{18}$O', u"\u2030"), xlabel="Age (ka)", xlim=[2400, 3200])
    axs[0].legend(frameon=False)
    axs[0].invert_yaxis()

    axs[1].plot(te_1313.age_ka, te_1313.MgCa, marker='+', label='U1313')
    axs[1].plot(te_607.age_ka, te_607.MgCa, marker='+', label='607')
    axs[1].set(ylabel='Mg/Ca (mmol/mol)', xlabel="Age (ka)", xlim=[2400, 3200])
    axs[1].legend(frameon=False)

    axs[2].plot(te_1313.age_ka, te_1313.BWT, marker='+', label='U1313')
    axs[2].plot(te_607.age_ka, te_607.BWT, marker='+', label='607')
    axs[2].set(ylabel='BWT', xlabel="Age (ka)", xlim=[2400, 3200])
    axs[2].legend(frameon=False)

    plt.show()

