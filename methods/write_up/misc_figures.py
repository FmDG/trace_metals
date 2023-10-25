import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

import objects.args_isfahan as args
from objects.core_data.isotopes import iso_1208, iso_1209, iso_849
from objects.core_data.trace_elements import bca_1209


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


def single_iso_figure(save_fig: bool = False):
    fig, ax = plt.subplots(1, figsize=(12, 8))

    ax.plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args.args_1208)
    ax.plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args.args_1209)

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


def boron_plots(save_fig:bool = False):
    fig, ax1 = plt.subplots(figsize=(8, 8))

    ax1.set(xlabel="Age (ka)", ylabel="B/Ca ({})".format(r'$\mu$mol/mol'))

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:grey'
    ax2.set_ylabel('Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"), color=color)

    lg_bca = bca_1209[(bca_1209.age_ka < 2700) & (bca_1209.glacial == 1)]
    eg_bca = bca_1209[(bca_1209.age_ka > 2700) & (bca_1209.glacial == 1)]
    li_bca = bca_1209[(bca_1209.age_ka < 2700) & (bca_1209.glacial == 2)]
    ei_bca = bca_1209[(bca_1209.age_ka > 2700) & (bca_1209.glacial == 2)]

    ax1.scatter(lg_bca.age_ka, lg_bca.Bca, c="tab:blue", alpha=0.5, marker='+', label=None)
    ax1.scatter(eg_bca.age_ka, eg_bca.Bca, c="tab:blue", alpha=0.5, marker='+', label=None)
    ax1.scatter(li_bca.age_ka, li_bca.Bca, c="tab:orange", alpha=0.5, marker='+', label=None)
    ax1.scatter(ei_bca.age_ka, ei_bca.Bca, c="tab:orange", alpha=0.5, marker='+', label=None)

    ax1.errorbar(lg_bca.age_ka.mean(), lg_bca.Bca.mean(), yerr=lg_bca.Bca.std(), c="tab:blue", marker="s",
                 label="Glacial")
    ax1.errorbar(eg_bca.age_ka.mean(), eg_bca.Bca.mean(), yerr=eg_bca.Bca.std(), c="tab:blue", marker="s",
                 label=None)
    ax1.errorbar(li_bca.age_ka.mean(), li_bca.Bca.mean(), yerr=li_bca.Bca.std(), c="tab:orange", marker="s",
                 label="Interglacial")
    ax1.errorbar(ei_bca.age_ka.mean(), ei_bca.Bca.mean(), yerr=ei_bca.Bca.std(), c="tab:orange", marker="s",
                 label=None)

    ax1.set_xlabel("Age (ka)")
    ax1.set_ylabel("B/Ca ({})".format(r'$\mu$mol/mol'), color="tab:blue")
    ax1.tick_params(axis='y', labelcolor="tab:blue")

    ax1.legend()

    ax1.set_xlim(2400, 2900)
    ax1.set_ylim(150, 200)
    ax1.tick_params(axis='x', which="both", top=True, bottom=True)

    ax2.plot(iso_1209.age_ka, iso_1209.d18O_unadj, color=color, marker="+", alpha=0.3)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.invert_yaxis()

    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    ax1.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax1.yaxis.set_minor_locator(AutoMinorLocator(10))
    ax2.yaxis.set_minor_locator(AutoMinorLocator(10))

    # Save the figure or show it
    if save_fig:
        plt.savefig("figures/B_Ca.png", format='png', dpi=300)
    else:
        plt.show()


if __name__ == "__main__":
    # pacific_plots(save_fig=True)
    # single_iso_figure(save_fig=False)
    boron_plots(save_fig=False)


