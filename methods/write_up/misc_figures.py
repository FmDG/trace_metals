import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

from methods.figures.tick_dirs import tick_dirs
import objects.args_isfahan as args
from objects.core_data.psu import psu_1208, psu_1209, psu_607
from objects.core_data.isotopes import iso_607, iso_1208, iso_1209, iso_849
from methods.interpolations.generate_interpolations import resampling


def pacific_plots(save_fig: bool = False):

    fig, ax = plt.subplots(1, figsize=(13, 7.5))

    ax.plot(iso_849[iso_849.age_ka.between(2400, 3400)].age_ka, iso_849[iso_849.age_ka.between(2400, 3400)].d18O_unadj, **args.args_849)
    ax.plot(iso_1208[iso_1208.age_ka.between(2400, 3400)].age_ka, iso_1208[iso_1208.age_ka.between(2400, 3400)].d18O_unadj, **args.args_1208)
    ax.plot(iso_1209[iso_1209.age_ka.between(2400, 3400)].age_ka, iso_1209[iso_1209.age_ka.between(2400, 3400)].d18O_unadj, **args.args_1209)

    ax.set(ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    ax.invert_yaxis()

    ax.set(xlabel="Age (ka)")
    ax.legend(shadow=False, frameon=False)
    ax.tick_params(axis='y', which="both", left=True, right=False, direction="out")
    ax.tick_params(axis='x', which="both", top=False, bottom=True)
    ax.tick_params(axis="both", which='major', length=6)
    ax.tick_params(axis="both", which='minor', length=3)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))

    fig.tight_layout()

    if save_fig:
        plt.savefig("figures/pacific_plots.png", format="png", dpi=150)
    else:
        plt.show()


def single_iso_figure(save_fig: bool = False):
    fig, ax = plt.subplots(1, figsize=(12, 8))

    ax.plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args.args_1208)
    ax.plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args.args_1209)

    ax.set(ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    ax.invert_yaxis()

    ax.set(xlabel="Age (ka)")
    ax.legend(shadow=False, frameon=False)
    ax.tick_params(axis='y', which="both", left=True, right=False, direction="out")
    ax.tick_params(axis='x', which="both", top=False, bottom=True)
    ax.tick_params(axis="both", which='major', length=6)
    ax.tick_params(axis="both", which='minor', length=3)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))

    fig.tight_layout()

    if save_fig:
        plt.savefig("figures/pacific_plots.png", format="png", dpi=150)
    else:
        plt.show()


def difference_BWT_figure(save_fig: bool = False, sampling_frequency: float = 5, dropna: bool = False):
    """
    This figure shows the interpolated difference in the BWT record of 1208 and 1209
    :param save_fig: determines whether this figure needs to be saved to Figure_S4.svg
    :param sampling_frequency: the frequency (in ka) that is resampled to
    :param dropna: whether to drop the NAN values in the resampling.
    :return:
    """
    # ------------------- PREPROCESSING -------------
    age_array, values_1208 = resampling(
        psu_1208,
        start=2400,
        end=2900,
        fs=sampling_frequency,
        value="temp"
    )
    _, values_1209 = resampling(
        psu_1209,
        start=2400,
        end=2900,
        fs=sampling_frequency,
        value="temp"
    )

    # Join the new data together in one DataFrame
    resampled_data = pd.DataFrame(list(zip(values_1208, values_1209)), columns=['temp_1208', 'temp_1209'])
    resampled_data['age_ka'] = age_array.tolist()

    resampled_data["difference"] = resampled_data.temp_1208 - resampled_data.temp_1209
    if dropna:
        resampled_data = resampled_data.dropna(subset='difference')

    # ------------- DEFINE FIGURE --------------------
    fig, axs = plt.subplots(
        nrows=2,
        ncols=1,
        sharex="all",
        figsize=(12, 7)
    )
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    # ------------- HIGHLIGHT MIS ---------------
    for ax in axs:
        # Highlight MIS 99 (2.494 - 2.51 Ma)
        ax.axvspan(
            xmin=2494,
            xmax=2510,
            ec=None,
            fc='red',
            alpha=0.1
        )
        # Highlight MIS G4 (2.681 - 2.69 Ma)
        ax.axvspan(
            xmin=2681,
            xmax=2690,
            ec=None,
            fc="blue",
            alpha=0.1
        )

    # ------------- PLOT DATA -------------------
    # Plot BWT data
    axs[0].plot(psu_1208.age_ka, psu_1208.temp, **args.args_1208)
    axs[0].plot(psu_1209.age_ka, psu_1209.temp, **args.args_1209)

    # Plot the interpolated differences
    axs[1].plot(resampled_data.age_ka, resampled_data.difference, **args.args_diff)
    axs[1].fill_between(resampled_data.age_ka, resampled_data.difference, **args.fill_diff)

    # ------------- FORMAT AXES ----------------
    # -- Label the axis --
    axs[0].set(ylabel='BWT Estimate ({})'.format(u'\N{DEGREE SIGN}C'))
    axs[1].set(ylabel='{} BWT ({})'.format(r'$\Delta$', u'\N{DEGREE SIGN}C'))

    tick_dirs(axs=axs, num_plots=2, min_age=2400, max_age=2900, legend=False)

    # Add a legend
    axs[0].legend(shadow=False, frameon=False)

    # Save the figure or show it
    if save_fig:
        plt.savefig("figures/paper/Figure_S5.svg", format='svg')
    else:
        plt.show()


if __name__ == "__main__":
    # pacific_plots(save_fig=True)
    single_iso_figure(save_fig=False)


