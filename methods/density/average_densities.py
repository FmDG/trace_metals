import matplotlib.pyplot as plt
import pandas as pd

# Load the density plot and tick direction methods
from methods.density.density_plots import density_plot
from methods.figures.tick_dirs import tick_dirs
# Load the data from the objects file
from objects.core_data.psu import psu_1208, psu_1209
from objects.args_isfahan import args_1209, args_1208, colour
from objects.colours import colours_extra
from objects.core_data.isotopes import iso_1208, iso_1209

# Modern Measurements
mod_temp_1209, mod_temp_1208, mod_temp_607 = 1.7, 1.3, 2.2
mod_sal_1209, mod_sal_1208, mod_sal_607 = 34.6, 34.6, 34.9

# Marine Isotope Stages
interglacials = [[2820, 2838, "G11"], [2777, 2798, "G9"], [2730, 2759, "G7"], [2690, 2704, "G5"], [2652, 2681, "G3"], [2614, 2638, "G1"], [2575, 2595, "103"], [2540, 2554, "101"], [2494, 2510, "99"]]
glacials = [[2798, 2820, "G10"], [2759, 2777, "G8"], [2704, 2730, "G6"], [2681, 2690, "G4"], [2638, 2652, "G2"], [2595, 2614, "104"], [2554, 2575, "102"], [2510, 2540, "100"]]
mpwp = [3055, 3087, "K1"]

glacial_interval = [2554, 2575, "102 (G)"]
interglacial_interval = [2575, 2595, "103 (IG)"]
pliocene_interval = [2820, 2838, "G11 (Plio)"]


def salinity_calculations(d18o: float) -> float:
    """
    Calculates salinity from seawater d18O values. From Lund et al., 2006, local_d18Osw == 0.50 * S - 17.0;
    :param d18o: the d18O of seawater value
    :return: a salinity value in psu
    """
    salinity = 2 * (d18o + 17.0)
    return salinity


def average_cdt(dataframe: pd.DataFrame, age_lower: int, age_upper: int) -> tuple[float, float]:
    """
    Return the temperature and salnity properties for a frame between the lower and upper age limits
    :param dataframe: dataset
    :param age_lower: lower limit of the age (in ka)
    :param age_upper: upper limit of the age (in ka)
    :return: the mean bottom water temperature and salinity for the site over the time interval.
    """
    selected = dataframe[dataframe.age_ka.between(age_lower, age_upper)]
    avg_bwt = selected.temp.mean()
    avg_d18_sw = selected.d18O_sw.mean()
    avg_sal = salinity_calculations(avg_d18_sw)
    return avg_sal, avg_bwt


def average_cdt_uncertainties(dataframe: pd.DataFrame, age_lower: int, age_upper: int) -> tuple[float, float, float, float]:
    """
    Return the temperature and salnity properties for a frame between the lower and upper age limits
    :param dataframe: dataset
    :param age_lower: lower limit of the age (in ka)
    :param age_upper: upper limit of the age (in ka)
    :return: the mean bottom water temperature and salinity for the site over the time interval.
    """
    selected = dataframe[dataframe.age_ka.between(age_lower, age_upper)]
    avg_bwt = selected.temp.mean()
    uncertainty_bwt = (selected.temp_plus1.mean() - selected.temp_min1.mean())/2
    avg_d18_sw = selected.d18O_sw.mean()
    avg_sal = salinity_calculations(avg_d18_sw)
    uncertainty_sal = selected.d18O_plus1.mean() - selected.d18O_min1.mean()
    return avg_sal, avg_bwt, uncertainty_sal, uncertainty_bwt


def add_modern_fill(ax: plt.axes, nadw: bool = True, aabw: bool = True, cdw: bool = True, aaiw: bool = True,
                    npdw: bool = True) -> plt.axes:
    if nadw:
        # NADW has a temperature of 2 - 4 °C with a salinity of 34.9-35.0 psu
        ax.fill([34.9, 34.9, 35.0, 35.0, 34.9], [2.0, 4.0, 4.0, 2.0, 2.0], label='NADW', c=colours_extra[0], alpha=0.5)
    if aabw:
        # AABW has temperatures ranging from −0.8°C to 2°C (35°F), salinities from 34.6 to 34.7
        ax.fill([34.6, 34.6, 34.7, 34.7, 34.6], [2.0, -0.8, -0.8, 2.0, 2.0], label='AABW', c=colours_extra[1], alpha=0.5)
    if cdw:
        # In the Pacific Ocean, it has a temperature of 0.1 to 2.0 °C. The salinity of CDW is 34.62 to 34.73
        ax.fill([34.62, 34.62, 34.73, 34.73, 34.62], [2.0, 0.1, 0.1, 2.0, 2.0], label='CDW', c=colours_extra[2], alpha=0.5)
    if aaiw:
        # Typical temperature values for the AAIW are 3-7°C, and a salinity of 34.2-34.4 psu upon initial formation
        ax.fill([34.2, 34.2, 34.4, 34.4, 34.2], [3.0, 7.0, 7.0, 3.0, 3.0], label='AAIW', c=colours_extra[3], alpha=0.5)
    if npdw:
        # Typical values from NPDW from Fuhr et al., 2021 of 2 - 1.5'C and 34.57 - 34.67 psu
        ax.fill([34.57, 34.57, 34.67, 34.67, 34.57], [2.0, 1.5, 1.5, 2.0, 2.0], label='NPDW', c=colours_extra[4], alpha=0.5)

    return ax


def plot_density_diff(ax: plt.axes, age_lower: int, age_higher: int, name: str = None, marker: str = None) -> plt.axes:
    ax.scatter(*average_cdt(psu_1208, age_lower, age_higher), marker=marker, label='1208 ({})'.format(name), color=colour[0])
    ax.scatter(*average_cdt(psu_1209, age_lower, age_higher), marker=marker, label='1209 ({})'.format(name), color=colour[1])
    return ax


def plot_density_diff_uncertainty(ax: plt.axes, age_lower: int, age_higher: int, name: str = None, marker: str = None) -> plt.axes:
    ans_1208 = average_cdt_uncertainties(psu_1208, age_lower, age_higher)
    ans_1209 = average_cdt_uncertainties(psu_1209, age_lower, age_higher)

    ax.errorbar(ans_1208[0], ans_1208[1], xerr=ans_1208[2], yerr=ans_1208[3], label="1208 ({})".format(name), color=colour[0], marker=marker, capsize=3.0)
    ax.errorbar(ans_1209[0], ans_1209[1], xerr=ans_1209[2], yerr=ans_1209[3], label="1209 ({})".format(name), color=colour[1], marker=marker, capsize=3.0)
    return ax


def plot_palaeo_densities(save_fig: bool = False):
    # Generate the density plot
    ax = density_plot(min_sal=32.0, min_temp=-3, max_temp=10)

    # Add the areas corresponding to modern water masses
    # ax = add_modern_fill(ax=ax, nadw=False, aabw=True, aaiw=True, cdw=True, npdw=True)

    # -- Add mPWP densities --
    ax = plot_density_diff(ax, age_lower=pliocene_interval[0], age_higher=pliocene_interval[1], name=pliocene_interval[2], marker="s")

    markers = ["o", "^", "*", "P", "X", "H", "p", "$o$"]
    slice_num = 2
    for x in range(slice_num):
        # -- Add Early Pleistocene IG densities (1/4)
        # ax = plot_density_diff(ax, age_lower=interglacials[4+x][0], age_higher=interglacials[4+x][1], name=interglacials[4+x][2], marker=markers[x])
        # -- Add Early Pleistocene G densities (1/4)
        # ax = plot_density_diff(ax, age_lower=glacials[4+x][0], age_higher=glacials[4+x][1], name=glacials[4+x][2], marker=markers[x + slice_num])
        pass

    # Plot up glacial and interglacial intervals
    ax = plot_density_diff(ax, age_lower=glacial_interval[0], age_higher=glacial_interval[1], name=glacial_interval[2], marker="o")
    ax = plot_density_diff(ax, age_lower=interglacial_interval[0], age_higher=interglacial_interval[1], name=interglacial_interval[2], marker="^")

    # -- Add modern densities
    ax.scatter(mod_sal_1208, mod_temp_1208, marker='D', label='1208 (Modern)', color=colour[0])
    ax.scatter(mod_sal_1209, mod_temp_1209, marker='D', label='1209 (Modern)', color=colour[1])
    # ax.scatter(mod_sal_607, mod_temp_607, marker='+', label='607 (Modern)')

    ax.legend(frameon=True, ncol=5)

    if save_fig:
        plt.savefig("figures/densities/past_densities_fills.png", format='png', dpi=150)
    else:
        plt.show()


def plot_palaeo_densities_uncertainties(save_fig: bool = False):
    # Generate the density plot
    ax = density_plot(min_sal=32.0, min_temp=-3, max_temp=10)

    # Add the areas corresponding to modern water masses
    # ax = add_modern_fill(ax=ax, nadw=False, aabw=True, aaiw=True, cdw=True, npdw=True)

    # -- Add mPWP densities --
    ax = plot_density_diff_uncertainty(ax, age_lower=pliocene_interval[0], age_higher=pliocene_interval[1], name=pliocene_interval[2], marker="s")

    # -- Add Early Pleistocene densities
    ax = plot_density_diff_uncertainty(ax, age_lower=interglacial_interval[0], age_higher=interglacial_interval[1], name=interglacial_interval[2], marker="^")
    ax = plot_density_diff_uncertainty(ax, age_lower=glacial_interval[0], age_higher=glacial_interval[1], name=glacial_interval[2], marker="o")

    # -- Add modern densities
    ax.scatter(mod_sal_1208, mod_temp_1208, marker='P', label='1208 (Modern)', color=colour[0])
    ax.scatter(mod_sal_1209, mod_temp_1209, marker='P', label='1209 (Modern)', color=colour[1])

    ax.legend(frameon=True, ncol=4)

    if save_fig:
        plt.savefig("figures/densities/densities_uncertain.png", format='png', dpi=150)
    else:
        plt.show()


def plot_isotopes(warm_sections: list[list[int, int]] = None, cold_sections: list[list[int, int]] = None, save_fig: bool = False):
    fig, axs = plt.subplots(
        nrows=2,
        sharex='all',
        figsize=(14, 7)
    )
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    min_age, max_age = 2200, 3400

    select_1208 = iso_1208[iso_1208.age_ka.between(min_age, max_age)]
    select_1209 = iso_1209[iso_1209.age_ka.between(min_age, max_age)]

    axs[0].plot(select_1208.age_ka, select_1208.d18O_unadj, **args_1208)
    axs[0].plot(select_1209.age_ka, select_1209.d18O_unadj, **args_1209)
    axs[0].invert_yaxis()

    select_1208 = psu_1208[psu_1208.age_ka.between(min_age, max_age)]
    select_1209 = psu_1209[psu_1209.age_ka.between(min_age, max_age)]

    axs[1].plot(select_1208.age_ka, select_1208.temp, **args_1208)
    axs[1].plot(select_1209.age_ka, select_1209.temp, **args_1209)

    axs[1].set(ylabel="BWT ({})".format(u'\N{DEGREE SIGN}C'))
    axs[0].set(ylabel="{} (VPDB {})".format(r'$\delta^{18}$O', u"\u2030"))


    tick_dirs(
        axs=axs,
        num_plots=2,
        min_age=min_age,
        max_age=max_age,
        legend=True
    )

    for ax in axs:
        for section in warm_sections:
            ax.axvspan(xmin=section[0], xmax=section[1], fc="r", ec=None, alpha=0.08)
        for section in cold_sections:
            ax.axvspan(xmin=section[0], xmax=section[1], fc="b", ec=None, alpha=0.08)

    for section in warm_sections + cold_sections:
        axs[1].annotate(section[2], (((section[0] + section[1])/2 - 6), -2), fontsize="xx-small")

    if save_fig:
        plt.savefig("figures/densities/timeslices.png", format='png', dpi=150)
    else:
        plt.show()


if __name__ == "__main__":
    # plot_palaeo_densities(save_fig=False)
    plot_palaeo_densities_uncertainties(save_fig=False)
    interglacials.append(mpwp)
    plot_isotopes(warm_sections=interglacials, cold_sections=glacials, save_fig=False)
