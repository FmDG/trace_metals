import matplotlib.pyplot as plt


from objects.misc.sea_level import sea_level
from objects.arguments.args_Nature import args_1209, args_1208
from objects.core_data.isotopes import iso_1208, iso_1209
from methods.sea_levels.analysis import resampled_data, filtered_1208, filtered_1209
from methods.figures.tick_dirs import tick_dirs


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
    return ax


def sea_level_isotope_comparison(save_fig: bool = False) -> None:
    n_plots = 3
    fig, axs = plt.subplots(
        nrows=n_plots,
        ncols=1,
        figsize=(12, 8),
        sharex="all"
    )
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    axs[0] = isotope_plot(axs[0])
    axs[1] = filtered_difference_plot(axs[1])
    axs[2] = sea_level_plot(axs[2])
    tick_dirs(axs, min_age=2400, max_age=3600, legend=True, num_plots=n_plots)
    # Save the figure or show it
    if save_fig:
        plt.savefig("figures/paper/sea_level.pdf", transparent=True)
    else:
        plt.show()



if __name__ == "__main__":
    sea_level_isotope_comparison(save_fig=False)