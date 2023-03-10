import matplotlib.pyplot as plt

from methods.density.average_densities import average_cdt
from methods.density.density_plots import density_plot

from objects.core_data.psu import psu_1208, psu_1209
from objects.args_egypt import colour

# Modern Measurements
mod_temp_1209, mod_temp_1208, mod_temp_607 = 1.7, 1.3, 2.2
mod_sal_1209, mod_sal_1208, mod_sal_607 = 34.6, 34.6, 34.9


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


def arrow_plot_densities():
    # Generate the density plot
    ax = density_plot(min_sal=32.0, min_temp=-3, max_temp=10)

    # -- Add mPWP densities --
    ax = arrow_diff(ax, age_lower=3060, age_higher=3090, lc=colour[2])

    # -- Add Early Pleistocene IG densities (1/4)
    ax = arrow_diff(ax, age_lower=2730, age_higher=2770, lc=colour[0])
    ax = arrow_diff(ax, age_lower=2655, age_higher=2675, lc=colour[0])
    ax = arrow_diff(ax, age_lower=2615, age_higher=2630, lc=colour[0])
    ax = arrow_diff(ax, age_lower=2570, age_higher=2595, lc=colour[0])

    # -- Add Early Pleistocene G densities (1/4)
    ax = arrow_diff(ax, age_lower=2800, age_higher=2815, lc=colour[1])
    ax = arrow_diff(ax, age_lower=2680, age_higher=2690, lc=colour[1])
    ax = arrow_diff(ax, age_lower=2635, age_higher=2650, lc=colour[1])
    ax = arrow_diff(ax, age_lower=2595, age_higher=2610, lc=colour[1])

    ax.annotate(
        text=None,
        xytext=(mod_sal_1208, mod_temp_1208),
        xy=(mod_sal_1209, mod_temp_1209),
        arrowprops=dict(arrowstyle="->", color=colour[3]),
    )

    plt.show()


if __name__ == "__main__":
    arrow_plot_densities()
