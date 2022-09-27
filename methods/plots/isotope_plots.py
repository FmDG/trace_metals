import matplotlib.pyplot as plt


def basic_plot(datasets, age_min=2400, age_max=3400, save_fig=False, figure_name='Figure_1', colours=None):
    # load the colours
    if colours is None:
        colours = ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e']

    # check the number of plots
    n_plots = len(datasets)
    if n_plots > 5:
        raise ValueError("Maximum number of plots = 5")
    # Check the input is correct
    if not (isinstance(age_min, int) and isinstance(age_max, int)):
        raise ValueError("Age inputs must be integers")
    for entry in datasets:
        if len(entry) != 3:
            raise ValueError('Dataset entries to be formatted as follows\n[Series(age_ka), Series(value), Name(Value)]')
        if len(entry[0]) != len(entry[1]):
            raise ValueError('Age_ka and Value are not of the same length')

    # Define the plot
    if save_fig:
        fig, axs = plt.subplots(nrows=n_plots, ncols=1, figsize=(19.6, 16.7), sharex='all')
    else:
        fig, axs = plt.subplots(nrows=n_plots, ncols=1, sharex='all')
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    for x in range(n_plots):
        axs[x].plot(datasets[x][0], datasets[x][1], color=colours[x])
        axs[x].set(ylabel=datasets[x][2])

    # Remove the various axes to clean up the plot
    for q in range(n_plots):
        # Remove the left/right axes to make the plot look cleaner
        if q % 2 == 1:
            axs[q].yaxis.set(ticks_position="right", label_position='right')
            axs[q].spines['left'].set_visible(False)
        else:
            axs[q].spines['right'].set_visible(False)
        axs[q].spines['top'].set_visible(False)
        axs[q].spines['bottom'].set_visible(False)

    # Set the bottom axis on and label it with the age.
    axs[(n_plots - 1)].spines['bottom'].set_visible(True)
    axs[(n_plots - 1)].set(xlabel='Age (ka)', xlim=[age_min, age_max])

    if save_fig:
        plt.savefig("figures/basic_plots/{}.png".format(figure_name), format='png')
    else:
        plt.show()
