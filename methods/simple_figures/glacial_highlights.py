import matplotlib.pyplot as plt

from methods.interpolations.generate_interpolations import generate_interpolation
from methods.figures.tick_dirs import tick_dirs
from objects.core_data.isotopes import iso_1209, iso_1208
from objects.core_data.lr04 import iso_lr04
from objects.core_data.psu import psu_1208, psu_1209
from objects.args_brewer import args_1209, args_1208, args_diff, fill_1208, fill_1209


def glacial_highlights(age_min: int = 2400, age_max: int = 2900):
    # We use a simple 1D interpolation, with a density of "freq"
    freq = 0.1
    interp_lr04, age_array = generate_interpolation(iso_lr04, fs=freq, start=age_min, end=age_max, pchip=False, value="d18O")

    threshold = 3.64
    glacials = (interp_lr04 > threshold)

    # Generate a plot to display this
    num_plots = 2
    fig, axs = plt.subplots(num_plots, sharex="all", figsize=(14, 6))
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    # Plot the oxygen isotope records from LR04
    # axs[0].plot(age_array, interp_lr04, label="LR04", c='k')
    # axs[0].fill_between(age_array, interp_lr04, threshold, fc='b', ec=None, alpha=0.2)
    # axs[0].set(ylabel='Benthic {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    # axs[0].plot([age_min, age_max], [threshold, threshold], '--', color='k', linewidth=1.0, label='Threshold = {} {}'.format(threshold, u"\u2030"))

    # Plot the oxygen isotope records from 1208 and 1209
    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)
    axs[0].set(ylabel='Benthic {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))

    # PSU BWT estimates
    axs[1].plot(psu_1208.age_ka, psu_1208.temp, **args_1208)
    axs[1].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, **fill_1208)
    axs[1].plot(psu_1209.age_ka, psu_1209.temp, **args_1209)
    axs[1].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, **fill_1209)

    # Label the position of the glacials
    axs[0].fill_between(age_array, (glacials * 5), 0.25, fc='b', ec=None, alpha=0.1, label="Glacial periods")
    axs[1].fill_between(age_array, ((glacials * 10) - 5), -5, fc='b', ec=None, alpha=0.1, label="Glacial periods")
    axs[0].set_ylim(4, 2)
    axs[1].set_ylim(-2.5, 4.0)

    # Remove the various axes to clean up the plot
    tick_dirs(axs, num_plots=num_plots, min_age=age_min, max_age=age_max, legend=False)

    axs[0].legend(frameon=False, shadow=False)

    plt.show()
