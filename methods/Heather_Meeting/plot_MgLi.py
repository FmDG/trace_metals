import os

import pandas as pd
import matplotlib.pyplot as plt


def plot_mg_li(save_fig=False, figure_name="Mg_Li"):
    te_1014 = pd.read_csv("data/cores/1014_te.csv")
    te_1018 = pd.read_csv("data/cores/1018_te.csv")
    te_1209 = pd.read_csv("data/cores/1209_te.csv")
    te_1208 = pd.read_csv("data/cores/1208_te.csv")
    psu_1209 = pd.read_csv("data/cores/1209_psu.csv")
    psu_1208 = pd.read_csv("data/cores/1208_psu.csv")

    num_plots = 3
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
    fig.suptitle("Comparison of Mg/Li and Mg/Ca\n ({} - {} ka)".format(min_age, max_age))

    # Plot the MgCa
    # axs[0].plot(te_1018.age_ka, te_1018.MgCa, color=colours[0], linestyle="-", marker="+", label="1018")
    # axs[0].plot(te_1014.age_ka, te_1014.MgCa, color=colours[1], linestyle="-", marker="+", label="1014")
    axs[0].plot(te_1208.age_ka, te_1208.MgCa, color=colours[2], linestyle="-", marker="+", label="1208")
    axs[0].plot(te_1209.age_ka, te_1209.MgCa, color=colours[3], linestyle="-", marker="+", label="1209")
    # Label the y-axis
    axs[0].set(ylabel='{} ({})'.format('Mg/Ca', 'mmol/mol'))
    axs[0].legend()

    # Plot the MgLi
    # axs[1].plot(te_1018.age_ka, (te_1018.MgCa/te_1018.LiCa), color=colours[0], linestyle="-", marker="+", label="1018")
    # axs[1].plot(te_1014.age_ka, (te_1014.MgCa/te_1014.LiCa), color=colours[1], linestyle="-", marker="+", label="1014")
    axs[1].plot(te_1209.age_ka, (te_1209.MgCa/te_1209.LiCa), color=colours[3], linestyle="-", marker="+", label="1209")
    # Label the y-axis
    axs[1].set(ylabel='{} ({})'.format('Mg/Li', r'mmol/$\mu$mol'))

    # Plot the Temp
    # axs[2].plot(te_1018.age_ka, te_1018.BWT, color=colours[0], linestyle="-", marker="+", label="1018")
    # axs[2].plot(te_1014.age_ka, te_1014.BWT, color=colours[1], linestyle="-", marker="+", label="1014")
    axs[2].plot(psu_1208.age_ka, psu_1208.BWT, color=colours[2], linestyle="-", marker="+", label="1208")
    axs[2].plot(psu_1209.age_ka, psu_1209.BWT, color=colours[3], linestyle="-", marker="+", label="1209")
    # Label the y-axis
    axs[2].set(ylabel='Modelled {} ({})'.format('Temperatures', u'\N{DEGREE SIGN}C'))

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
        plt.savefig("figures/Mg_Li_comparison/{}_{}-{}.pdf".format(figure_name, min_age, max_age), format="pdf")
    else:
        plt.show()


if __name__ == "__main__":
    os.chdir("../..")
    plot_mg_li(save_fig=True, figure_name="MgLi_1208-09")
