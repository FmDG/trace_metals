import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ruptures as rpt

from methods.interpolations.isotope_interpolations import generate_interpolation
from objects.colours import dark_02


def normalise_array(data_array):
    return (data_array - np.min(data_array)) / (np.max(data_array) - np.min(data_array))


def find_change_point(dataset, value, n=1, known_bkps=False):
    # Convert data to numpy
    data_array = dataset[value].to_numpy()
    time_array = dataset.age_ka.to_numpy()

    data_array = normalise_array(data_array)

    # Detect the change-point or points
    if known_bkps:
        algo = rpt.Dynp(model="rbf").fit(data_array)
        result = algo.predict(n_bkps=n)
    else:
        algo = rpt.Pelt(model="rbf").fit(data_array)
        result = algo.predict(pen=n)

    # Remove the final element
    result.pop(-1)
    # Save the change-point (or points)
    changepoint = time_array[result]

    return changepoint


def change_points_interp(data_array, time_array, known_bkps=True, n=1):
    data_array = normalise_array(data_array)

    # Detect the change-point or points
    if known_bkps:
        algo = rpt.Dynp(model="rbf").fit(data_array)
        result = algo.predict(n_bkps=n)
    else:
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
    cp_1209 = find_change_point(te_1209, "MgCa", n=n, known_bkps=True)
    cp_1208 = find_change_point(te_1208, "MgCa", n=n, known_bkps=True)

    # Display the elements
    num_plots = 2
    fig, axs = plt.subplots(nrows=num_plots, figsize=(12, 8), sharex='all')
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    axs[0].plot(te_1209.age_ka, te_1209.MgCa, marker='+', color=dark_02[1], label="1209")
    for x in cp_1209:
        axs[0].axvline(x, ls='--', color=dark_02[2], label='Change-point = {} ka'.format(x))
    axs[0].set(ylabel='Mg/Ca (mmol/mol)')

    axs[1].plot(te_1208.age_ka, te_1208.MgCa, marker='+', color=dark_02[0], label="1208")
    for x in cp_1208:
        axs[1].axvline(x, ls='--', color=dark_02[2], label='Change-point = {} ka'.format(x))
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


def iso_change_points(n=1, fs=0.1):
    age_start = 2400
    age_end = 3400

    # Load the dataset
    iso_1209 = pd.read_csv("data/cores/1209_cibs.csv")
    iso_1208 = pd.read_csv("data/cores/1208_cibs.csv")

    # Limit d18O sets
    iso_1208 = iso_1208[iso_1208.age_ka.between(age_start, age_end)]
    iso_1209 = iso_1209[iso_1209.age_ka.between(age_start, age_end)]

    # Generate interpolations
    interp_1208, age_array = generate_interpolation(iso_1208, fs=fs, pchip=False)
    interp_1209, _ = generate_interpolation(iso_1209, fs=fs, pchip=False)

    cp_1208 = change_points_interp(interp_1208, age_array, known_bkps=True, n=n)
    cp_1209 = change_points_interp(interp_1209, age_array, known_bkps=True, n=n)

    # Display the elements
    num_plots = 2
    fig, axs = plt.subplots(nrows=num_plots, figsize=(12, 8), sharex='all')
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, marker='+', color=dark_02[1], label="1209")
    for x in cp_1209:
        axs[0].axvline(x, ls='--', color=dark_02[2], label='Change-point = {:.2f} ka'.format(x))
    axs[0].set(ylabel='{} ({})'.format(r'$\delta^{18}$O', u"\u2030"))

    axs[1].plot(iso_1208.age_ka, iso_1208.d18O_unadj, marker='+', color=dark_02[0], label="1208")
    for x in cp_1208:
        axs[1].axvline(x, ls='--', color=dark_02[2], label='Change-point = {:.2f} ka'.format(x))
    axs[1].set(ylabel='{} ({})'.format(r'$\delta^{18}$O', u"\u2030"))

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
    axs[(num_plots - 1)].set(xlabel='Age (ka)')

    plt.show()


def diff_change_points(n=1, known_bkps=True, fs=0.1):
    age_start = 2400
    age_end = 3400

    # Load the dataset
    iso_1209 = pd.read_csv("data/cores/1209_cibs.csv")
    iso_1208 = pd.read_csv("data/cores/1208_cibs.csv")

    # Limit d18O sets
    iso_1208 = iso_1208[iso_1208.age_ka.between(age_start, age_end)]
    iso_1209 = iso_1209[iso_1209.age_ka.between(age_start, age_end)]

    # Generate interpolations
    interp_1208, age_array = generate_interpolation(iso_1208, fs=fs, pchip=False)
    interp_1209, _ = generate_interpolation(iso_1209, fs=fs, pchip=False)

    differences = (interp_1208 - interp_1209)

    cp_diff = change_points_interp(differences, age_array, known_bkps=known_bkps, n=n)

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.plot(age_array, differences, color=dark_02[0])
    for x in cp_diff:
        ax.axvline(x, ls='--', color=dark_02[2], label='Change-point = {:.2f} ka'.format(x))
    ax.set(xlabel="Age (ka)", ylabel=r'$\Delta \delta^{18}$O', xlim=[age_start, age_end])
    ax.invert_yaxis()
    ax.legend(frameon=False, shadow=False)

    plt.show()


if __name__ == "__main__":
    os.chdir('../..')
    iso_change_points(n=1, fs=0.1)
