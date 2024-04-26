import matplotlib.pyplot as plt

from objects.core_data.isotopes import iso_1208, iso_1209, uvi_1208, uvi_1209
from objects.arguments.args_Nature import colours
from methods.figures.tick_dirs import tick_dirs, tick_dirs_single
from methods.figures.highlight_mis import highlight_all_mis_greyscale
from methods.interpolations.binning_records import binning_multiple_series


def show_difference_cibs_uvis(save_fig: bool = False) -> None:
    uvi_1208_new = uvi_1208.rename(columns={"d18O": "d18O_unadj"})
    uvi_1209_new = uvi_1209.rename(columns={"d18O": "d18O_unadj"})
    answers_1208 = binning_multiple_series(iso_1208, uvi_1208_new, names=["cibs", "uvis"], fs=5)
    answers_1209 = binning_multiple_series(iso_1209, uvi_1209_new, names=["cibs", "uvis"], fs=5)

    fig, axs = plt.subplots(
        nrows=3,
        sharex="all",
        figsize=(20, 10)
    )

    for ax in axs:
        highlight_all_mis_greyscale(ax)

    fig.subplots_adjust(hspace=0)
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, label="Cibs")
    axs[1].plot(iso_1208.age_ka, iso_1208.d18O_unadj, label="Cibs")

    axs[0].plot(uvi_1209.age_ka, uvi_1209.d18O, label="Uvis")
    axs[1].plot(uvi_1208.age_ka, uvi_1208.d18O, label="Uvis")

    axs[2].scatter(answers_1208.age_ka, (answers_1208.d18O_unadj_mean_uvis - answers_1208.d18O_unadj_mean_cibs),
                label="1208", c=colours[0], marker="+")
    axs[2].scatter(answers_1209.age_ka, (answers_1209.d18O_unadj_mean_uvis - answers_1209.d18O_unadj_mean_cibs),
                label="1209", c=colours[1], marker="+")
    diff_1209 = (answers_1209.d18O_unadj_mean_uvis - answers_1209.d18O_unadj_mean_cibs).mean()
    diff_1208 = (answers_1208.d18O_unadj_mean_uvis - answers_1208.d18O_unadj_mean_cibs).mean()
    axs[2].axhline(0.64, ls=":")
    axs[2].axhline(0.47, ls="-.")
    axs[2].axhline(diff_1209, label="1209 difference = {:.3g}{}".format(diff_1209, u"\u2030"), ls="--", color=colours[1])
    axs[2].axhline(diff_1208, label="1208 difference = {:.3g}{}".format(diff_1208, u"\u2030"), ls="--", color=colours[0])

    print("{} {} mean difference = {:.3g} ka".format("Uvigerina", "1209", uvi_1209.age_ka.diff().mean()))
    print("{} {} mean difference = {:.3g} ka".format("Cibicidoides", "1209", iso_1209.age_ka.diff().mean()))
    print("{} {} mean difference = {:.3g} ka".format("Uvigerina", "1208", uvi_1208.age_ka.diff().mean()))
    print("{} {} mean difference = {:.3g} ka".format("Cibicidoides", "1209", iso_1208.age_ka.diff().mean()))

    axs[0].set(ylabel='1209 {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[1].set(ylabel='1208 {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[2].set(ylabel='Uvis - Cibs {} ({} VPDB)'.format(r'$\Delta \delta^{18}$O', u"\u2030"))

    for ax in axs:
        ax.invert_yaxis()

    tick_dirs(axs, 3, 2400, 3600, True)

    if save_fig:
        plt.savefig("figures/Figure_d18O_Cibs_Uvis.png", format="png", dpi=300)
    else:
        plt.show()


def adjusted_uvi_plot(save_fig: bool = False) -> None:

    fig, axs = plt.subplots(
        nrows=2,
        sharex="all",
        sharey="all",
        figsize=(15, 7)
    )

    for ax in axs:
        highlight_all_mis_greyscale(ax)

    fig.subplots_adjust(hspace=0)
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, label="Cibicidoides", marker="o", ms=2)
    axs[1].plot(iso_1208.age_ka, iso_1208.d18O_unadj, label="Cibicidoides", marker="o", ms=2)

    axs[0].plot(uvi_1209.age_ka, uvi_1209.d18O - 0.70, label="Uvigerina (-0.70{})".format(u"\u2030"), marker="s", ms=2)
    axs[1].plot(uvi_1208.age_ka, uvi_1208.d18O - 0.70, label="Uvigerina (-0.70{})".format(u"\u2030"), marker="s", ms=2)

    axs[0].set(ylabel='1209 {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[1].set(ylabel='1208 {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))

    axs[0].invert_yaxis()

    tick_dirs(axs, 2, 2350, 3650, True)

    if save_fig:
        plt.savefig("figures/Figure_d18O_Uvis_adj.png", format="png", dpi=300)
    else:
        plt.show()

if __name__ == "__main__":
    adjusted_uvi_plot(save_fig=True)