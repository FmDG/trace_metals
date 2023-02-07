import matplotlib.pyplot as plt
import pandas as pd

from methods.density.density_plots import density_plot
from methods.figures.tick_dirs import tick_dirs

# Load the data from the objects file
from objects.core_data.psu import psu_1208, psu_1209, psu_607
from objects.core_data.isotopes import iso_1208, iso_1209
from objects.args_lakota import args_1209, args_1208
from objects.colours import colours_extra

# Modern Measurements
temp_1209, temp_1208 = 1.7, 1.3
sal_1209, sal_1208 = 34.4, 34.4
sal_607 = 34.9
temp_607 = 2.2


def salinity_calculations(d18o: float) -> float:
    """
    Calculates salinity from seawater d18O values. From Lund et al., 2006, local_d18Osw == 0.50 * S - 17.0;
    :param d18o: the d18O of seawater value
    :return: a salinity value in psu
    """
    salinity = 2 * (d18o + 17.0)
    return salinity


def average_cdt(dataframe: pd.DataFrame, age_lower: int, age_upper: int) -> tuple[2, float]:
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


def add_modern_fill(ax: plt.axes, nadw: bool = True) -> plt.axes:
    if nadw:
        # NADW has a temperature of 2 - 4 °C with a salinity of 34.9-35.0 psu
        ax.fill([34.9, 34.9, 35.0, 35.0, 34.9], [2.0, 4.0, 4.0, 2.0, 2.0], label='NADW', c=colours_extra[0], alpha=0.5)
    # AABW has temperatures ranging from −0.8°C to 2°C (35°F), salinities from 34.6 to 34.7
    ax.fill([34.6, 34.6, 34.7, 34.7, 34.6], [2.0, -0.8, -0.8, 2.0, 2.0], label='AABW', c=colours_extra[1], alpha=0.5)
    # In the Pacific Ocean, it has a temperature of 0.1 to 2.0 °C. The salinity of CDW is 34.62 to 34.73
    ax.fill([34.62, 34.62, 34.73, 34.73, 34.62], [2.0, 0.1, 0.1, 2.0, 2.0], label='CDW', c=colours_extra[2], alpha=0.5)
    # Typical temperature values for the AAIW are 3-7°C, and a salinity of 34.2-34.4 psu upon initial formation
    ax.fill([34.2, 34.2, 34.4, 34.4, 34.2], [3.0, 7.0, 7.0, 3.0, 3.0], label='AAIW', c=colours_extra[3], alpha=0.5)

    return ax


def plot_palaeo_densities():
    ax = density_plot(min_sal=32.0)

    ax = add_modern_fill(ax)

    '''ax.scatter(*average_cdt(psu_1208, 3060, 3090), marker='+', label='1208 (mPWP)')
    ax.scatter(*average_cdt(psu_1209, 3060, 3090), marker='+', label='1209 (mPWP)')

    ax.scatter(*average_cdt(psu_1208, 2740, 2755), marker='+', label='1208 (IG)')
    ax.scatter(*average_cdt(psu_1209, 2740, 2755), marker='+', label='1209 (IG)')

    ax.scatter(*average_cdt(psu_1208, 2800, 2815), marker='+', label='1208 (G)')
    ax.scatter(*average_cdt(psu_1209, 2800, 2815), marker='+', label='1209 (G)')'''

    ax.scatter(sal_1208, temp_1208, marker='+', label='1208 (Modern)')
    ax.scatter(sal_1209, temp_1209, marker='+', label='1209 (Modern)')
    ax.scatter(sal_607, temp_607, marker='+', label='607 (Modern)')

    ax.legend(frameon=True, ncol=4)

    plt.show()


def plot_isotopes(sections: list[list[int, int]] = None):
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
    axs[0].set(ylabel="d18O")

    select_1208 = psu_1208[psu_1208.age_ka.between(min_age, max_age)]
    select_1209 = psu_1209[psu_1209.age_ka.between(min_age, max_age)]

    axs[1].plot(select_1208.age_ka, select_1208.temp, **args_1208)
    axs[1].plot(select_1209.age_ka, select_1209.temp, **args_1209)
    axs[1].set(ylabel="BWT")

    tick_dirs(
        axs=axs,
        num_plots=2,
        min_age=min_age,
        max_age=max_age,
        legend=True
    )

    for ax in axs:
        for section in sections:
            ax.axvspan(xmin=section[0], xmax=section[1], fc="b", ec=None, alpha=0.08)

    plt.show()


if __name__ == "__main__":
    plot_palaeo_densities()
    # plot_isotopes(sections=[[3060, 3090], [2740, 2755], [2800, 2815]])
