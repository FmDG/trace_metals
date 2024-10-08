import matplotlib.pyplot as plt


from objects.misc.sea_level import sea_level
from objects.misc.mis_boundaries import mis_boundaries
from objects.arguments.args_Nature import args_1209, args_1208, fill_1208, fill_1209, args_607, fill_607, colours, args_1207
from objects.core_data.psu import psu_1208, psu_1209, psu_607
from objects.core_data.isotopes import iso_1208, iso_1209, iso_607, iso_1207
from objects.core_data.lr04 import iso_probstack
from objects.core_data.misc_proxies import opal_882
from objects.core_data.alkenones import sst_846, sst_1208
from objects.core_data.planktics import planktics_1208, planktics_1209, planktics_1207
from analysis import resampled_data, resampled_SST, rolling_corr_spear, rolling_corr_pears, sst_gradients, glacial_means, interglacial_means
from methods.figures.arrows import draw_arrows


def isotope_plot(ax: plt.axis) -> plt.axis:
    ax.plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)
    ax.fill_between(iso_1208.age_ka, iso_1208.d18O_unadj - 0.05, iso_1208.d18O_unadj + 0.05, **fill_1208)
    ax.plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)
    ax.fill_between(iso_1209.age_ka, iso_1209.d18O_unadj - 0.05, iso_1209.d18O_unadj + 0.05, **fill_1209)
    ax.set(ylabel='Cibicidoides {} ({}, VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    ax.invert_yaxis()
    return ax


def isotope_plot_1207(ax: plt.axis) -> plt.axis:
    ax.plot(iso_1207.age_ka, iso_1207.d18O_unadj, **args_1207)
    ax.plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)
    ax.plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)
    ax.set(ylabel='Cibicidoides {} ({}, VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    ax.invert_yaxis()
    return ax


def psu_bwt_plot(ax: plt.axis) -> plt.axis:
    ax.plot(psu_1208.age_ka, psu_1208.temp, **args_1208)
    ax.fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, **fill_1208)
    ax.plot(psu_1209.age_ka, psu_1209.temp, **args_1209)
    ax.fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, **fill_1209)
    ax.set(ylabel='BWT Estimate ({})'.format(u'\N{DEGREE SIGN}C'))
    return ax


def psu_d18sw_plot(ax: plt.axis) -> plt.axis:
    ax.plot(psu_1208.age_ka, psu_1208.d18O_sw, **args_1208)
    ax.fill_between(psu_1208.age_ka, psu_1208.d18O_min1, psu_1208.d18O_plus1, **fill_1208)
    ax.plot(psu_1209.age_ka, psu_1209.d18O_sw, **args_1209)
    ax.fill_between(psu_1209.age_ka, psu_1209.d18O_min1, psu_1209.d18O_plus1, **fill_1209)
    ax.set(ylabel='Derived {} ({})'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))
    ax.invert_yaxis()
    return ax


def iso_607_plot(ax: plt.axis) -> plt.axis:
    ax.plot(iso_607.age_ka, iso_607.d18O, **args_607)
    return ax


def psu_607_plot(ax: plt.axis) -> plt.axis:
    ax.plot(psu_607.age_ka, psu_607.temp, **args_607)
    ax.fill_between(psu_607.age_ka, psu_607.temp_min1, psu_607.temp_plus1, **fill_607)
    return ax


def sea_level_plot(ax: plt.axis, colour: str = None,  age_min: int = 2400, age_max: int = 3600) -> plt.axis:
    if colour:
        args = {"marker": None, "color": colour}
    else:
        args = {"marker": None}

    ax.axhline(0, c='k', lw=0.7)
    clipped_sea_level = sea_level[sea_level.age_ka.between(age_min, age_max)]
    ax.plot(clipped_sea_level.age_ka, clipped_sea_level.SL_m, **args)
    ax.set(ylabel="Sea Level relative to present (m)")
    return ax


def difference_plot(ax: plt.axis, colour: str = None, centre_line: bool = False, left: int = 1) -> plt.axis:
    if colour:
        args = {"marker": None, "color": colour}
    else:
        args = {"marker": None}
    if centre_line:
        ax.axhline(0, c="k", lw=0.7)
    ax.plot(resampled_data.age_ka, resampled_data.difference_d18O, **args)
    ax.set(ylabel="{} ({})".format(r'$\Delta \delta^{18}$O', u"\u2030"))
    ax.invert_yaxis()
    ratio_arrows = (abs(resampled_data.difference_d18O.min())/(abs(resampled_data.difference_d18O.min()) + resampled_data.difference_d18O.max()) - 1)
    ax = draw_arrows(ax, ratio_arrows, left=left)
    return ax


def filtered_difference_plot(ax: plt.axis, colour: str = None, left: int = 1) -> plt.axis:
    if colour:
        args = {"marker": None, "color": colour, "label": "10-ka filtered data"}
    else:
        args = {"marker": None, "label": "5-ka filtered data"}
    filter_diff = resampled_data[resampled_data.age_ka.between(2400, 3400)]
    ax.plot(filter_diff.age_ka, filter_diff.difference_d18O, marker="+", color="tab:grey", label="Difference" , alpha=0.7)
    ax.set(ylabel="{} ({})".format(r'$\Delta \delta^{18}$O (1208 - 1209)', u"\u2030"))
    ax.plot(filter_diff.age_ka, filter_diff.filtered_difference, **args)
    ax.fill_between(filter_diff.age_ka, filter_diff.filtered_difference, alpha=0.1)
    ratio_arrows = (abs(filter_diff.filtered_difference.min())/(abs(filter_diff.filtered_difference.min()) + filter_diff.filtered_difference.max()) - 1)
    # ax = draw_arrows(ax, ratio_arrows, left=left)
    ax.invert_yaxis()
    return ax


def opal_plot(ax: plt.axis, colour: str = None) -> plt.axis:
    if colour:
        args = {"marker": None, "color": colour}
    else:
        args = {"marker": None}
    ax.plot(opal_882.age_ka, opal_882.opal_acc_rate, **args)
    ax.set(ylabel="Biogenic Opal MAR ({})".format(r'g cm$^{-2}$ kyr$^{-1}$'))
    return ax


def alkenone_plot(ax: plt.axis) -> plt.axis:
    ax.plot(sst_846.age_ka, sst_846.SST, color='gray', marker='o', label="ODP 846 (Equatorial Pacific)", ms=3, mfc="white")
    ax.plot(sst_1208.age_ka, sst_1208.temp, color='k', marker="D", label="ODP 1208 (NW Pacific)", ms=3, mfc="white")
    ax.legend(frameon=True)
    ax.set(ylabel="Alkenone SST ({})".format(u'\N{DEGREE SIGN}C'))
    return ax


def alkenone_gradient_plot(ax: plt.axis) -> plt.axis:
    args = {"marker": "+", "label": "846 - 1208", "color": "k", "lw": 1.2}
    ax.plot(resampled_SST.age_ka, resampled_SST.difference_SST, **args)
    ax.plot([2490, 2730], [sst_gradients["sst_grad_1"][0], sst_gradients["sst_grad_1"][0]], color='g')
    ax.plot([2730, 2900], [sst_gradients["sst_grad_2"][0], sst_gradients["sst_grad_2"][0]], color='g')
    ax.fill_between([2490, 2730], [sst_gradients["sst_grad_1"][0] + sst_gradients["sst_grad_1"][1], sst_gradients["sst_grad_1"][0] + sst_gradients["sst_grad_1"][1]], [sst_gradients["sst_grad_1"][0] - sst_gradients["sst_grad_1"][1], sst_gradients["sst_grad_1"][0] - sst_gradients["sst_grad_1"][1]],
                    color='g', alpha=0.1, ec=None)
    ax.fill_between([2730, 2900], [sst_gradients["sst_grad_2"][0] + sst_gradients["sst_grad_2"][1], sst_gradients["sst_grad_2"][0] + sst_gradients["sst_grad_2"][1]], [sst_gradients["sst_grad_2"][0] - sst_gradients["sst_grad_2"][1], sst_gradients["sst_grad_2"][0] - sst_gradients["sst_grad_2"][1]],
                    color='g', alpha=0.1, ec=None)
    ax.set(ylabel="Alkenone SST Gradient ({})".format(u'\N{DEGREE SIGN}C'))
    return ax


def alkenone_gradient_plot_glacial_interglacials(ax: plt.axis) -> plt.axis:
    args = {"marker": "+", "label": "846 - 1208", "color": "k", "lw": 1.2}
    ax.plot(resampled_SST.age_ka, resampled_SST.difference_SST, **args)
    ax.plot([2490, 2730], [sst_gradients["glacial_sst_grad_1"][0], sst_gradients["glacial_sst_grad_1"][0]], color='b')
    ax.plot([2730, 2900], [sst_gradients["glacial_sst_grad_2"][0], sst_gradients["glacial_sst_grad_2"][0]], color='b')
    ax.plot([2490, 2730], [sst_gradients["interglacial_sst_grad_1"][0], sst_gradients["interglacial_sst_grad_1"][0]], color='r')
    ax.plot([2730, 2900], [sst_gradients["interglacial_sst_grad_2"][0], sst_gradients["interglacial_sst_grad_2"][0]], color='r')
    ax.fill_between([2490, 2730], [sst_gradients["glacial_sst_grad_1"][0] + sst_gradients["glacial_sst_grad_1"][1], sst_gradients["glacial_sst_grad_1"][0] + sst_gradients["glacial_sst_grad_1"][1]], [sst_gradients["glacial_sst_grad_1"][0] - sst_gradients["glacial_sst_grad_1"][1], sst_gradients["glacial_sst_grad_1"][0] - sst_gradients["glacial_sst_grad_1"][1]],
                    color='b', alpha=0.1, ec=None)
    ax.fill_between([2730, 2900], [sst_gradients["glacial_sst_grad_2"][0] + sst_gradients["glacial_sst_grad_2"][1], sst_gradients["glacial_sst_grad_2"][0] + sst_gradients["glacial_sst_grad_2"][1]], [sst_gradients["glacial_sst_grad_2"][0] - sst_gradients["glacial_sst_grad_2"][1], sst_gradients["glacial_sst_grad_2"][0] - sst_gradients["glacial_sst_grad_2"][1]],
                    color='b', alpha=0.1, ec=None)
    ax.fill_between([2490, 2730], [sst_gradients["interglacial_sst_grad_1"][0] + sst_gradients["interglacial_sst_grad_1"][1], sst_gradients["interglacial_sst_grad_1"][0] + sst_gradients["interglacial_sst_grad_1"][1]], [sst_gradients["interglacial_sst_grad_1"][0] - sst_gradients["interglacial_sst_grad_1"][1], sst_gradients["interglacial_sst_grad_1"][0] - sst_gradients["interglacial_sst_grad_1"][1]],
                    color='r', alpha=0.1, ec=None)
    ax.fill_between([2730, 2900], [sst_gradients["interglacial_sst_grad_2"][0] + sst_gradients["interglacial_sst_grad_2"][1], sst_gradients["interglacial_sst_grad_2"][0] + sst_gradients["interglacial_sst_grad_2"][1]], [sst_gradients["interglacial_sst_grad_2"][0] - sst_gradients["interglacial_sst_grad_2"][1], sst_gradients["interglacial_sst_grad_2"][0] - sst_gradients["interglacial_sst_grad_2"][1]],
                    color='r', alpha=0.1, ec=None)
    ax.set(ylabel="Alkenone SST Gradient ({})".format(u'\N{DEGREE SIGN}C'))
    return ax

def spearman_correlation_plot_sea_level(ax: plt.axis) -> plt.axis:
    ax.plot(rolling_corr_spear.age_ka, (rolling_corr_spear.r ** 2), c="k")  # Plot the correlation
    ax.set(ylabel="Rolling Correlation ({})".format(r'r$^2$'))
    return ax


def spearman_significance_plot_sea_level(ax: plt.axis) -> plt.axis:
    ax.plot(rolling_corr_spear.age_ka, rolling_corr_spear.p, c="k")  # Plot the significance
    ax.axhline(0.05, c='r', ls="--", label="p = 0.05")
    ax.invert_yaxis()
    ax.set(ylabel="Significance (p-value)", yscale="log")
    return ax


def pearson_correlation_plot_sea_level(ax: plt.axis) -> plt.axis:
    ax.plot(rolling_corr_pears.age_ka, (rolling_corr_pears.r ** 2), c="k")  # Plot the correlation
    ax.set(ylabel="Rolling Correlation ({})".format(r'r$^2$'))
    return ax


def pearson_significance_plot_sea_level(ax: plt.axis) -> plt.axis:
    ax.plot(rolling_corr_pears.age_ka, rolling_corr_pears.p, c="k")  # Plot the significance
    ax.axhline(0.05, c='r', ls="--", label="p = 0.05")
    ax.invert_yaxis()
    ax.set(ylabel="Rolling Significance (p-value)", yscale="log")
    return ax


def difference_plot_glacials(ax: plt.axis, left: int = 1) -> plt.axis:
    filter_diff = resampled_data[resampled_data.age_ka.between(2400, 3400)]
    ax.plot(filter_diff.age_ka, filter_diff.difference_d18O, marker="+", color="tab:grey", label=None,
            alpha=0.7)
    ax.plot(glacial_means.age_ka, (glacial_means.value_1208 - glacial_means.value_1209), label="Glacial Mean", marker="o")
    ax.plot(interglacial_means.age_ka, (interglacial_means.value_1208 - interglacial_means.value_1209), label="Interglacial Mean", marker="^")
    ax.set(ylabel="{} ({})".format(r'$\Delta \delta^{18}$O', u"\u2030"))
    ax.invert_yaxis()
    ratio_arrows = (abs(filter_diff.filtered_difference.min())/(abs(filter_diff.filtered_difference.min()) + filter_diff.filtered_difference.max()) - 1)
    ax = draw_arrows(ax, ratio_arrows, left=left)
    ax.legend(frameon=False)
    ax.axhline(0, c="k")

    return ax


def average_difference_plot(ax: plt.axis, start=2700, end=3300) -> plt.axis:
    ax.plot(resampled_data.age_ka, resampled_data.difference_d18O, marker=None)
    avg_pre = resampled_data[resampled_data.age_ka.between(start, end)].difference_d18O.mean()
    std_pre = resampled_data[resampled_data.age_ka.between(start, end)].difference_d18O.std()
    ax.set(ylabel="{} ({})".format(r'$\Delta \delta^{18}$O', u"\u2030"))
    print(f'Difference = {avg_pre:.4f} ± {std_pre:.4f}')
    ax.plot([start, end], [avg_pre, avg_pre], label=f'Mean = {avg_pre:.2f}')
    ax.invert_yaxis()
    return ax


def planktic_difference_plot(ax: plt.axis) -> plt.axis:
    ax.plot(planktics_1207.age_ka, planktics_1207.d18O, label="1207", c=colours[2], marker="+")
    ax.plot(planktics_1208.age_ka, planktics_1208.d18O, label="1208", c=colours[0], marker="+")
    ax.plot(planktics_1209.age_ka, planktics_1209.d18O, label="1209", c=colours[1], marker="+")
    ax.set(ylabel="Planktic {} ({})".format(r'$\delta^{18}$O', u"\u2030"))
    ax.invert_yaxis()
    return ax


def probStack_plot(ax: plt.axis, colour=colours[2]) -> plt.axis:
    ax.plot(iso_probstack.age_ka, iso_probstack.d18O_unadj, c=colour)
    ax.invert_yaxis()
    ax.set(ylabel='Probabilistic {} stack ({}, VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    return ax
