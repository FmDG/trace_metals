import os

import pandas as pd
import matplotlib.pyplot as plt


def isotope_plot():
    # Load the datasets
    iso_1208 = pd.read_csv("data/cores/1208_cibs.csv")
    iso_1209 = pd.read_csv("data/cores/1209_cibs.csv")

    # Remove missing
    iso_1208 = iso_1208.dropna()
    iso_1209 = iso_1209.dropna()

    # Set up the colours
    colour_1208 = '#1b9e77'
    colour_1209 = '#d95f02'
    colour_other = '#7570b3'

    # Set up the figure
    fig, ax = plt.subplots(1, figsize=(19, 10), sharex=True)

    ax.plot(iso_1209.age_ka, iso_1209.d18O_unadj, label="1209", color=colour_1209, mec=colour_1209, marker='o', mfc=(1,1,1,0))
    ax.plot(iso_1208.age_ka, iso_1208.d18O_unadj, label="1208", color=colour_1208, mec=colour_1208, marker='D', mfc=(1,1,1,0))
    ax.set(ylabel='{} ({})'.format(r'$\delta^{18}$O', u"\u2030"), xlabel='Age (ka)', xlim=[2350, 3600])
    ax.invert_yaxis()
    ax.legend()

    # plt.savefig("figures/poster/isotopes.svg", format="svg")
    # plt.show()


def core_plots():
    # Load the datasets
    iso_1208 = pd.read_csv("data/cores/1208_cibs.csv")
    iso_1209 = pd.read_csv("data/cores/1209_cibs.csv")
    # Other datasets (0.64 too high)
    iso_607 = pd.read_csv("data/cores/607_cibs_adj.csv")
    iso_849 = pd.read_csv("data/cores/849_cibs_adj.csv")
    iso_1313 = pd.read_csv("data/cores/U1313_cibs_adj.csv")

    # N Atlantic datasets (0.64 too high)
    iso_981 = pd.read_csv("data/cores/981_cibs_adj.csv")
    iso_982 = pd.read_csv("data/cores/982_cibs_adj.csv")

    # Define the age limits
    age_min, age_max = 2300, 3300

    num_plots = 3
    fig, axs = plt.subplots(num_plots, 1, sharex=True)
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    # Plot all North Atlantic records
    axs[0].plot(iso_607.age_ka, (iso_607.d18O - 0.64), label="607")
    axs[0].plot(iso_1313.age_ka, (iso_1313.d18O - 0.64), label="U1313")
    axs[0].plot(iso_981.age_ka, (iso_981.d18O - 0.64), label="981")
    axs[0].plot(iso_982.age_ka, (iso_982.d18O - 0.64), label="982")
    axs[0].set(ylabel='{} ({})'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[0].invert_yaxis()
    axs[0].legend()

    # Plot the 607 and U1313 records
    axs[1].plot(iso_607.age_ka, (iso_607.d18O - 0.64), label="607")
    axs[1].plot(iso_1313.age_ka, (iso_1313.d18O - 0.64), label="U1313")
    axs[1].set(ylabel='{} ({})'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[1].invert_yaxis()
    axs[1].legend()

    # Plot the 981 and 982 records
    axs[2].plot(iso_981.age_ka, (iso_981.d18O - 0.64), label="981")
    axs[2].plot(iso_982.age_ka, (iso_982.d18O - 0.64), label="982")
    axs[2].set(ylabel='{} ({})'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[2].invert_yaxis()
    axs[2].legend()

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

    plt.show()



if __name__ == "__main__":
    os.chdir("../..")
    # isotope_plot()
    core_plots()
