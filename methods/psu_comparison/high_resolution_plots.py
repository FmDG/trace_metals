from objects.core_data.psu import psu_1208, psu_mPWP_1209
from objects.core_data.isotopes import iso_1209, iso_1208
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from methods.figures.highlight_mis import highlight_all_mis_greyscale
from objects.arguments.args_Nature import args_1209, args_1208, fill_1209, fill_1208


def plot_high_res_psu(save_fig: bool = False) -> None:
    num_plots = 3
    fig, axs = plt.subplots(
        nrows=num_plots,
        figsize=(15, (num_plots*10)),
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
    axs[1].plot(psu_mPWP_1209.age_ka, psu_mPWP_1209.temp, **args_1209)
    axs[1].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, **fill_1208)
    axs[1].fill_between(psu_mPWP_1209.age_ka, psu_mPWP_1209.temp_min1, psu_mPWP_1209.temp_plus1, **fill_1209)
    axs[1].xaxis.set_minor_locator(AutoMinorLocator(10))
    axs[1].yaxis.set_minor_locator(AutoMinorLocator(5))
    axs[1].legend(frameon=True)
    axs[1].set(ylabel=r'BWT ($\degree$C)')
    axs[1].spines['right'].set_visible(False)
    axs[1].spines['top'].set_visible(False)
    axs[1].spines["bottom"].set_visible(False)

    axs[2].plot(psu_1208.age_ka, psu_1208.d18O_sw, **args_1208)
    axs[2].plot(psu_mPWP_1209.age_ka, psu_mPWP_1209.d18O_sw, **args_1209)
    axs[2].fill_between(psu_1208.age_ka, psu_1208.d18O_min1, psu_1208.d18O_plus1, **fill_1208)
    axs[2].fill_between(psu_mPWP_1209.age_ka, psu_mPWP_1209.d18O_min1, psu_mPWP_1209.d18O_plus1, **fill_1209)
    axs[2].xaxis.set_minor_locator(AutoMinorLocator(10))
    axs[2].yaxis.set_minor_locator(AutoMinorLocator(5))
    axs[2].legend(frameon=True)
    axs[2].set(xlabel="Age (ka)", ylabel='{} ({})'.format(r'$\delta^{18}$O$_{sw}$', u'\u2030'), xlim=[2420, 2860])
    axs[2].yaxis.set(ticks_position="right", label_position='right')
    axs[2].spines['left'].set_visible(False)
    axs[2].spines['top'].set_visible(False)

    if save_fig:
        plt.savefig("figures/high_resolution/HighResolution_BWT_d18O_SW.png", dpi=300)
    else:
        plt.show()


if __name__ == "__main__":
    plot_high_res_psu(save_fig=True)