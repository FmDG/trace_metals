import pandas as pd
import matplotlib.pyplot as plt
import os


def corruption_test(save_fig=False):

    os.chdir("../..")

    # Load the trace element data
    te_1209 = pd.read_csv("data/1209_TE_Full.csv")

    # Load the colour palette
    colours = ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e']

    # Define the number of plots
    num_plots = 5

    if save_fig:
        fig, axs = plt.subplots(num_plots, 1, sharex=True, figsize=(8.25, 11.75))
    else:
        fig, axs = plt.subplots(num_plots, 1, sharex=True)

    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)
    # Name the Plots
    fig.suptitle("Comparison of Trace Elements - 1209")

    i = 0

    axs[i].plot(te_1209.mcd, te_1209.MgCa, marker="+", color=colours[i])
    axs[i].set(ylabel="Mg/Ca (mmol/mol)")
    i += 1

    axs[i].plot(te_1209.mcd, te_1209.BCa, marker="+", color=colours[i])
    axs[i].set(ylabel="B/Ca  ({}/mol)".format(r'$\mu$mol'))
    i += 1

    axs[i].plot(te_1209.mcd, te_1209.MnCa, marker="+", color=colours[i])
    axs[i].set(ylabel="Mn/Ca ({}/mol)".format(r'$\mu$mol'))
    i += 1

    axs[i].plot(te_1209.mcd, te_1209.AlCa, marker="+", color=colours[i])
    axs[i].set(ylabel="Al/Ca ({}/mol)".format(r'$\mu$mol'))
    i += 1

    axs[i].plot(te_1209.mcd, te_1209.FeCa, marker="+", color=colours[i])
    axs[i].set(ylabel="Fe/Ca ({}/mol)".format(r'$\mu$mol'))
    i += 1

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
    axs[(num_plots - 1)].set(xlabel='Depth (mcd)')

    if save_fig:
        plt.savefig("figures/TE_and_PSU_data/corruption_test.pdf", format="pdf")
    else:
        plt.show()


if __name__ == "__main__":
    corruption_test(save_fig=False)
