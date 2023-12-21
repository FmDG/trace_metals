import matplotlib.pyplot as plt
import pandas as pd

from methods.density.calculations import full_inverse_salinity
from methods.density.density_plots import density_plot
from objects.args_Nature import colours as colour
from objects.colours import colours_extra
from objects.core_data.psu import psu_1208, psu_1209, psu_core_tops_1209

# Modern Measurements
mod_temp_1209, mod_temp_1208 = 1.805, 1.525
mod_sal_1209, mod_sal_1208 = 34.61, 34.65

glacial_interval = [2798, 2820, "G10"]
interglacial_interval = [2730, 2759, "G7"]


def average_cdt(dataframe: pd.DataFrame, age_lower: int, age_upper: int) -> tuple[float, float]:
    """
    Return the temperature and salinity properties for a frame between the lower and upper age limits
    :param dataframe: dataset
    :param age_lower: lower limit of the age (in ka)
    :param age_upper: upper limit of the age (in ka)
    :return: the mean bottom water temperature and salinity for the site over the time interval.
    """
    selected = dataframe[dataframe.age_ka.between(age_lower, age_upper)]
    age_avg = (age_lower + age_upper) / 2
    avg_bwt = selected.temp.mean()
    avg_d18_sw = selected.d18O_sw.mean()
    avg_sal = full_inverse_salinity(avg_d18_sw, age_avg)
    return avg_sal, avg_bwt


def add_modern_fill(ax: plt.axes, nadw: bool = True, aabw: bool = True, cdw: bool = True, aaiw: bool = True,
                    npdw: bool = True) -> plt.axes:
    if nadw:
        # NADW has a temperature of 2 - 4 °C with a salinity of 34.9-35.0 psu
        ax.fill([34.9, 34.9, 35.0, 35.0, 34.9], [2.0, 4.0, 4.0, 2.0, 2.0], label='NADW', c=colours_extra[0], alpha=0.5)
    if aabw:
        # AABW has temperatures ranging from −0.8°C to 2°C (35°F), salinity from 34.6 to 34.7
        ax.fill([34.6, 34.6, 34.7, 34.7, 34.6], [2.0, -0.8, -0.8, 2.0, 2.0], label='AABW', c=colours_extra[1],
                alpha=0.5)
    if cdw:
        # In the Pacific Ocean, it has a temperature of 0.1 to 2.0 °C. The salinity of CDW is 34.62 to 34.73
        ax.fill([34.62, 34.62, 34.73, 34.73, 34.62], [2.0, 0.1, 0.1, 2.0, 2.0], label='CDW', c=colours_extra[2],
                alpha=0.5)
    if aaiw:
        # Typical temperature values for the AAIW are 3-7°C, and a salinity of 34.2-34.4 psu upon initial formation
        ax.fill([34.2, 34.2, 34.4, 34.4, 34.2], [3.0, 7.0, 7.0, 3.0, 3.0], label='AAIW', c=colours_extra[3], alpha=0.5)
    if npdw:
        # Typical values from NPDW from Fuhr et al., 2021 of 2 - 1.5'C and 34.57 - 34.67 psu
        ax.fill([34.57, 34.57, 34.67, 34.67, 34.57], [2.0, 1.5, 1.5, 2.0, 2.0], label='NPDW', c=colours_extra[4],
                alpha=0.5)

    return ax


def plot_density_diff(ax: plt.axes, age_lower: int, age_higher: int, name: str = None, marker: str = None) -> plt.axes:
    ax.scatter(*average_cdt(psu_1208, age_lower, age_higher), marker=marker, label='1208 ({})'.format(name),
               color=colour[0])
    ax.scatter(*average_cdt(psu_1209, age_lower, age_higher), marker=marker, label='1209 ({})'.format(name),
               color=colour[1])
    return ax


def plot_palaeo_densities(save_fig: bool = False):
    # Generate the density plot
    ax = density_plot(min_sal=32.0, max_sal=35.0, min_temp=-4, max_temp=10, lv=15)

    # Plot up glacial and interglacial intervals
    ax = plot_density_diff(ax, age_lower=glacial_interval[0], age_higher=glacial_interval[1], name=glacial_interval[2],
                           marker="o")
    ax = plot_density_diff(ax, age_lower=interglacial_interval[0], age_higher=interglacial_interval[1],
                           name=interglacial_interval[2], marker="^")

    # -- Add modern densities
    ax.scatter(mod_sal_1208, mod_temp_1208, marker='D', label='1208 (Modern)', color=colour[0])
    ax.scatter(mod_sal_1209, mod_temp_1209, marker='D', label='1209 (Modern)', color=colour[1])

    holocene_sal, holocene_temp = average_cdt(psu_core_tops_1209, 0, 12)
    lgm_sal, lgm_temp = average_cdt(psu_core_tops_1209, 12, 120)
    ax.scatter(holocene_sal, holocene_temp, marker='s', label='1209 (Holocene)', color=colour[2])
    ax.scatter(lgm_sal, lgm_temp, marker='s', label='1209 (LGM)', color=colour[2])

    ax.legend(frameon=True, ncol=2)

    if save_fig:
        plt.savefig("figures/densities/past_densities_fills.png", format='png', dpi=150)
    else:
        plt.show()


if __name__ == "__main__":
    plot_palaeo_densities(save_fig=False)
