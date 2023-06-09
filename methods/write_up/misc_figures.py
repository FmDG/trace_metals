import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

from methods.figures.tick_dirs import tick_dirs
import objects.args_isfahan as args
from objects.core_data.psu import psu_1208, psu_1209, psu_607
from objects.core_data.isotopes import iso_607, iso_1208, iso_1209, iso_849


def pacific_plots(save_fig: bool = False):

    fig, ax = plt.subplots(1, figsize=(13, 7.5))

    ax.plot(iso_849[iso_849.age_ka.between(2400, 3400)].age_ka, iso_849[iso_849.age_ka.between(2400, 3400)].d18O_unadj, **args.args_849)
    ax.plot(iso_1208[iso_1208.age_ka.between(2400, 3400)].age_ka, iso_1208[iso_1208.age_ka.between(2400, 3400)].d18O_unadj, **args.args_1208)
    ax.plot(iso_1209[iso_1209.age_ka.between(2400, 3400)].age_ka, iso_1209[iso_1209.age_ka.between(2400, 3400)].d18O_unadj, **args.args_1209)

    ax.set(ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    ax.invert_yaxis()

    ax.set(xlabel="Age (ka)")
    ax.legend(shadow=False, frameon=False)
    ax.tick_params(axis='y', which="both", left=True, right=False, direction="out")
    ax.tick_params(axis='x', which="both", top=False, bottom=True)
    ax.tick_params(axis="both", which='major', length=6)
    ax.tick_params(axis="both", which='minor', length=3)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))

    fig.tight_layout()

    if save_fig:
        plt.savefig("figures/pacific_plots.png", format="png", dpi=150)
    else:
        plt.show()


if __name__ == "__main__":
    pacific_plots(save_fig=True)


