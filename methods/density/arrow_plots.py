import matplotlib.pyplot as plt

from methods.density.average_densities import average_cdt
from methods.density.density_plots import density_plot
from objects.arguments.args_egypt import colour
from objects.core_data.psu import psu_1208, psu_1209

# Modern Measurements
mod_temp_1209, mod_temp_1208, mod_temp_607 = 1.7, 1.3, 2.2
mod_sal_1209, mod_sal_1208, mod_sal_607 = 34.6, 34.6, 34.9

# Marine Isotope Stages
interglacials = [[2730, 2759, "G7"], [2652, 2681, "G3"], [2614, 2638, "G1"], [2575, 2595, "103"], [2540, 2554, "101"],
                 [2494, 2510, "99"]]
glacials = [[2798, 2820, "G10"], [2681, 2690, "G4"], [2638, 2652, "G2"], [2595, 2614, "104"], [2554, 2575, "102"],
            [2510, 2540, "100"]]
mpwp = [3055, 3087, "K1"]


def arrow_diff(ax: plt.axes, age_lower: int, age_higher: int, lc=None) -> plt.axes:
    ans_01 = average_cdt(psu_1208, age_lower, age_higher)
    ans_02 = average_cdt(psu_1209, age_lower, age_higher)

    ax.annotate(
        xytext=(ans_01[0], ans_01[1]),
        xy=(ans_02[0], ans_02[1]),
        arrowprops=dict(arrowstyle="->", color=lc),
        text=None
    )

    return ax


def arrow_plot_densities(save_fig: bool = False):
    # Generate the density plot
    ax = density_plot(min_sal=32.0, min_temp=-3, max_temp=10)

    # -- Add mPWP densities --
    ax = arrow_diff(ax, age_lower=mpwp[0], age_higher=mpwp[1], lc=colour[2])

    # -- Add Early Pleistocene IG densities (1/4)
    for x in interglacials:
        ax = arrow_diff(ax, age_lower=x[0], age_higher=x[1], lc=colour[0])

    # -- Add Early Pleistocene G densities (1/4)
    for y in glacials:
        ax = arrow_diff(ax, age_lower=y[0], age_higher=y[1], lc=colour[1])

    ax.annotate(
        text=None,
        xytext=(mod_sal_1208, mod_temp_1208),
        xy=(mod_sal_1209, mod_temp_1209),
        arrowprops=dict(arrowstyle="->", color=colour[3]),
    )

    if save_fig:
        plt.savefig("figures/densities/arrow_plot.png", format='png', dpi=150)
    else:
        plt.show()


if __name__ == "__main__":
    arrow_plot_densities(save_fig=True)
