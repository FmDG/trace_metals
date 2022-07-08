import pandas as pd
import os
import matplotlib.pyplot as plt


def psu_plots_by_run(min_age=2400, max_age=2900, num_runs=2, save_fig=False, figure_name="FIGURE", fill=True):

    # Colours and Lines
    colours = ['#66c2a5', '#fc8d62', '#8da0cb']
    lines = ["dotted", "dashed", "dashdot"]

    # The number of plots that we're looking at - here it is just modelled temperature and d18O_sw
    num_plots = 2

    # Store the datasets for all the runs
    datasets = []
    for x in range(num_runs):
        # Load the datasets
        data_607 = pd.read_csv("data/PSU_Solver/RUN_{}/run_607.csv".format((x + 1)))
        data_1208 = pd.read_csv("data/PSU_Solver/RUN_{}/run_1208.csv".format(x + 1))
        data_1209 = pd.read_csv("data/PSU_Solver/RUN_{}/run_1209.csv".format((x + 1)))
        datasets.append([[data_1209, "1209"], [data_1208, "1208"], [data_607, "607"]])

    # Set up figure
    if save_fig:
        fig, axs = plt.subplots(num_plots, 1, sharex=True, figsize=(8.25, 11.75))
    else:
        fig, axs = plt.subplots(num_plots, 1, sharex=True)
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    # Name the Plot
    fig.suptitle("Comparison of Sites 607/1208/1209\n ({} - {} ka)".format(min_age, max_age))

    # For each run...
    for x in range(num_runs):
        # and each dataset...
        for y in range(len(datasets[x])):
            # plot the temperature against age,
            axs[0].plot(datasets[x][y][0]["age_ka"], datasets[x][y][0]["temp"], color=colours[y], linestyle=lines[y], label="{} Run {}".format(datasets[x][y][1], (x + 1)))
            # and if desired, fill in the error bars
            if fill:
                axs[0].fill_between(datasets[x][y][0]["age_ka"], datasets[x][y][0]["temp_min1"], datasets[x][y][0]["temp_plus1"], alpha=0.1, facecolor=colours[y])

    # Label the y-axis
    axs[0].set(ylabel='Modelled {} ({})'.format('Temperature', u'\N{DEGREE SIGN}C'))
    # Add a legend
    axs[0].legend(loc='upper left', shadow=False, frameon=False)

    # Repeat the above for the modelled d18Osw
    for x in range(num_runs):
        for y in range(len(datasets[x])):
            axs[1].plot(datasets[x][y][0]["age_ka"], datasets[x][y][0]["d18O_sw"], color=colours[y], linestyle=lines[y], label="{} Run {}".format(datasets[x][y][1], (x + 1)))
            if fill:
                axs[1].fill_between(datasets[x][y][0]["age_ka"], datasets[x][y][0]["d18O_min1"], datasets[x][y][0]["d18O_plus1"], alpha=0.1, facecolor=colours[y])

    # Label the y-axis
    axs[1].set(ylabel='Modelled {} ({})'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))

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

    # Either save or display the figure
    if save_fig:
        plt.savefig("figures/TE_and_PSU_data/{}_{}-{}.pdf".format(figure_name, min_age, max_age), format="pdf")
    else:
        plt.show()


if __name__ == "__main__":
    # Change to the relevant directory
    os.chdir("../..")
    psu_plots_by_run(fill=False, save_fig=True, num_runs=4, figure_name="Multi_Runs")
