import os

import matplotlib.pyplot as plt
import pandas as pd
import ruptures as rpt


def find_change_point(dataset, value, n=1):
    # Convert data to numpy
    data_array = dataset[value].to_numpy()
    time_array = dataset.age_ka.to_numpy()

    # Detect the change-point or points
    algo = rpt.Pelt(model="rbf").fit(data_array)
    result = algo.predict(pen=n)

    # Remove the final element
    result.pop(-1)
    # Save the change-point (or points)
    changepoint = time_array[result]

    return changepoint


def te_change_points(limit_age=True, n=1):
    # Load the dataset
    te_1209 = pd.read_csv("data/cores/1209_te.csv")
    te_1208 = pd.read_csv("data/cores/1208_te.csv")

    if limit_age:
        # Limit data to the last 2900
        te_1209 = te_1209[te_1209.age_ka < 2900]

    # Find the change-points
    cp_1209 = find_change_point(te_1209, "MgCa", n=n)
    cp_1208 = find_change_point(te_1208, "MgCa", n=n)

    # Display the elements
    num_plots = 2
    fig, axs = plt.subplots(nrows=num_plots, figsize=(12, 8), sharex='all')
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    axs[0].plot(te_1209.age_ka, te_1209.MgCa, marker='+', label="1209")
    for x in cp_1209:
        axs[0].axvline(x, ls='--', color='r', label='Change-point = {} ka'.format(x))
    axs[0].set(ylabel='Mg/Ca (mmol/mol)')

    axs[1].plot(te_1208.age_ka, te_1208.MgCa, marker='+', label="1208")
    for x in cp_1208:
        axs[1].axvline(x, ls='--', color='r', label='Change-point = {} ka'.format(x))
    axs[1].set(ylabel='Mg/Ca (mmol/mol)')

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
    axs[(num_plots - 1)].set(xlabel='Age (ka)')

    plt.show()


if __name__ == "__main__":
    os.chdir('../..')
    te_change_points(n=5)
