import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import matplotlib

from objects.args_blues import args_1209, args_1208, fill_1208, fill_1209
from methods.figures.tick_dirs import tick_dirs, tick_dirs_both
from objects.core_data.isotopes import iso_607, iso_1208, iso_1209
from objects.core_data.psu import psu_1208, psu_1209, psu_607


# Increase the font size to 24
matplotlib.rcParams.update({'font.size': 20})


def figure_one(save_fig: bool = False):

    age_max = 3600
    age_min = 2300

    # Define the figure
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        sharex="all",
        figsize=(31.496, 7.874)
    )

    fig.subplots_adjust(left=0.05, right=0.99, bottom=0.1, top=0.99)

    # d18O original data
    ax.plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)
    ax.plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)

    # -- Define the axes --
    ax.set(ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))

    # Invert the axes with d18O
    ax.invert_yaxis()

    # Add a legend
    ax.legend(shadow=False, frameon=False)

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_minor_locator(AutoMinorLocator(20))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))

    # Set the bottom axis on and label it with the age.
    ax.set(xlabel='Age (ka)', xlim=[age_min, age_max])

    if save_fig:
        plt.savefig("figures/poster/Figure_1_alt.png", format="png", dpi=300)
    else:
        plt.show()


def figure_two(save_fig: bool = False):
    # Plots for d18O_benthic, BWT and d18O_sw.
    num_plots = 3
    min_age, max_age = 2450, 2850

    # Define the figure
    fig, axs = plt.subplots(
        nrows=num_plots,
        ncols=1,
        sharex="all",
        figsize=(15.7, 13.7)
    )

    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0, left=0.08, right=0.93, bottom=0.08, top=0.99)

    new_psu_1209 = psu_1209[psu_1209.age_ka.between(min_age, max_age)]
    new_psu_1208 = psu_1208[psu_1208.age_ka.between(min_age, max_age)]

    # -- Plot the 1208 data --
    # d18O original data
    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)

    # PSU BWT estimates
    axs[1].plot(new_psu_1208.age_ka, new_psu_1208.temp, **args_1208)
    axs[1].fill_between(new_psu_1208.age_ka, new_psu_1208.temp_min1, new_psu_1208.temp_plus1, **fill_1208)
    # PSU d18O_sw estimates
    axs[2].plot(new_psu_1208.age_ka, new_psu_1208.d18O_sw, **args_1208)
    axs[2].fill_between(new_psu_1208.age_ka, new_psu_1208.d18O_min1, new_psu_1208.d18O_plus1, **fill_1208)

    # -- Plot the 1209 data --
    # d18O original data
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)
    # PSU BWT estimates
    axs[1].plot(new_psu_1209.age_ka, new_psu_1209.temp, **args_1209)
    axs[1].fill_between(new_psu_1209.age_ka, new_psu_1209.temp_min1, new_psu_1209.temp_plus1, **fill_1209)
    # PSU d18O_sw estimates
    axs[2].plot(new_psu_1209.age_ka, new_psu_1209.d18O_sw, **args_1209)
    axs[2].fill_between(new_psu_1209.age_ka, new_psu_1209.d18O_min1, new_psu_1209.d18O_plus1, **fill_1209)

    # -- Define the axes --
    axs[0].set(ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[1].set(ylabel="BWT ({})".format(u'\N{DEGREE SIGN}C'))
    axs[2].set(ylabel='Derived {} ({} VPDB)'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))

    # Invert the axes with d18O
    axs[0].invert_yaxis()
    axs[2].invert_yaxis()

    # Decide which Tick Directions function you want to run.
    # tick_dirs_both(axs, num_plots, min_age, max_age)
    tick_dirs(axs, num_plots, min_age, max_age, legend=False)

    axs[0].legend(shadow=False, frameon=False)

    # Save the figure if required
    if save_fig:
        plt.savefig("figures/poster/Figure_2_alt.png", format="png", dpi=300)
    else:
        plt.show()


if __name__ == "__main__":
    figure_one(save_fig=False)
    figure_two(save_fig=True)
