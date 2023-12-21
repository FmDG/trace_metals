import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

import objects.args_brewer as args
from methods.figures.tick_dirs import tick_dirs
from objects.core_data.isotopes import iso_1208, iso_1209
from objects.core_data.lr04 import iso_probstack


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


def lr04_figure(save_fig: bool = False, age_min: int = 2400, age_max: int = 3600):
    fig, ax = plt.subplots(figsize=(11, 8))

    ax.plot(iso_1208.age_ka, iso_1208.d18O_unadj, marker="+")
    # -- Define the axes --
    ax.set(ylabel='LR04 {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    ax.invert_yaxis()

    ax.set(xlabel="Age (ka)", xlim=[age_min, age_max])
    ax.tick_params(axis='y', which="both", left=True, right=False, direction="out")
    ax.tick_params(axis='x', which="both", top=False, bottom=True)
    ax.tick_params(axis="both", which='major', length=6)
    ax.tick_params(axis="both", which='minor', length=3)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))

    if save_fig:
        plt.savefig("figures/LR04.png", format="png", dpi=150)
    else:
        plt.show()


def probstack_comparison(save_fig: bool = False, age_min: int = 2400, age_max: int = 3600):
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=(12, 8),
        sharex="all"
    )
    ax.plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args.args_1208)
    ax.plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args.args_1209)
    ax.plot(iso_probstack.age_ka, (iso_probstack.d18O_unadj - 0.64), marker="+", label="ProbStack (-0.64)",
            c='tab:blue')
    ax.fill_between(iso_probstack.age_ka, (iso_probstack.lower_95 - 0.64), (iso_probstack.upper_95 - 0.64),
                    fc='tab:blue', alpha=0.1)

    ax.set(xlabel="Age (ka)", ylabel="{} ({})".format(r'$\delta^{18}$O', u'\u2030'), xlim=[age_min, age_max],
           ylim=[2, 4])
    ax.invert_yaxis()
    ax.legend()

    if save_fig:
        plt.savefig("figures/ProbStack_figure_01.png", dpi=300)
    else:
        plt.show()


if __name__ == "__main__":
    probstack_comparison(save_fig=True)
