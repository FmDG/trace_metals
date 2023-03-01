import matplotlib.pyplot as plt
import pandas as pd

from methods.density.density_plots import density_plot
from methods.figures.tick_dirs import tick_dirs
from objects.args_lakota import args_1209, args_1208
from objects.colours import colours_extra
from objects.core_data.isotopes import iso_1208, iso_1209
# Load the data from the objects file
from objects.core_data.psu import psu_1208, psu_1209, psu_607

# Modern Measurements
mod_temp_1209, mod_temp_1208, mod_temp_607 = 1.7, 1.3, 2.2
mod_sal_1209, mod_sal_1208, mod_sal_607 = 34.4, 34.4, 34.9


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
    # ax.fill([34.62, 34.62, 34.73, 34.73, 34.62], [2.0, 0.1, 0.1, 2.0, 2.0], label='CDW', c=colours_extra[2], alpha=0.5)
    # Typical temperature values for the AAIW are 3-7°C, and a salinity of 34.2-34.4 psu upon initial formation
    ax.fill([34.2, 34.2, 34.4, 34.4, 34.2], [3.0, 7.0, 7.0, 3.0, 3.0], label='AAIW', c=colours_extra[3], alpha=0.5)

    return ax


def plot_palaeo_densities():
    # Generate the density plot
    ax = density_plot(min_sal=32.0)

    # Add the areas corresponding to modern water masses
    ax = add_modern_fill(ax)

    # -- Add mPWP densities --
    ax.scatter(*average_cdt(psu_1208, 3060, 3090), marker='s', label='1208 (mPWP)', color='r')
    ax.scatter(*average_cdt(psu_1209, 3060, 3090), marker='s', label='1209 (mPWP)', color='b')
    # ax.scatter(*average_cdt(psu_607, 3060, 3090), marker='+', label='607 (mPWP)')

    # -- Add Early Pleistocene IG densities --
    ax.scatter(*average_cdt(psu_1208, 2655, 2675), marker='o', label='1208 (IG)', color='r')
    ax.scatter(*average_cdt(psu_1209, 2655, 2675), marker='o', label='1209 (IG)', color='b')

    # -- Add Early Pleistocene G densities
    ax.scatter(*average_cdt(psu_1208, 2800, 2815), marker='^', label='1208 (G)', color='r')
    ax.scatter(*average_cdt(psu_1209, 2800, 2815), marker='^', label='1209 (G)', color='b')

    # -- Add modern densities
    ax.scatter(mod_sal_1208, mod_temp_1208, marker='D', label='1208 (Modern)', color='r')
    ax.scatter(mod_sal_1209, mod_temp_1209, marker='D', label='1209 (Modern)', color='b')
    # ax.scatter(mod_sal_607, mod_temp_607, marker='+', label='607 (Modern)')

    ax.legend(frameon=True, ncol=5)

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


def get_density_trajectories(dataframe: pd.DataFrame, ages: list[list[int, int]]):
    sals = []
    temps = []
    for age_set in ages:
        sal_01, temp_01 = average_cdt(dataframe, age_set[0], age_set[1])
        sals.append(sal_01)
        temps.append(temp_01)

    return sals, temps


def plot_density_trajectories():

    ages = [[3060, 3090], [2655, 2675], [2800, 2815]]

    # Compile trajectory for 1208
    traj_1208_sal, traj_1208_temp = get_density_trajectories(psu_1208, ages)
    traj_1208_sal.append(mod_sal_1208)
    traj_1208_temp.append(mod_temp_1208)

    # Compile trajectory for 1209
    traj_1209_sal, traj_1209_temp = get_density_trajectories(psu_1209, ages)
    traj_1209_sal.append(mod_sal_1209)
    traj_1209_temp.append(mod_temp_1209)

    # Compile trajcetory for 607
    traj_607_sal, traj_607_temp = get_density_trajectories(psu_607, ages)
    traj_607_sal.append(mod_sal_607)
    traj_607_temp.append(mod_temp_607)

    ax = density_plot(min_sal=32.0)

    ax.plot(traj_1208_sal, traj_1208_temp, label='1208')
    ax.plot(traj_1209_sal, traj_1209_temp, label='1209')
    ax.plot(traj_607_sal, traj_607_temp, label='607')

    ax.legend()

    plt.show()


if __name__ == "__main__":
    plot_palaeo_densities()
    # plot_isotopes(sections=[[3060, 3090], [2655, 2675], [2800, 2815]])
    # plot_density_trajectories()
