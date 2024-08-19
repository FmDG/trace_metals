from objects.core_data.isotopes import iso_1209, iso_1208
from objects.core_data.psu import psu_1209, psu_1208
from objects.arguments.args_Nature import args_1209, args_1208, args_diff

from methods.interpolations.binning_records import binning_multiple_series
from methods.figures.highlight_mis import highlight_all_mis_greyscale
from methods.figures.tick_dirs import tick_dirs

import matplotlib.pyplot as plt
import pandas as pd

resampling_freq = 2  # Resampling frequency in ka
age_min, age_max = 2200, 3600  # Minimum and maximum ages in ka


def generate_differences():
    ## ------------- GENERATE DIFFERENCES  -------------
    resampled_data_iso = binning_multiple_series(
        iso_1208, iso_1209,
        names=["1208", "1209"],
        fs=resampling_freq,
        start=age_min,
        end=age_max
    ).dropna(how='all')
    # Filter the difference in d18O
    resampled_data_iso["difference_d18O"] = resampled_data_iso.d18O_unadj_mean_1208 - resampled_data_iso.d18O_unadj_mean_1209

    # Repeat the process for BWT
    resampled_data_temp = binning_multiple_series(
        psu_1208, psu_1209,
        names=["1208", "1209"],
        fs=resampling_freq,
        start=age_min,
        end=age_max,
        value='temp'
    ).dropna(how='all')
    # Filter the difference in d18O
    resampled_data_temp["difference_temp"] = resampled_data_temp.temp_mean_1208 - resampled_data_temp.temp_mean_1209

    # Repeat the process for d18O_sw
    resampled_data_seawater = binning_multiple_series(
        psu_1208, psu_1209,
        names=["1208", "1209"],
        fs=resampling_freq,
        start=age_min,
        end=age_max,
        value='d18O_sw'
    ).dropna(how='all')
    # Filter the difference in d18O
    resampled_data_seawater["difference_d18O_sw"] = resampled_data_seawater.d18O_sw_mean_1208 - resampled_data_seawater.d18O_sw_mean_1209

    # Merge all databases together
    resampled_data = pd.merge(resampled_data_iso, resampled_data_temp, how='outer', on='age_ka')
    return pd.merge(resampled_data, resampled_data_seawater, how='outer', on='age_ka')


def present_differences():
    difference_data = generate_differences()
    fig, axs = plt.subplots(
        nrows=2,
        figsize=[10, 8],
        sharex='all'
    )
    for ax in axs:
        highlight_all_mis_greyscale(ax)
        ax.set(ylabel='Cibicidoides {} ({}, VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
        ax.invert_yaxis()

    axs[0].plot(difference_data.dropna(subset='difference_d18O').age_ka,
                difference_data.dropna(subset='difference_d18O').difference_d18O, **args_diff)
    axs[1].plot(difference_data.dropna(subset='d18O_unadj_mean_1208').age_ka,
                difference_data.dropna(subset='d18O_unadj_mean_1208').d18O_unadj_mean_1208, **args_1208)
    axs[1].plot(difference_data.dropna(subset='d18O_unadj_mean_1209').age_ka,
                difference_data.dropna(subset='d18O_unadj_mean_1209').d18O_unadj_mean_1209, **args_1209)
    tick_dirs(axs, 2, 2350, 3550, True)

    fig, axs = plt.subplots(
        nrows=2,
        figsize=[10, 8],
        sharex='all'
    )
    for ax in axs:
        highlight_all_mis_greyscale(ax)
        ax.set(ylabel='BWT Estimate ({})'.format(u'\N{DEGREE SIGN}C'))

    axs[0].plot(difference_data.dropna(subset='difference_temp').age_ka,
                difference_data.dropna(subset='difference_temp').difference_temp, **args_diff)
    axs[1].plot(difference_data.dropna(subset='temp_mean_1208').age_ka,
                difference_data.dropna(subset='temp_mean_1208').temp_mean_1208, **args_1208)
    axs[1].plot(difference_data.dropna(subset='temp_mean_1209').age_ka,
                difference_data.dropna(subset='temp_mean_1209').temp_mean_1209, **args_1209)
    tick_dirs(axs, 2, 2400, 2900, True)

    fig, axs = plt.subplots(
        nrows=2,
        figsize=[10, 8],
        sharex='all'
    )
    for ax in axs:
        highlight_all_mis_greyscale(ax)
        ax.set(ylabel='Derived {} ({} VPDB)'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))
        ax.invert_yaxis()

    axs[0].plot(difference_data.dropna(subset='difference_d18O_sw').age_ka,
                difference_data.dropna(subset='difference_d18O_sw').difference_d18O_sw, **args_diff)
    axs[1].plot(difference_data.dropna(subset='d18O_sw_mean_1208').age_ka,
                difference_data.dropna(subset='d18O_sw_mean_1208').d18O_sw_mean_1208, **args_1208)
    axs[1].plot(difference_data.dropna(subset='d18O_sw_mean_1209').age_ka,
                difference_data.dropna(subset='d18O_sw_mean_1209').d18O_sw_mean_1209, **args_1209)

    tick_dirs(axs, 2, 2400, 2900, True)

    plt.show()

if __name__ == '__main__':
    present_differences()