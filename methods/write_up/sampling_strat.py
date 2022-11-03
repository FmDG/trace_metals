import matplotlib.pyplot as plt

from objects.core_data.isotopes import iso_1209, iso_1208
from objects.core_data.psu import psu_1208, psu_1209
from objects.figure_arguments import args_1209, args_1208
from methods.figures.tick_dirs import tick_dirs


def sampling_figures():
    min_age, max_age = 2400, 2800
    # Define figure
    fig, axs = plt.subplots(2, sharex='all')
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)
    # Name the Plot
    fig.suptitle("Comparison of Sites 1208 and 1209\n ({} - {} ka)".format(min_age, max_age))

    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)
    axs[0].set(ylabel="d18O")
    axs[0].legend()
    axs[0].invert_yaxis()

    axs[1].plot(psu_1208.age_ka, psu_1208.temp, **args_1208)
    axs[1].plot(psu_1209.age_ka, psu_1209.temp, **args_1209)
    axs[1].set(ylabel="BWT", xlabel='Age (ka)', xlim=[min_age, max_age])
    axs[1].legend()

    tick_dirs(axs=axs, num_plots=2, min_age=min_age, max_age=max_age)

    plt.show()


def sampling_resolution():
    num_plots = 2
    min_age, max_age = 2450, 2750

    isosample_1209 = iso_1209[iso_1209.age_ka.between(min_age, max_age)]
    isosample_1208 = iso_1208[iso_1208.age_ka.between(min_age, max_age)]

    tesample_1209 = psu_1209[psu_1209.age_ka.between(min_age, max_age)]
    tesample_1208 = psu_1208[psu_1208.age_ka.between(min_age, max_age)]

    # Define figure
    fig, axs = plt.subplots(num_plots, sharex='all')
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)
    # Name the Plot
    fig.suptitle("Comparison of Sites 1208 and 1209\n ({} - {} ka)".format(min_age, max_age))

    axs[0].plot(tesample_1208.age_ka, tesample_1208.temp, **args_1208)
    axs[0].plot(tesample_1209.age_ka, tesample_1209.temp, **args_1209)
    axs[0].set(ylabel="BWT")

    axs[1].plot(tesample_1208.age_ka, tesample_1208.age_ka.diff(), **args_1208)
    axs[1].plot(tesample_1209.age_ka, tesample_1209.age_ka.diff(), **args_1209)
    axs[1].set(ylabel="Age between samples (ka)".format(r'$^{-1}$'), xlabel='Age (ka)', xlim=[min_age, max_age])

    tick_dirs(axs=axs, num_plots=num_plots, min_age=min_age, max_age=max_age)

    plt.show()


if __name__ == "__main__":
    sampling_resolution()

