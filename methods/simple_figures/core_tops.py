import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

from objects.core_data.core_tops import core_top_1209_uvi, core_top_1208, core_top_1209_cibs
from methods.figures.tick_dirs import tick_dirs
from methods.figures.highlight_mis import highlight_all_mis_greyscale
from objects.arguments.args_Nature import colours


def temp_from_mgca(x):
    return (x - 0.9) / 0.1


def mgca_from_temp(x):
    return (0.1 * x) + 0.9

def core_tops():
    # -- Define the figure --
    n_plots = 3
    fig, axs = plt.subplots(
        nrows=n_plots,
        sharex="all",
        figsize=(12, 8)
    )
    ## - Reduce the space between axes to 0 -
    fig.subplots_adjust(hspace=0)

    # -- Plot the data --
    cibs_data = core_top_1209_cibs.dropna(subset="d18O")
    uvis_data = core_top_1209_uvi.dropna(subset="d18O")
    uvis_1208 = core_top_1208.dropna(subset="d18O")
    mgca_data = core_top_1209_uvi.dropna(subset="MgCa")
    mgca_1208 = core_top_1208.dropna(subset="MgCa")
    axs[0].plot(cibs_data.age_ka, cibs_data.d18O, marker="+", c=colours[1])
    axs[1].plot(uvis_1208.age_ka, uvis_1208.d18O, marker="+", c=colours[0], label="1208")
    axs[1].plot(uvis_data.age_ka, uvis_data.d18O, marker="+", c=colours[1], label="1209")
    axs[2].plot(mgca_data.age_ka, mgca_data.MgCa, marker="+", c=colours[1], label="1209")
    axs[2].plot(mgca_1208.age_ka, mgca_1208.MgCa, marker="+", c=colours[0], label="1208")

    # -- Format the axes --
    axs[0].invert_yaxis()
    axs[1].invert_yaxis()
    ## - Add a second BWT axis -
    secax = axs[2].secondary_yaxis('right', functions=(temp_from_mgca, mgca_from_temp))
    secax.set_ylabel(r'BWT ($\degree$C)', color=colours[2])
    secax.tick_params(axis='y', labelcolor=colours[2])
    secax.yaxis.set_minor_locator(AutoMinorLocator(5))
    ## - Define the axes -
    for ax in axs:
        highlight_all_mis_greyscale(ax)
    axs[0].set_ylabel('Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"), color=colours[2])
    axs[1].set_ylabel('Uvigerina {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"), color=colours[3])
    axs[2].set_ylabel('Uvigerina Mg/Ca ({}mol/mol)'.format(r'$\mu$'), color=colours[2])
    ## - Set up Tick Dirs -
    tick_dirs(axs, n_plots, -5, 80, True)

    print(temp_from_mgca(1.09))
    print(mgca_from_temp(1.805))

    print(mgca_from_temp(1.525))

    plt.show()


if __name__ == "__main__":
    core_tops()
