import matplotlib.pyplot as plt

import objects.args_brewer as args
from objects.core_data.isotopes import iso_1208, iso_1209
from methods.figures.tick_dirs import tick_dirs


def whole_isotope_figure(age_min: int = 2200, age_max: int = 3700):
    fig, axs = plt.subplots(
        nrows=2,
        figsize=(14, 6),
        sharex="all"
    )

    # d18O original data
    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args.args_1208)
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args.args_1209)

    # d18O original data
    axs[1].plot(iso_1208.age_ka, iso_1208.d13C, **args.args_1208)
    axs[1].plot(iso_1209.age_ka, iso_1209.d13C, **args.args_1209)

    # -- Define the axes --
    axs[0].set(ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[1].set(ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{13}$C', u"\u2030"))

    # Invert the axes with d18O
    axs[0].invert_yaxis()

    # Add a legend
    axs[0].legend(shadow=False, frameon=False)

    tick_dirs(axs, num_plots=2, max_age=age_max, min_age=age_min)

    plt.show()


