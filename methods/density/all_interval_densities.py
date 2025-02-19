import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from methods.density.calculations import bespoke_inverse_salinity, full_inverse_salinity
from methods.density.density_plots import density_plot
from objects.arguments.args_Nature import colours as colour
from average_densities import average_cdt
from objects.core_data.psu import psu_1208, psu_1209, psu_core_tops_1209, psu_core_tops_1208
from objects.misc.mis_boundaries import mis_boundaries
from objects.misc.sea_level import sea_level

# Modern Measurements
mod_temp_1209, mod_temp_1208 = 1.805, 1.525
mod_sal_1209, mod_sal_1208 = 34.580, 34.628

mod_d18O_sw_1209, mod_d18O_sw_1208 = -0.078, -0.075


def find_interval_average(lower_age: int, upper_age:int, dataframe: pd.DataFrame, interval: str = 'glacial') -> tuple[float, float, float, float]:
    if interval not in ['glacial', 'interglacial']:
        raise ValueError("Must input glacial or interglacial to this function")

    selected_intervals = mis_boundaries.loc[mis_boundaries.age_start.between(lower_age, upper_age)]
    selected_intervals = selected_intervals.loc[selected_intervals.age_end.between(lower_age - 10000, upper_age)]
    selected_intervals = selected_intervals.loc[selected_intervals.glacial == interval]
    if selected_intervals.empty:
        return 0, 0, 0, 0
    all_bwt = []
    all_d18Osw = []
    for _, row in selected_intervals.iterrows():
        start = row["age_start"]
        end = row["age_end"]
        selected = dataframe[dataframe.age_ka.between(start, end)]
        all_bwt.append(selected.temp.values)
        all_d18Osw.append(selected.d18O_sw.values)

    average_bwt = np.mean(np.concatenate(all_bwt))
    sigma_bwt = np.std(np.concatenate(all_bwt))
    average_d18Osw = np.mean(np.concatenate(all_d18Osw))
    sigma_d18Osw = np.std(np.concatenate(all_d18Osw))
    return average_bwt, average_d18Osw, sigma_bwt, sigma_d18Osw


def find_interval_correction(lower_age: int, upper_age:int, interval: str = 'glacial') -> tuple[float, float]:
    if interval not in ['glacial', 'interglacial']:
        raise ValueError("Must input glacial or interglacial to this function")

    selected_intervals = mis_boundaries.loc[mis_boundaries.age_start.between(lower_age, upper_age)]
    selected_intervals = selected_intervals.loc[selected_intervals.age_end.between(lower_age - 10000, upper_age)]
    selected_intervals = selected_intervals.loc[selected_intervals.glacial == interval]
    if selected_intervals.empty:
        return 0, 0

    all_rsl = []
    all_d18O_ivc = []
    for _, row in selected_intervals.iterrows():
        start = row["age_start"]
        end = row["age_end"]
        selected_rsl = sea_level[sea_level.age_ka.between(start, end)]
        all_rsl.append(selected_rsl.SL_m.values)
        all_d18O_ivc.append(selected_rsl.d18Ow_IV.values)

    average_rsl = np.mean(np.concatenate(all_rsl))
    average_d18O_ivc = np.mean(np.concatenate(all_d18O_ivc))
    return average_rsl, average_d18O_ivc


def find_total_average(lower_age: int, upper_age:int, dataframe: pd.DataFrame) -> tuple[float, float, float, float]:
    selected = dataframe[dataframe.age_ka.between(lower_age, upper_age)]
    avg_bwt = selected.temp.mean()
    std_bwt = selected.temp.std()
    avg_d18_sw = selected.d18O_sw.mean()
    std_d18O_sw = selected.d18O_sw.std()
    return avg_bwt, avg_d18_sw, std_bwt, std_d18O_sw


def find_total_correction(lower_age: int, upper_age: int) -> tuple[float, float]:
    selected_rsl = sea_level[sea_level.age_ka.between(lower_age, upper_age)]
    average_rsl = np.mean(selected_rsl.SL_m.values)
    average_ivc = np.mean(selected_rsl.d18Ow_IV.values)
    return average_rsl, average_ivc

def plot_densities(save_fig: bool = False):
    # Generate the density plot
    ax = density_plot(min_sal=31, max_sal=36, min_temp=-2, max_temp=6, lv=10)

    bwt_g_1208, d18Osw_g_1208, bwt_std_g_1208, d18Osw_std_g_1208 = find_interval_average(2300, 2700, psu_1208, 'glacial')
    bwt_g_1209, d18Osw_g_1209, bwt_std_g_1209, d18Osw_std_g_1209 = find_interval_average(2300, 2700, psu_1209, 'glacial')
    bwt_ig_1208, d18Osw_ig_1208, bwt_std_ig_1208, d18Osw_std_ig_1208 = find_interval_average(2300, 2700, psu_1208, 'interglacial')
    bwt_ig_1209, d18Osw_ig_1209, bwt_std_ig_1209, d18Osw_std_ig_1209 = find_interval_average(2300, 2700, psu_1209, 'interglacial')

    glacial_rsl, glacial_ivc = find_interval_correction(2400, 2700, 'glacial')
    interglacial_rsl, interglacial_ivc = find_interval_correction(2400, 2700, 'interglacial')
    pliocene_rsl, pliocene_ivc = find_total_correction(2700, 3000)

    sal_g_1208 = bespoke_inverse_salinity(d18Osw_g_1208, glacial_ivc, mod_d18O_sw_1208, mod_sal_1208, glacial_rsl)
    sal_g_1209 = bespoke_inverse_salinity(d18Osw_g_1209, glacial_ivc, mod_d18O_sw_1209, mod_sal_1209, glacial_rsl)
    sal_ig_1208 = bespoke_inverse_salinity(d18Osw_ig_1208, interglacial_ivc, mod_d18O_sw_1208, mod_sal_1208, interglacial_rsl)
    sal_ig_1209 = bespoke_inverse_salinity(d18Osw_ig_1209, interglacial_ivc, mod_d18O_sw_1209, mod_sal_1209, interglacial_rsl)

    sal_std_g_1208 = bespoke_inverse_salinity((d18Osw_g_1208 + d18Osw_std_g_1208), glacial_ivc, mod_d18O_sw_1208, mod_sal_1208, glacial_rsl) - sal_g_1208

    bwt_lp_1208, d18Osw_lp_1208, bwt_std_lp_1208, d18Osw_std_lp_1208 = find_total_average(2700, 3000, psu_1208)
    bwt_lp_1209, d18Osw_lp_1209, bwt_std_lp_1209, d18Osw_std_lp_1209 = find_total_average(2700, 3000, psu_1209)

    sal_lp_1208 = bespoke_inverse_salinity(d18Osw_lp_1208, pliocene_ivc, mod_d18O_sw_1208, mod_sal_1208, pliocene_rsl)
    sal_lp_1209 = bespoke_inverse_salinity(d18Osw_lp_1209, pliocene_ivc, mod_d18O_sw_1209, mod_sal_1209, pliocene_rsl)

    sal_ct_1208, bwt_ct_1208,  = average_cdt(psu_core_tops_1208, 0, 12, mod_sal_1208, mod_d18O_sw_1208)
    sal_ct_1209, bwt_ct_1209 = average_cdt(psu_core_tops_1209, 0, 12, mod_sal_1209, mod_d18O_sw_1209)

    # -- Add densities
    '''ax.plot([sal_g_1208, sal_g_1209], [bwt_g_1208, bwt_g_1209], ls=':', color='black')
    ax.plot([sal_ig_1208, sal_ig_1209], [bwt_ig_1208, bwt_ig_1209], ls=':', color='black')
    ax.plot([sal_lp_1208, sal_lp_1209], [bwt_lp_1208, bwt_lp_1209], ls=':', color='black')
    ax.plot([mod_sal_1208, mod_sal_1209], [mod_temp_1208, mod_temp_1209], ls=':', color='black')
    ax.plot([sal_ct_1208, sal_ct_1209], [bwt_ct_1208, bwt_ct_1209], ls=':', color='black')'''

    marker_size = 70

    ax.scatter(sal_g_1208, bwt_g_1208 ,marker='o', label=f'1208 (Pleistocene Glacials)', color=colour[0], s=marker_size, facecolor= "white", linewidths=2.0)
    ax.scatter(sal_ig_1208, bwt_ig_1208, marker='^', label=f'1208 (Pleistocene Interlacials)', color=colour[0], s=marker_size, facecolor= "white", linewidths=2.0)
    ax.scatter(sal_lp_1208, bwt_lp_1208, marker='*', label=f'1208 (Late Pliocene)', color=colour[0], s=marker_size*1.5, facecolor= "white", linewidths=1.7)
    ax.scatter(mod_sal_1208, mod_temp_1208, marker='D', label='1208 (Modern)', color=colour[0], s=marker_size)
    ax.scatter(sal_ct_1208, bwt_ct_1208, marker='s', color=colour[0], label='1208 (Holocene)', s=marker_size)

    ax.scatter(sal_g_1209, bwt_g_1209, marker='o', label=f'1209 (Pleistocene Glacials)', color=colour[1], s=marker_size, facecolor= "white", linewidths=2.0)
    ax.scatter(sal_ig_1209, bwt_ig_1209, marker='^', label=f'1209 (Pleistocene Interlacials)', color=colour[1], s=marker_size, facecolor= "white", linewidths=2.0)
    ax.scatter(sal_lp_1209, bwt_lp_1209, marker='*', label=f'1209 (Late Pliocene)', color=colour[1], s=marker_size*1.5, facecolor= "white", linewidths=1.7)
    ax.scatter(mod_sal_1209, mod_temp_1209, marker='D', label='1209 (Modern)', color=colour[1], s=marker_size)
    ax.scatter(sal_ct_1209, bwt_ct_1209, marker='s', color=colour[1], label='1209 (Holocene)', s=marker_size)

    sal_1209 = []
    for i in range(len(psu_1209.d18O_sw.values)):
        sal_1209.append(full_inverse_salinity(psu_1209.d18O_sw.values[i], psu_1209.age_ka.values[i], mod_d18O_sw_1209, mod_sal_1209))

    sal_1208 = []
    for i in range(len(psu_1208.d18O_sw.values)):
        sal_1208.append(full_inverse_salinity(psu_1208.d18O_sw.values[i], psu_1208.age_ka.values[i], mod_d18O_sw_1208, mod_sal_1208))

    # ax.scatter(sal_1208, psu_1208.temp.values, c=colour[0], marker='+', alpha=0.25)
    # ax.scatter(sal_1209, psu_1209.temp.values, c=colour[1], marker='+', alpha=0.25)

    ax.legend(frameon=True, ncol=2)

    if save_fig:
        plt.savefig("figures/paper/Figure_2_density_new.pdf", format='pdf', dpi=300)
    else:
        plt.show()



if __name__ == "__main__":
    plot_densities(False)