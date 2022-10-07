import matplotlib.pyplot as plt

from objects.core_data.isotopes import iso_1209, iso_1208
from objects.core_data.trace_elements import te_1208, te_1209
import objects.figure_arguments as args
from objects.colours import colours_04
from methods.figures.tick_dirs import tick_dirs


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
    Supplemental figure 2. A set of cross-plots showing Mg/Ca against Mn/Ca, Fe/Ca etc... to show that there is no
    correlation between contaminants and measured values.
    :param save_fig: boolean to describe if we want to save this figure as Figure_S2.png
    :param figure_ratio: the ratio of x to y in the final displayed/saved figure
    :return: no return
    """
    # Mg/Ca against B/Ca, Mn/Ca, Fe/Ca, and Al/Ca
    num_plots = 4

    fig, axs = plt.subplots(
        nrows=num_plots,
        ncols=1,
        sharex="all",
        figsize=(8, 8*figure_ratio)
    )

    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)
    # Name the Plot
    fig.suptitle("Raw Data - ODP 1209")

    # Mg/Ca
    axs[0].plot(te_1209.mcd, te_1209.MgCa, label='Mg/Ca', color=colours_04[0], marker='+')

    # Fe/Ca
    axs[1].plot(te_1209.mcd, te_1209.FeCa, label='Fe/Ca', color=colours_04[1], marker='+')
    axs[1].axhline(120, ls='--', lw='0.8', color='r', label='Threshold')

    # Al/Ca
    axs[2].plot(te_1209.mcd, te_1209.AlCa, label='Al/Ca', color=colours_04[2], marker='+')
    axs[2].axhline(120, ls='--', lw='0.8', color='r', label='Threshold')

    # Mn/Ca
    axs[3].plot(te_1209.mcd, te_1209.MnCa, label='Mn/Ca', color=colours_04[3], marker='+')
    axs[3].axhline(120, ls='--', lw='0.8', color='r', label='Threshold')

    # Define the axes
    axs[0].set(ylabel='Mg/Ca ({})'.format('mmol/mol'))
    axs[1].set(ylabel='Fe/Ca ({})'.format(r'$\mu$mol/mol'), ylim=[0, 250])
    axs[2].set(ylabel='Al/Ca ({})'.format(r'$\mu$mol/mol'), ylim=[0, 250])
    axs[3].set(ylabel='Mn/Ca ({})'.format(r'$\mu$mol/mol'), ylim=[0, 250])

    for q in range(num_plots):
        # Remove the left/right axes to make the plot look cleaner
        if q % 2 == 1:
            axs[q].yaxis.set(ticks_position="right", label_position='right')
            axs[q].spines['left'].set_visible(False)
        else:
            axs[q].spines['right'].set_visible(False)
        axs[q].spines['top'].set_visible(False)
        axs[q].spines['bottom'].set_visible(False)

    # Set the bottom axis on and label it with the age.
    axs[(num_plots - 1)].spines['bottom'].set_visible(True)
    axs[(num_plots - 1)].set(xlabel="MCD")

    # Save the figure if required
    if save_fig:
        plt.savefig("figures/paper/Figure_S2.png", format="png", dpi=300)
    else:
        plt.show()


if __name__ == "__main__":
    figure_s1()
