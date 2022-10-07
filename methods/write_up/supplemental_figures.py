import matplotlib.pyplot as plt

from objects.core_data.isotopes import iso_1209, iso_1208
from objects.core_data.trace_elements import te_1208, te_1209
import objects.figure_arguments as args
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
        plt.savefig("figures/paper/Figure_S1.png".format(min_age, max_age), format="png", dpi=300)
    else:
        plt.show()

    return 1


if __name__ == "__main__":
    figure_s1(save_fig=False, figure_ratio=1)
