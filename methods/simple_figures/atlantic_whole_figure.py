import matplotlib.pyplot as plt

import objects.arguments.args_Nature as args
from methods.figures.tick_dirs import tick_dirs
from objects.core_data.isotopes import iso_1208, iso_1209, iso_607
from objects.core_data.psu import psu_1208, psu_1209, psu_607


def atlantic_iso_bwt_figure(age_min: int = 2400, age_max: int = 2900):
    fig, axs = plt.subplots(
        nrows=2,
        figsize=(14, 8),
        sharex="all"
    )

    # d18O original data
    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args.args_1208)
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args.args_1209)
    axs[0].plot(iso_607.age_ka, iso_607.d18O, **args.args_607)

    # PSU BWT estimates
    axs[1].plot(psu_1208.age_ka, psu_1208.temp, **args.args_1208)
    axs[1].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, **args.fill_1208)
    axs[1].plot(psu_1209.age_ka, psu_1209.temp, **args.args_1209)
    axs[1].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, **args.fill_1209)
    axs[1].plot(psu_607.age_ka, psu_607.temp, **args.args_607)
    axs[1].fill_between(psu_607.age_ka, psu_607.temp_min1, psu_607.temp_plus1, **args.fill_607)

    # -- Define the axes --
    axs[0].set(ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[1].set(ylabel="BWT ({})".format(u'\N{DEGREE SIGN}C'))

    # Invert the axes with d18O
    axs[0].invert_yaxis()

    tick_dirs(axs, num_plots=2, max_age=age_max, min_age=age_min, legend=False)

    # Add a legend
    axs[0].legend(shadow=False, frameon=False)

    plt.show()
