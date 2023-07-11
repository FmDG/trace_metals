import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

import objects.args_brewer as args
from objects.core_data.isotopes import iso_1208, iso_1209
from objects.core_data.psu import psu_1208, psu_1209
from methods.figures.tick_dirs import tick_dirs


def iso_bwt_figure(age_min: int = 2200, age_max: int = 3700):
    fig, axs = plt.subplots(
        nrows=2,
        figsize=(14, 6),
        sharex="all"
    )

    # d18O original data
    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args.args_1208)
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args.args_1209)

    # PSU BWT estimates
    axs[1].plot(psu_1208.age_ka, psu_1208.temp, **args.args_1208)
    axs[1].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, **args.fill_1208)
    axs[1].plot(psu_1209.age_ka, psu_1209.temp, **args.args_1209)
    axs[1].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, **args.fill_1209)
    # axs[1].fill_between(psu_1209.age_ka, psu_1209.temp_min2, psu_1209.temp_plus2, alpha=0.05)

    # -- Define the axes --
    axs[0].set(ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[1].set(ylabel="BWT ({})".format(u'\N{DEGREE SIGN}C'), ylim=(-2.0, 3.5))

    # Invert the axes with d18O
    axs[0].invert_yaxis()

    tick_dirs(axs, num_plots=2, max_age=age_max, min_age=age_min, legend=False)

    # Add a legend
    axs[0].legend(shadow=False, frameon=False)

    plt.show()


