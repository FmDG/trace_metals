import matplotlib.pyplot as plt

import objects.arguments.args_Nature as args
from methods.figures.tick_dirs import tick_dirs
from objects.core_data.isotopes import iso_1208, iso_1209
from objects.core_data.psu import psu_1208, psu_1209


def pliocene_reference_figure():
    new_1208, new_1209, min_age, max_age = pliocene_inset()
    # new_1208, new_1209, min_age, max_age = pliocene_reference()

    # Plots for d18O_benthic and BWT
    num_plots = 2

    # Define the figure
    fig, axs = plt.subplots(
        nrows=num_plots,
        ncols=1,
        sharex="all",
        figsize=(4, 4)
    )

    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)
    # Name the Plot
    fig.suptitle("Comparison of Sites 1208 and 1209\n ({} - {} ka)".format(min_age, max_age))

    # -- Plot the 1208 data --
    # d18O original data
    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args.args_1208)

    # PSU BWT estimates
    axs[1].plot(new_1208.age_ka, new_1208.temp, **args.args_1208)
    axs[1].fill_between(new_1208.age_ka, new_1208.temp_min1, new_1208.temp_plus1, **args.fill_1208)

    # -- Plot the 1209 data --
    # d18O original data
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args.args_1209)
    # PSU BWT estimates
    axs[1].plot(new_1209.age_ka, new_1209.temp, **args.args_1209)
    axs[1].fill_between(new_1209.age_ka, new_1209.temp_min1, new_1209.temp_plus1, **args.fill_1209)

    # -- Define the axes --
    axs[0].set(ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[1].set(ylabel="BWT ({})".format(u'\N{DEGREE SIGN}C'))

    # Invert the axes with d18O
    axs[0].invert_yaxis()

    # Decide which Tick Directions function you want to run.
    # tick_dirs_both(axs, num_plots, min_age, max_age)
    tick_dirs(axs, num_plots, min_age, max_age, legend=False)

    # Save the figure if required
    plt.show()

    return 1


def pliocene_inset():
    new_1209 = psu_1209[psu_1209.age_ka > 2900]
    new_1208 = psu_1208[psu_1208.age_ka.between(3050, 3150)]
    return new_1208, new_1209, 3050, 3150


def pliocene_reference():
    pliocene_1209 = psu_1209[psu_1209.age_ka > 2900]
    mpwp_1209_temp = pliocene_1209.temp.mean()

    pliocene_1208 = psu_1208[psu_1208.age_ka.between(3060, 3110)]
    mpwp_1208_temp = pliocene_1208.temp.mean()

    new_1209 = psu_1209[psu_1209.age_ka < 2900]
    new_1208 = psu_1208[psu_1208.age_ka < 2900]
    return new_1208, new_1209, 2400, 2900


if __name__ == "__main__":
    pliocene_reference_figure()
