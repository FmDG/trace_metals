from objects.arguments.args_Nature import args_1208, args_607, args_1209, args_1014, args_1018, args_849
from objects.core_data.psu import psu_1208, psu_1209, psu_1014, psu_1018, psu_607
from objects.core_data.trace_elements import te_849
from objects.core_data.isotopes import iso_1208, iso_1209, iso_607, iso_1014, iso_1018
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from methods.interpolations.binning_records import binning_multiple_series
from methods.interpolations.generate_interpolations import linear_relations
import objects.arguments.args_Nature as args
from methods.figures.highlight_mis import highlight_all_mis_greyscale
from methods.figures.tick_dirs import tick_dirs

def compare_psu(save_fig: bool = False) -> None:
    temp_comparator = binning_multiple_series(
        psu_1208, psu_1209,
        names=["1208", "1209"],
        start=2000,
        end=3600,
        fs=2,
        value="temp"
    )
    temp_comparator = temp_comparator.dropna()

    fig, ax = plt.subplots(
        figsize=(8, 8)
    )

    pre_iNHG = temp_comparator[temp_comparator.age_ka > 2700]
    post_iNHG = temp_comparator[temp_comparator.age_ka < 2700.1]

    ax.scatter(post_iNHG.temp_mean_1209, post_iNHG.temp_mean_1208, label="post 2.7 Ma", marker="o", s=20)
    ax.scatter(pre_iNHG.temp_mean_1209, pre_iNHG.temp_mean_1208, label="pre 2.7 Ma", marker="^", s=20)
    ax.set(xlabel=r'BWT 1209 ($\degree$C)', ylabel=r'BWT 1208 ($\degree$C)')
    ax.axis("equal")
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))

    ax = linear_relations(ax, temp_comparator, "temp_mean_1208", "temp_mean_1209", True)
    ax.legend()

    if save_fig:
        plt.savefig("figures/psu_plots/BWT_crossplot.png", dpi=300)
    else:
        plt.show()


def california_margin(save_fig: bool = False) -> None:

    fig, ax = plt.subplots(
        figsize=(15, 10)
    )

    highlight_all_mis_greyscale(ax)

    # PSU BWT estimates
    ax.plot(psu_1208.age_ka, psu_1208.temp, **args.args_1208)
    ax.fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, **args.fill_1208)
    ax.plot(psu_1209.age_ka, psu_1209.temp, **args.args_1209)
    ax.fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, **args.fill_1209)
    ax.plot(psu_1014.age_ka, psu_1014.temp, **args.args_1014)
    ax.fill_between(psu_1014.age_ka, psu_1014.temp_min1, psu_1014.temp_plus1, **args.fill_1014)
    ax.plot(psu_1018.age_ka, psu_1018.temp, **args.args_1018)
    ax.fill_between(psu_1018.age_ka, psu_1018.temp_min1, psu_1018.temp_plus1, **args.fill_1018)
    ax.plot(psu_607.age_ka, psu_607.temp, **args.args_607)
    ax.fill_between(psu_607.age_ka, psu_607.temp_min1, psu_607.temp_plus1, **args.fill_607)

    ax.set(xlabel='Age (ka)', xlim=[2400, 2800], ylabel='BWT Estimate ({})'.format(u'\N{DEGREE SIGN}C'))
    ax.legend(frameon=False)

    if save_fig:
        plt.savefig("figures/California_Margin/temp_zoom.png", dpi=300)


    fig, axs = plt.subplots(
        nrows = 2,
        sharex='all',
        figsize=(20, 10)
    )

    ## - Reduce the space between axes to 0 -
    fig.subplots_adjust(hspace=0)

    for ax in axs:
        highlight_all_mis_greyscale(ax)

    # PSU BWT estimates
    axs[0].plot(psu_1208.age_ka, psu_1208.temp, **args.args_1208)
    axs[0].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, **args.fill_1208)
    axs[0].plot(psu_1209.age_ka, psu_1209.temp, **args.args_1209)
    axs[0].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, **args.fill_1209)
    axs[0].plot(psu_1014.age_ka, psu_1014.temp, **args.args_1014)
    axs[0].fill_between(psu_1014.age_ka, psu_1014.temp_min1, psu_1014.temp_plus1, **args.fill_1014)
    axs[0].plot(psu_1018.age_ka, psu_1018.temp, **args.args_1018)
    axs[0].fill_between(psu_1018.age_ka, psu_1018.temp_min1, psu_1018.temp_plus1, **args.fill_1018)
    axs[0].plot(psu_607.age_ka, psu_607.temp, **args.args_607)
    axs[0].fill_between(psu_607.age_ka, psu_607.temp_min1, psu_607.temp_plus1, **args.fill_607)
    axs[0].set(ylabel='BWT Estimate ({})'.format(u'\N{DEGREE SIGN}C'))

    # PSU d18O_sw estimates
    axs[1].plot(psu_1208.age_ka, psu_1208.d18O_sw, **args.args_1208)
    axs[1].fill_between(psu_1208.age_ka, psu_1208.d18O_min1, psu_1208.d18O_plus1, **args.fill_1208)
    axs[1].plot(psu_1209.age_ka, psu_1209.d18O_sw, **args.args_1209)
    axs[1].fill_between(psu_1209.age_ka, psu_1209.d18O_min1, psu_1209.d18O_plus1, **args.fill_1209)
    axs[1].plot(psu_1014.age_ka, psu_1014.d18O_sw, **args.args_1014)
    axs[1].fill_between(psu_1014.age_ka, psu_1014.d18O_min1, psu_1014.d18O_plus1, **args.fill_1014)
    axs[1].plot(psu_1018.age_ka, psu_1018.d18O_sw, **args.args_1018)
    axs[1].fill_between(psu_1018.age_ka, psu_1018.d18O_min1, psu_1018.d18O_plus1, **args.fill_1018)
    axs[1].plot(psu_607.age_ka, psu_607.d18O_sw, **args.args_607)
    axs[1].fill_between(psu_607.age_ka, psu_607.d18O_min1, psu_607.d18O_plus1, **args.fill_607)
    axs[1].set(ylabel='Derived {} ({} VPDB)'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))

    tick_dirs(axs, 2, 2500, 2800, True)

    if save_fig:
        plt.savefig("figures/California_Margin/psu.png", dpi=300)
    else:
        plt.show()


def california_margin_full(save_fig: bool = False):
    fig, axs = plt.subplots(
        nrows=3,
        sharex='all',
        figsize=(20, 20)
    )

    ## - Reduce the space between axes to 0 -
    fig.subplots_adjust(hspace=0)

    for ax in axs:
        highlight_all_mis_greyscale(ax)

    # PSU BWT estimates
    axs[0].plot(psu_1208.age_ka, psu_1208.temp, **args.args_1208)
    axs[0].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, **args.fill_1208)
    axs[0].plot(psu_1209.age_ka, psu_1209.temp, **args.args_1209)
    axs[0].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, **args.fill_1209)
    axs[0].plot(psu_1014.age_ka, psu_1014.temp, **args.args_1014)
    axs[0].fill_between(psu_1014.age_ka, psu_1014.temp_min1, psu_1014.temp_plus1, **args.fill_1014)
    axs[0].plot(psu_1018.age_ka, psu_1018.temp, **args.args_1018)
    axs[0].fill_between(psu_1018.age_ka, psu_1018.temp_min1, psu_1018.temp_plus1, **args.fill_1018)
    axs[0].plot(psu_607.age_ka, psu_607.temp, **args.args_607)
    axs[0].fill_between(psu_607.age_ka, psu_607.temp_min1, psu_607.temp_plus1, **args.fill_607)
    axs[0].plot(te_849.age_ka, te_849.BWT, **args.args_849)
    axs[0].set(ylabel='BWT Estimate ({})'.format(u'\N{DEGREE SIGN}C'))

    # PSU d18O_sw estimates
    axs[1].plot(psu_1208.age_ka, psu_1208.d18O_sw, **args.args_1208)
    axs[1].fill_between(psu_1208.age_ka, psu_1208.d18O_min1, psu_1208.d18O_plus1, **args.fill_1208)
    axs[1].plot(psu_1209.age_ka, psu_1209.d18O_sw, **args.args_1209)
    axs[1].fill_between(psu_1209.age_ka, psu_1209.d18O_min1, psu_1209.d18O_plus1, **args.fill_1209)
    axs[1].plot(psu_1014.age_ka, psu_1014.d18O_sw, **args.args_1014)
    axs[1].fill_between(psu_1014.age_ka, psu_1014.d18O_min1, psu_1014.d18O_plus1, **args.fill_1014)
    axs[1].plot(psu_1018.age_ka, psu_1018.d18O_sw, **args.args_1018)
    axs[1].fill_between(psu_1018.age_ka, psu_1018.d18O_min1, psu_1018.d18O_plus1, **args.fill_1018)
    axs[1].plot(psu_607.age_ka, psu_607.d18O_sw, **args.args_607)
    axs[1].fill_between(psu_607.age_ka, psu_607.d18O_min1, psu_607.d18O_plus1, **args.fill_607)
    axs[1].invert_yaxis()
    axs[1].set(ylabel='Derived {} ({} VPDB)'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))

    axs[2].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)
    axs[2].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)
    axs[2].plot(iso_607.age_ka, iso_607.d18O, **args_607)
    axs[2].plot(iso_1014.age_ka, iso_1014.d18O, **args_1014)
    axs[2].plot(iso_1018.age_ka, iso_1018.d18O, **args_1018)
    axs[2].invert_yaxis()
    axs[2].set(ylabel='{} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))

    tick_dirs(axs, 3, 2500, 2800, True)

    if save_fig:
        plt.savefig("figures/California_Margin/iso_psu_zoom.png", dpi=300)
    else:
        plt.show()


if __name__ == "__main__":
    california_margin_full(False)