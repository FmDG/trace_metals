import matplotlib.pyplot as plt


from objects.misc.sea_level import sea_level
from objects.arguments.args_Nature import args_1209, args_1208
from objects.core_data.isotopes import iso_1208, iso_1209
from methods.sea_levels.analysis import resampled_data, filtered_1208, filtered_1209, rolling_corr


def sea_level_plot(ax: plt.axis, colour: str = None,  age_min: int = 2350, age_max: int = 3400) -> plt.axis:
    if colour:
        args = {"marker": None, "color": colour}
    else:
        args = {"marker": None}

    ax.axhline(0, c='k', lw=0.7)
    clipped_sea_level = sea_level[sea_level.age_ka.between(age_min, age_max)]
    ax.plot(clipped_sea_level.age_ka, clipped_sea_level.SL_m, **args)
    ax.set(ylabel="Sea Level relative to present (m)")
    return ax


def isotope_plot(ax: plt.axis) -> plt.axis:
    ax.plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)
    ax.plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)
    ax.set(ylabel='Cibicidoides {} ({}, VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    ax.invert_yaxis()
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
    ax.legend(frameon=False)
    return ax


def sea_level_correlation_plot(ax: plt.axis, colour: str = None) -> plt.axis:
    if colour:
        args = {"marker": None, "color": colour}
    else:
        args = {"marker": None}
    ax.plot(rolling_corr.age_ka, (rolling_corr.r ** 2), **args)  # Plot the correlation
    ax.set(ylabel=r'Correlation, $R^{2}$')
    return ax


def sea_level_correlation_significance_plot(ax: plt.axis, colour: str = None) -> plt.axis:
    if colour:
        args = {"marker": None, "color": colour}
    else:
        args = {"marker": None}
    ax.plot(rolling_corr.age_ka, rolling_corr.p, **args)  # Plot the significance
    ax.axhline(0.05, c='r', ls="--", label="p = 0.05")
    ax.legend(frameon=False)
    ax.invert_yaxis()
    ax.set(ylabel="Significance, p-value", yscale="log")
    return ax
