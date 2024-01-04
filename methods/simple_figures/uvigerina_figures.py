from objects.core_data.isotopes import uvi_1208, uvi_1209, iso_1208, iso_1209
from objects.arguments.args_Nature import args_1208, args_1209
from methods.figures.tick_dirs import tick_dirs

import matplotlib.pyplot as plt


def uvigerina_comparison(save_fig: bool = False):
    fig, axs = plt.subplots(
        nrows=2,
        figsize=(12, 8)
    )
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    axs[0].plot(uvi_1208.age_ka, uvi_1208.d18O, **args_1208)
    axs[0].plot(uvi_1209.age_ka, uvi_1209.d18O, **args_1209)
    axs[0].set(ylabel="Uvigerina {} ({})".format(r'$\delta^{18}$O', u'\u2030'))

    axs[1].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)
    axs[1].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)
    axs[1].set(ylabel="Cibicidoides {} ({})".format(r'$\delta^{18}$O', u'\u2030'))

    for ax in axs:
        ax.invert_yaxis()

    tick_dirs(axs=axs, num_plots=2, min_age=2300, max_age=3600, legend=True)

    # Save the figure or show it
    if save_fig:
        plt.savefig("figures/Uvigerina_Comparison.pdf", transparent=False)
    else:
        plt.show()


if __name__ == "__main__":
    uvigerina_comparison(save_fig=True)