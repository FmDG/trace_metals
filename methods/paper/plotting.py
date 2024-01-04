import matplotlib.pyplot as plt


from objects.misc.sea_level import sea_level
from objects.arguments.args_Nature import args_1209, args_1208, fill_1208, fill_1209, args_607, fill_607
from objects.core_data.psu import psu_1208, psu_1209, psu_607
from objects.core_data.isotopes import iso_1208, iso_1209, iso_607
from methods.sea_levels.analysis import resampled_data, filtered_1208, filtered_1209


def isotope_plot(ax: plt.axis) -> plt.axis:
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
    ax.set(ylabel='Derived {} ({} VPDB)'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))
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


def difference_plot(ax: plt.axis, colour: str = None, centre_line: bool = False) -> plt.axis:
    if colour:
        args = {"marker": None, "color": colour}
    else:
        args = {"marker": None}
    if centre_line:
        ax.axhline(0, c="k", lw=0.7)
    ax.plot(resampled_data.age_ka, (resampled_data.d18O_unadj_mean_1208 - resampled_data.d18O_unadj_mean_1209), **args)
    ax.set(ylabel="{} ({})".format(r'$\Delta \delta^{18}$O', u"\u2030"))
    ax.invert_yaxis()
    return ax


def filtered_difference_plot(ax: plt.axis, colour: str = None) -> plt.axis:
    if colour:
        args = {"marker": None, "color": colour, "label": "5-ka filtered data"}
    else:
        args = {"marker": None, "label": "5-ka filtered data"}
    ax.axhline(0, c="k", lw=0.7)
    ax.plot(resampled_data.age_ka, (resampled_data.d18O_unadj_mean_1208 - resampled_data.d18O_unadj_mean_1209),
                marker="+", color="tab:grey", label="Difference" , alpha=0.7)
    ax.set(ylabel="{} ({})".format(r'$\Delta \delta^{18}$O', u"\u2030"))
    ax.plot(resampled_data.age_ka, (filtered_1208 - filtered_1209), **args)
    ax.fill_between(resampled_data.age_ka, (filtered_1208 - filtered_1209), alpha=0.1)
    ax.invert_yaxis()
    return ax