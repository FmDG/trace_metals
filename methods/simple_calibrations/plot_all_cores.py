import os

import matplotlib.pyplot as plt
import pandas as pd


def plot_all_cores(save_fig=False, is607=True, is1208=True, is1209=True, is1014=False, is1018=False, is1313=False,
                   is849=True, max_age=3000, min_age=2400, figure_name="ComparingCores"):
    # Load the datasets
    num_data = is849 + is607 + is1313 + is1014 + is1018 + is1209 + is1208
    if num_data == 0:
        raise ValueError("Must have at least one dataset plotted")
    datasets = []
    if is1209:
        is_1209 = pd.read_csv("data/cores/1209_cibs.csv")
        te_1209 = pd.read_csv("data/cores/1209_te.csv")
        psu_1209 = pd.read_csv("data/cores/1209_psu.csv")
        datasets.append({"Isotopes": is_1209, "TE": te_1209, "BWT": psu_1209, "Name": '1209'})
    if is1208:
        is_1208 = pd.read_csv("data/cores/1208_cibs.csv")
        te_1208 = pd.read_csv("data/cores/1208_te.csv")
        psu_1208 = pd.read_csv("data/cores/1208_psu.csv")
        datasets.append({"Isotopes": is_1208, "TE": te_1208, "BWT": psu_1208, "Name": '1208'})
    if is607:
        is_607 = pd.read_csv("data/cores/607_cibs_adj.csv")
        te_607 = pd.read_csv("data/cores/607_te.csv")
        datasets.append({"Isotopes": is_607, "TE": te_607, "BWT": te_607, "Name": '607'})
    if is849:
        is_849 = pd.read_csv("data/cores/849_cibs_adj.csv")
        te_849 = pd.read_csv("data/cores/849_te.csv")
        datasets.append({"Isotopes": is_849, "TE": te_849, "BWT": te_849, "Name": '849'})
    if is1014:
        is_1014 = pd.read_csv("data/cores/1014_cibs.csv")
        te_1014 = pd.read_csv("data/cores/1014_te.csv")
        datasets.append({"Isotopes": is_1014, "TE": te_1014, "BWT": te_1014, "Name": '1014'})
    if is1018:
        is_1018 = pd.read_csv("data/cores/1018_cibs.csv")
        te_1018 = pd.read_csv("data/cores/1018_te.csv")
        datasets.append({"Isotopes": is_1018, "TE": te_1018, "BWT": te_1018, "Name": '1018'})
    if is1313:
        is_1313 = pd.read_csv("data/cores/U1313_cibs_adj.csv")
        te_1313 = pd.read_csv("data/cores/U1313_te.csv")
        datasets.append({"Isotopes": is_1313, "TE": te_1313, "BWT": te_1313, "Name": 'U1313'})

    num_plots = 3
    colours = ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02', '#a6761d']

    # Set up figure
    if save_fig:
        fig, axs = plt.subplots(num_plots, 1, sharex=True, figsize=(8.25, 11.75))
    else:
        fig, axs = plt.subplots(num_plots, 1, sharex=True)
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    # Name the Plot
    fig.suptitle("Comparison of Core Sites\n ({} - {} ka)".format(min_age, max_age))

    # Plot the d18O
    for x in range(num_data):
        axs[0].plot(datasets[x]["Isotopes"].age_ka, datasets[x]["Isotopes"].d18O, color=colours[x], linestyle='-',
                    label=datasets[x]["Name"])
    # Label the y-axis
    axs[0].set(ylabel='{} ({})'.format(r'$\delta^{18}$O', u"\u2030"))

    # Plot the MgCa
    for x in range(num_data):
        axs[1].plot(datasets[x]["TE"].age_ka, datasets[x]["TE"].MgCa, color=colours[x], linestyle='-',
                    label=datasets[x]["Name"])
    # Label the y-axis
    axs[1].set(ylabel='{} ({})'.format('Mg/Ca', 'mmol/mol'))

    # Plot the Temperature
    for x in range(num_data):
        axs[2].plot(datasets[x]["BWT"].age_ka, datasets[x]["BWT"].BWT, color=colours[x], linestyle='-',
                    label=datasets[x]["Name"])
    # Label the y-axis
    axs[2].set(ylabel='Inferred {} ({})'.format('Temperatures', u'\N{DEGREE SIGN}C'))
    axs[0].legend()

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
        plt.savefig("figures/607_comparison/{}_{}-{}.pdf".format(figure_name, min_age, max_age), format="pdf")
    else:
        plt.show()


if __name__ == "__main__":
    os.chdir("../..")
    plot_all_cores(
        is1014=False,
        is1018=False,
        is1208=True,
        is1209=True,
        is1313=False,
        is607=True,
        is849=False,
        min_age=2400,
        max_age=2900,
        figure_name="comp_607_1014-18",
        save_fig=False
    )
