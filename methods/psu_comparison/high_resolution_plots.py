from objects.core_data.psu import psu_1208, psu_1209
from objects.core_data.isotopes import iso_1209, iso_1208
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from methods.figures.highlight_mis import highlight_all_mis_greyscale
from methods.paper.analysis import resampled_data
from objects.arguments.args_Nature import args_1209, args_1208, fill_1209, fill_1208
from methods.interpolations.generate_interpolations import generate_interpolation
from methods.interpolations.filter_data import filter_series
from objects.misc.sea_level import sea_level


def plot_high_res_bwt_d18o_sw(save_fig: bool = False) -> None:
    num_plots = 3
    fig, axs = plt.subplots(
        nrows=num_plots,
        figsize=(15, 25),
        sharex="all"
    )
    fig.subplots_adjust(hspace=0)

    highlight_all_mis_greyscale(axs[0])
    highlight_all_mis_greyscale(axs[1])
    highlight_all_mis_greyscale(axs[2], annotate=True)

    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)
    axs[0].xaxis.set_minor_locator(AutoMinorLocator(10))
    axs[0].yaxis.set_minor_locator(AutoMinorLocator(5))
    axs[0].legend(frameon=True)
    axs[0].set(ylabel='{} ({})'.format(r'$\delta^{18}$O', u'\u2030'))
    axs[0].yaxis.set(ticks_position="right", label_position='right')
    axs[0].spines['left'].set_visible(False)
    secax = axs[0].secondary_xaxis('top')
    secax.set(xlabel="Age (ka)")
    secax.xaxis.set_minor_locator(AutoMinorLocator(10))
    axs[0].spines["bottom"].set_visible(False)
    axs[0].invert_yaxis()

    axs[1].plot(psu_1208.age_ka, psu_1208.temp, **args_1208)
    axs[1].plot(psu_1209.age_ka, psu_1209.temp, **args_1209)
    axs[1].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, **fill_1208)
    axs[1].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, **fill_1209)
    axs[1].xaxis.set_minor_locator(AutoMinorLocator(10))
    axs[1].yaxis.set_minor_locator(AutoMinorLocator(5))
    axs[1].legend(frameon=True)
    axs[1].set(ylabel=r'BWT ($\degree$C)')
    axs[1].spines['right'].set_visible(False)
    axs[1].spines['top'].set_visible(False)
    axs[1].spines["bottom"].set_visible(False)

    axs[2].plot(psu_1208.age_ka, psu_1208.d18O_sw, **args_1208)
    axs[2].plot(psu_1209.age_ka, psu_1209.d18O_sw, **args_1209)
    axs[2].fill_between(psu_1208.age_ka, psu_1208.d18O_min1, psu_1208.d18O_plus1, **fill_1208)
    axs[2].fill_between(psu_1209.age_ka, psu_1209.d18O_min1, psu_1209.d18O_plus1, **fill_1209)
    axs[2].xaxis.set_minor_locator(AutoMinorLocator(10))
    axs[2].yaxis.set_minor_locator(AutoMinorLocator(5))
    axs[2].legend(frameon=True)
    axs[2].set(xlabel="Age (ka)", ylabel='{} ({})'.format(r'$\delta^{18}$O$_{sw}$', u'\u2030'), xlim=[2350, 2860])
    axs[2].yaxis.set(ticks_position="right", label_position='right')
    axs[2].spines['left'].set_visible(False)
    axs[2].spines['top'].set_visible(False)

    if save_fig:
        plt.savefig("figures/high_resolution/HighResolution_BWT_d18O_SW.png", dpi=300)
    else:
        plt.show()


def plot_high_res_bwt_d18o(save_fig: bool = False) -> None:
    num_plots = 2
    fig, axs = plt.subplots(
        nrows=num_plots,
        figsize=(15, (num_plots*10)),
        sharex="all"
    )
    fig.subplots_adjust(hspace=0)

    highlight_all_mis_greyscale(axs[0])
    highlight_all_mis_greyscale(axs[1], annotate=True)

    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)
    axs[0].xaxis.set_minor_locator(AutoMinorLocator(10))
    axs[0].yaxis.set_minor_locator(AutoMinorLocator(5))
    axs[0].legend(frameon=True)
    axs[0].set(ylabel='{} ({})'.format(r'$\delta^{18}$O', u'\u2030'))
    axs[0].yaxis.set(ticks_position="right", label_position='right')
    axs[0].spines['left'].set_visible(False)
    secax = axs[0].secondary_xaxis('top')
    secax.set(xlabel="Age (ka)")
    secax.xaxis.set_minor_locator(AutoMinorLocator(10))
    axs[0].spines["bottom"].set_visible(False)
    axs[0].invert_yaxis()

    axs[1].plot(psu_1208.age_ka, psu_1208.temp, **args_1208)
    axs[1].plot(psu_1209.age_ka, psu_1209.temp, **args_1209)
    axs[1].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, **fill_1208)
    axs[1].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, **fill_1209)
    axs[1].xaxis.set_minor_locator(AutoMinorLocator(10))
    axs[1].yaxis.set_minor_locator(AutoMinorLocator(5))
    axs[1].legend(frameon=True)
    axs[1].set(xlabel="Age (ka)", ylabel=r'BWT ($\degree$C)', xlim=[2470, 2860])
    axs[1].spines['right'].set_visible(False)
    axs[1].spines['top'].set_visible(False)

    if save_fig:
        plt.savefig("figures/high_resolution/HighResolution_BWT_d18O.png", dpi=300)
    else:
        plt.show()


def plot_high_res_bwt_diff(save_fig: bool = False) -> None:
    num_plots = 3
    fig, axs = plt.subplots(
        nrows=num_plots,
        figsize=(15, 20),
        sharex="all"
    )
    fig.subplots_adjust(hspace=0)

    highlight_all_mis_greyscale(axs[0])
    highlight_all_mis_greyscale(axs[1])
    highlight_all_mis_greyscale(axs[2], annotate=True)

    filter_diff = resampled_data[resampled_data.age_ka.between(2320, 3400)]
    axs[0].plot(filter_diff.age_ka, filter_diff.difference_d18O, marker="+", label="Difference")
    axs[0].fill_between(filter_diff.age_ka, filter_diff.difference_d18O, alpha=0.1)
    axs[0].set(ylabel="{} ({})".format(r'$\Delta \delta^{18}$O (1208 - 1209)', u"\u2030"))
    axs[0].invert_yaxis()
    axs[0].xaxis.set_minor_locator(AutoMinorLocator(10))
    axs[0].yaxis.set_minor_locator(AutoMinorLocator(5))
    axs[0].yaxis.set(ticks_position="right", label_position='right')
    axs[0].spines['left'].set_visible(False)
    secax = axs[0].secondary_xaxis('top')
    secax.set(xlabel="Age (ka)")
    secax.xaxis.set_minor_locator(AutoMinorLocator(10))
    axs[0].spines["bottom"].set_visible(False)

    axs[1].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)
    axs[1].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)
    axs[1].xaxis.set_minor_locator(AutoMinorLocator(10))
    axs[1].yaxis.set_minor_locator(AutoMinorLocator(5))
    axs[1].legend(frameon=True)
    axs[1].set(ylabel='{} ({})'.format(r'$\delta^{18}$O', u'\u2030'))
    axs[1].spines['right'].set_visible(False)
    axs[1].spines['top'].set_visible(False)
    axs[1].spines["bottom"].set_visible(False)
    axs[1].invert_yaxis()

    axs[2].plot(psu_1208.age_ka, psu_1208.temp, **args_1208)
    axs[2].plot(psu_1209.age_ka, psu_1209.temp, **args_1209)
    axs[2].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, **fill_1208)
    axs[2].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, **fill_1209)
    axs[2].xaxis.set_minor_locator(AutoMinorLocator(10))
    axs[2].yaxis.set_minor_locator(AutoMinorLocator(5))
    axs[2].legend(frameon=True)
    axs[2].set(xlabel="Age (ka)", ylabel=r'BWT ($\degree$C)', xlim=[2350, 2860])
    axs[2].yaxis.set(ticks_position="right", label_position='right')
    axs[2].spines['left'].set_visible(False)
    axs[2].spines['top'].set_visible(False)

    if save_fig:
        plt.savefig("figures/high_resolution/HighResolution_BWT_Dd18O.png", dpi=300)
    else:
        plt.show()

def plot_high_res_diff(save_fig: bool = False)-> None:
    start, end = 2400, 3400
    fs = 0.1
    abs_diff_1209, age_series = generate_interpolation(iso_1209, fs, start, end, False, "d18O_unadj")
    abs_diff_1208, _ = generate_interpolation(iso_1208, fs, start, end, False, "d18O_unadj")
    difference_series = abs_diff_1208 - abs_diff_1209
    filtered_series = filter_series(difference_series, 500)
    num_plots = 2
    fig, axs = plt.subplots(
        nrows=num_plots,
        figsize=(30, 20),
        sharex="all"
    )
    fig.subplots_adjust(hspace=0)

    highlight_all_mis_greyscale(axs[0])
    highlight_all_mis_greyscale(axs[1], annotate=True)

    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)
    axs[0].xaxis.set_minor_locator(AutoMinorLocator(10))
    axs[0].yaxis.set_minor_locator(AutoMinorLocator(5))
    axs[0].legend(frameon=True)
    axs[0].set(ylabel='{} ({})'.format(r'$\delta^{18}$O', u'\u2030'))
    axs[0].yaxis.set(ticks_position="right", label_position='right')
    axs[0].spines['left'].set_visible(False)
    secax = axs[0].secondary_xaxis('top')
    secax.set(xlabel="Age (ka)")
    secax.xaxis.set_minor_locator(AutoMinorLocator(10))
    axs[0].spines["bottom"].set_visible(False)
    axs[0].invert_yaxis()

    axs[1].fill_between(age_series, filtered_series, alpha=0.1)
    axs[1].plot(age_series, filtered_series, marker=None, label=f'Filtered Difference (5 ka)')
    axs[1].plot(age_series, difference_series, marker=None, label="Absolute Difference")
    axs[1].set(ylabel="{} ({})".format(r'$\Delta \delta^{18}$O (1208 - 1209)', u"\u2030"), xlabel="Age (ka)", xlim=[start, end])
    axs[1].invert_yaxis()
    axs[1].xaxis.set_minor_locator(AutoMinorLocator(10))
    axs[1].yaxis.set_minor_locator(AutoMinorLocator(5))
    axs[1].spines['right'].set_visible(False)
    axs[1].spines["top"].set_visible(False)
    axs[1].legend()


    if save_fig:
        plt.savefig("figures/high_resolution/HighResolution_Dd18O_Long.png", dpi=300)
    else:
        plt.show()


def plot_high_res_bwt_d18o_sl(save_fig: bool = False) -> None:
    num_plots = 3
    fig, axs = plt.subplots(
        nrows=num_plots,
        figsize=(15, 25),
        sharex="all"
    )
    fig.subplots_adjust(hspace=0)

    highlight_all_mis_greyscale(axs[0])
    highlight_all_mis_greyscale(axs[1])
    highlight_all_mis_greyscale(axs[2], annotate=True)

    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)
    axs[0].xaxis.set_minor_locator(AutoMinorLocator(10))
    axs[0].yaxis.set_minor_locator(AutoMinorLocator(5))
    axs[0].set(ylabel='{} ({})'.format(r'$\delta^{18}$O', u'\u2030'))
    axs[0].yaxis.set(ticks_position="right", label_position='right')
    axs[0].spines['left'].set_visible(False)
    secax = axs[0].secondary_xaxis('top')
    secax.set(xlabel="Age (ka)")
    secax.xaxis.set_minor_locator(AutoMinorLocator(10))
    axs[0].spines["bottom"].set_visible(False)
    axs[0].invert_yaxis()

    axs[1].plot(psu_1208.age_ka, psu_1208.temp, **args_1208)
    axs[1].plot(psu_1209.age_ka, psu_1209.temp, **args_1209)
    axs[1].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, **fill_1208)
    axs[1].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, **fill_1209)
    axs[1].xaxis.set_minor_locator(AutoMinorLocator(10))
    axs[1].yaxis.set_minor_locator(AutoMinorLocator(5))
    axs[1].set(ylabel=r'BWT ($\degree$C)')
    axs[1].spines['right'].set_visible(False)
    axs[1].spines['top'].set_visible(False)
    axs[1].spines["bottom"].set_visible(False)

    cropped_sl = sea_level[sea_level.age_ka.between(2340, 2870)]
    axs[2].plot(cropped_sl.age_ka, cropped_sl.SL_m, marker=None)
    axs[2].xaxis.set_minor_locator(AutoMinorLocator(10))
    axs[2].yaxis.set_minor_locator(AutoMinorLocator(5))
    axs[2].set(xlabel="Age (ka)", ylabel='Sea Level (m)', xlim=[2350, 2860])
    axs[2].yaxis.set(ticks_position="right", label_position='right')
    axs[2].spines['left'].set_visible(False)
    axs[2].spines['top'].set_visible(False)

    if save_fig:
        plt.savefig("figures/high_resolution/HighResolution_BWT_d18O_SL.png", dpi=300)
    else:
        plt.show()

if __name__ == "__main__":
    plot_high_res_bwt_d18o_sl(save_fig=True)