import matplotlib.pyplot as plt
import numpy as np
import ruptures as rpt

from methods.interpolations.generate_interpolations import generate_interpolation
from objects.arguments.args_Nature import colours as clr
from objects.core_data.isotopes import iso_1208, iso_1209
from objects.core_data.psu import psu_1208, psu_1209


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


def change_points_interp(data_array, time_array, known_bkp=True, n=1):
    data_array = normalise_array(data_array)

    # Detect the change-point or points
    if known_bkp:
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


def bwt_change_points(n: int = 1, save_fig: bool = False):
    """
    Generates the change points for the BWT record from 1208 and 1209.
    :param n: number of change points
    :param save_fig: boolean to determine if the figure should be saved after.
    :return: No return.
    """

    use_1209 = psu_1209[psu_1209.age_ka < 2900]

    # Find the change-points
    cp_1209 = find_change_point(use_1209, "temp", n=n, known_bkps=True)
    cp_1208 = find_change_point(psu_1208, "temp", n=n, known_bkps=True)

    # Display the elements
    num_plots = 2
    fig, axs = plt.subplots(nrows=num_plots, figsize=(12, 8), sharex='all')
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    axs[0].plot(use_1209.age_ka, use_1209.temp, marker='+', color=clr[1], label="1209")
    for x in cp_1209:
        axs[0].axvline(x, ls='--', color=clr[2], label='Change-point = {} ka'.format(x))
    axs[0].set(ylabel="BWT ({})".format(u'\N{DEGREE SIGN}C'))

    axs[1].plot(psu_1208.age_ka, psu_1208.temp, marker='+', color=clr[0], label="1208")
    for x in cp_1208:
        axs[1].axvline(x, ls='--', color=clr[2], label='Change-point = {} ka'.format(x))
    axs[1].set(ylabel="BWT ({})".format(u'\N{DEGREE SIGN}C'))

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

    # Save the figure if required
    if save_fig:
        plt.savefig("figures/changepoints/changepoints_BWT.png", format="png", dpi=300)
    else:
        plt.show()


def iso_change_points(n=1, save_fig: bool = True):
    """
    Finds the changepoint (the point where there is a marked change in the signal) across the isotope record from
    Site 1208 and 1209.
    :param n: number of changepoints
    :param save_fig: boolean to determine if the figure should be saved or no.
    :return:
    """
    # Limit the isotope record to the study period (2400 - 3400 ka).
    age_start = 2400
    age_end = 3400

    # Limit d18O sets
    use_1208 = iso_1208[iso_1208.age_ka.between(age_start, age_end)]
    use_1209 = iso_1209[iso_1209.age_ka.between(age_start, age_end)]

    # Generate interpolations for the dataset with frequency fs
    interp_1208, age_array = generate_interpolation(use_1208, fs=0.1, pchip=False)
    interp_1209, _ = generate_interpolation(use_1209, fs=0.1, pchip=False)

    # Find the change points in the interpolated datasets.
    cp_1208 = change_points_interp(interp_1208, age_array, known_bkp=True, n=n)
    cp_1209 = change_points_interp(interp_1209, age_array, known_bkp=True, n=n)

    # Display the elements
    num_plots = 2
    fig, axs = plt.subplots(nrows=num_plots, figsize=(12, 8), sharex='all')
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    axs[0].plot(use_1209.age_ka, use_1209.d18O_unadj, marker='+', color=clr[1], label="1209")
    for x in cp_1209:
        axs[0].axvline(x, ls='--', color=clr[2], label='Change-point = {:.2f} ka'.format(x))
    axs[0].set(ylabel='{} ({})'.format(r'$\delta^{18}$O', u"\u2030"))

    axs[1].plot(use_1208.age_ka, use_1208.d18O_unadj, marker='+', color=clr[0], label="1208")
    for x in cp_1208:
        axs[1].axvline(x, ls='--', color=clr[2], label='Change-point = {:.2f} ka'.format(x))
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

    # Save the figure if required
    if save_fig:
        plt.savefig("figures/changepoints/changepoints_d18O.png", format="png", dpi=300)
    else:
        plt.show()


def diff_change_points(n=1, save_fig: bool = False):
    """
    Finds the changepoint in the Dd18O record between 1208 and 1209
    :param n: number of change points in the record
    :param save_fig: save the resultant figure or no.
    :return:
    """
    age_start = 2400
    age_end = 3400

    # Limit d18O sets
    use_1208 = iso_1208[iso_1208.age_ka.between(age_start, age_end)]
    use_1209 = iso_1209[iso_1209.age_ka.between(age_start, age_end)]

    # Generate interpolations
    interp_1208, age_array = generate_interpolation(use_1208, fs=0.1, pchip=False)
    interp_1209, _ = generate_interpolation(use_1209, fs=0.1, pchip=False)

    differences = (interp_1208 - interp_1209)

    cp_diff = change_points_interp(differences, age_array, known_bkp=True, n=n)

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.plot(age_array, differences, color=clr[0])
    for x in cp_diff:
        ax.axvline(x, ls='--', color=clr[2], label='Change-point = {:.2f} ka'.format(x))
    ax.set(xlabel="Age (ka)", ylabel=r'$\Delta \delta^{18}$O', xlim=[age_start, age_end])
    ax.invert_yaxis()
    ax.legend(frameon=False, shadow=False)

    # Save the figure if required
    if save_fig:
        plt.savefig("figures/changepoints/change_points_Dd18O.png", format="png", dpi=300)
    else:
        plt.show()


if __name__ == "__main__":
    iso_change_points(save_fig=True)
    # diff_change_points(save_fig=False)
    bwt_change_points(save_fig=True)
