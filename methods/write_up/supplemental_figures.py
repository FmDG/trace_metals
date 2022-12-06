import matplotlib.pyplot as plt

from objects.core_data.isotopes import iso_1209, iso_1208
from objects.core_data.trace_elements import te_1208, te_1209
import objects.args_isfahan as args
from objects.met_brewer import Isfahan2
from methods.figures.tick_dirs import tick_dirs

colours_04 = Isfahan2


def processing_thresholds(data_set, threshold):
    excess_mn = data_set.MnCa > threshold
    excess_al = data_set.AlCa > threshold
    excess_fe = data_set.FeCa > threshold
    total_excess = excess_mn + excess_fe + excess_al
    return total_excess


def figure_s1(save_fig: bool = False, figure_ratio: float = 1.0) -> int:
    """
    Supplemental figure showing the raw data of the d18O and Mg/Ca values.
    :parameter save_fig: bool - save the figure to the folder paper as Figure_S1
    :parameter figure_ratio: float - the ratio of height to width in the final figure
    :return: returns 1 if all is well
    """

    # Error handling
    if not isinstance(save_fig, bool):
        raise ValueError("save_fig must be of type bool")

    # d18O and TE for 1209
    num_plots = 4
    min_age, max_age = 2400, 3500

    # --------------------- PLOT THE DATA ------------------------

    fig, axs = plt.subplots(
        nrows=num_plots,
        ncols=1,
        sharex="all",
        figsize=(8, 8*figure_ratio)
    )

    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)
    # Name the Plot
    fig.suptitle("Raw Data - ODP 1209\n ({} - {} ka)".format(min_age, max_age))

    # -- Plot the 1209 data --
    # Isotopes
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args.args_1209)
    # Trace Elements
    axs[2].plot(te_1209.age_ka, te_1209.MgCa, **args.args_1209)

    # -- Plot the 1208 data --
    # Isotopes
    axs[1].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args.args_1208)
    # Trace Elements
    axs[3].plot(te_1208.age_ka, te_1208.MgCa, **args.args_1208)

    # -- Define the axes --
    axs[0].set(ylabel="{} (VPDB {})".format(r'$\delta^{18}$O', u"\u2030"))
    axs[1].set(ylabel="{} (VPDB {})".format(r'$\delta^{18}$O', u"\u2030"))
    axs[2].set(ylabel="Mg/Ca (mmol/mol)")
    axs[3].set(ylabel="Mg/Ca (mmol/mol)")

    # Invert the axes with d18O
    axs[0].invert_yaxis()
    axs[1].invert_yaxis()

    tick_dirs(axs, num_plots, min_age, max_age)

    # Save the figure if required
    if save_fig:
        plt.savefig("figures/paper/Figure_S1.png", format="png", dpi=300)
    else:
        plt.show()

    return 1


def figure_s2(save_fig: bool = False, figure_ratio: float = 1.0):
    """
    Supplemental figure 2.     - [ ] A set of plots showing Mg/Ca and Mn/Ca against depth to show that there is no
    contamination of specific values - repeat this for a bunch of contaminant indicators.
    :param save_fig: boolean to describe if we want to save this figure as Figure_S2.png
    :param figure_ratio: the ratio of x to y in the final displayed/saved figure
    :return: no return
    """
    # Mg/Ca against B/Ca, Mn/Ca, Fe/Ca, and Al/Ca
    num_plots = 4

    te_1209['excess'] = processing_thresholds(te_1209, 120)

    fig, axs = plt.subplots(
        nrows=num_plots,
        ncols=1,
        sharex="all",
        figsize=(10, 10 * figure_ratio)
    )

    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)
    # Name the Plot
    fig.suptitle("Raw Data - ODP 1209")

    # Mg/Ca
    axs[0].scatter(te_1209.mcd, te_1209.MgCa, label='Included', color=colours_04[0], marker='+')
    axs[0].scatter(te_1209[te_1209['excess']].mcd, te_1209[te_1209['excess']].MgCa, label='Excluded', color='r', marker='+')
    axs[0].legend(shadow=False, frameon=True)

    # Al/Ca
    axs[1].scatter(te_1209.mcd, te_1209.AlCa, label='Al/Ca', color=colours_04[1], marker='+')
    axs[1].scatter(te_1209[te_1209.AlCa > 120].mcd, te_1209[te_1209.AlCa > 120].AlCa, color='r', marker='+')
    axs[1].axhline(120, ls='--', lw='0.8', color='r', label='Threshold')

    # Mn/Ca
    axs[2].scatter(te_1209.mcd, te_1209.MnCa, label='Mn/Ca', color=colours_04[2], marker='+')
    axs[2].scatter(te_1209[te_1209.MnCa > 120].mcd, te_1209[te_1209.MnCa > 120].MnCa, color='r', marker='+')
    axs[2].axhline(120, ls='--', lw='0.8', color='r', label='Threshold')

    # Fe/Ca
    axs[3].scatter(te_1209.mcd, te_1209.FeCa, label='Fe/Ca', color=colours_04[3], marker='+')
    axs[3].scatter(te_1209[te_1209.FeCa > 120].mcd, te_1209[te_1209.FeCa > 120].FeCa, color='r', marker='+')
    axs[3].axhline(120, ls='--', lw='0.8', color='r', label='Threshold')

    # Define the axes
    axs[0].set(ylabel='Mg/Ca ({})'.format('mmol/mol'))
    axs[1].set(ylabel='Al/Ca ({})'.format(r'$\mu$mol/mol'), ylim=[0, 250])
    axs[2].set(ylabel='Mn/Ca ({})'.format(r'$\mu$mol/mol'), ylim=[0, 250])
    axs[3].set(ylabel='Fe/Ca ({})'.format(r'$\mu$mol/mol'), ylim=[0, 250])

    for q in range(num_plots):
        # Remove the left/right axes to make the plot look cleaner
        if q % 2 == 1:
            axs[q].yaxis.set(ticks_position="right", label_position='right')

    axs[(num_plots - 1)].set(xlabel="MCD")

    # Save the figure if required
    if save_fig:
        plt.savefig("figures/paper/Figure_S2.png", format="png", dpi=300)
    else:
        plt.show()


def figure_s3(save_fig: bool = False, figure_ratio: float = 1.0):
    """
    Generates figure S1. A set of cross-plots showing Mg/Ca against Mn/Ca, Fe/Ca etc... to show that there is no
    correlation between contaminants and measured values.
    :param save_fig: boolean to describe if we want to save this figure as Figure_S3.png
    :param figure_ratio: the ratio of x to y in the final displayed/saved figure
    :return: no return
    """
    # Mg/Ca against B/Ca, Mn/Ca, Fe/Ca, and Al/Ca

    fig, axs = plt.subplots(
        nrows=1,
        ncols=3,
        sharex="all",
        sharey='all',
        figsize=(15, 5)
    )

    # Reduce space between axes
    fig.subplots_adjust(hspace=0.1, wspace=0.1)
    # Name the Plot
    fig.suptitle("Cross Plots - ODP 1209")

    # Mn/Ca
    axs[0].scatter(te_1209.MnCa, te_1209.MgCa, marker='+', label='Mn/Ca', color=colours_04[0])
    axs[0].scatter(te_1209[te_1209.MnCa > 120].MnCa, te_1209[te_1209.MnCa > 120].MgCa, marker='+', color='r')
    axs[0].set(title='Mn/Ca', xlabel='Mn/Ca ({})'.format(r'$\mu$mol/mol'))

    # Fe/Ca
    axs[1].scatter(te_1209.FeCa, te_1209.MgCa, marker='+', label='Fe/Ca', color=colours_04[1])
    axs[1].scatter(te_1209[te_1209.FeCa > 120].FeCa, te_1209[te_1209.FeCa > 120].MgCa, marker='+', color='r')
    axs[1].set(title='Fe/Ca', xlabel='Fe/Ca ({})'.format(r'$\mu$mol/mol'))

    # Al/Ca
    axs[2].scatter(te_1209.AlCa, te_1209.MgCa, marker='+', label='Al/Ca', color=colours_04[2])
    axs[2].scatter(te_1209[te_1209.AlCa > 120].AlCa, te_1209[te_1209.AlCa > 120].MgCa, marker='+', color='r')
    axs[2].set(title='Al/Ca', xlabel='Al/Ca ({})'.format(r'$\mu$mol/mol'))

    for ax in axs.flat:
        ax.set(ylabel='Mg/Ca (mmol/mol)', xlim=[0, 270])
        ax.label_outer()

    # Save the figure if required
    if save_fig:
        plt.savefig("figures/paper/Figure_S3.png", format="png", dpi=300)
    else:
        plt.show()


def figure_s4(save_fig: bool = False, figure_ratio: float = 1.0):
    pass


if __name__ == "__main__":
    figure_s1(save_fig=False)
    figure_s2(save_fig=False, figure_ratio=0.8)
    figure_s3(save_fig=False)
