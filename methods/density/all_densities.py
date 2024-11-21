import matplotlib.pyplot as plt
from density_plots import density_plot
from calculations import full_inverse_salinity
from objects.core_data.psu import psu_1208, psu_1209
from objects.arguments.args_Nature import colours, args_1208, args_1209

# Modern Measurements
mod_temp_1209, mod_temp_1208 = 1.805, 1.525
mod_sal_1209, mod_sal_1208 = 34.580, 34.628

mod_d18O_sw_1209, mod_d18O_sw_1208 = -0.078, -0.075


def plot_all_densities(save_fig: bool = False) -> None:
    # Generate the density plot
    ax = density_plot(min_sal=30, max_sal=36, min_temp=-3, max_temp=4, lv=10)

    sal_1209 = []
    for i in range(len(psu_1209.d18O_sw.values)):
        sal_1209.append(full_inverse_salinity(psu_1209.d18O_sw.values[i], psu_1209.age_ka.values[i], mod_d18O_sw_1209, mod_sal_1209))

    sal_1208 = []
    for i in range(len(psu_1208.d18O_sw.values)):
        sal_1208.append(full_inverse_salinity(psu_1208.d18O_sw.values[i], psu_1208.age_ka.values[i], mod_d18O_sw_1208, mod_sal_1208))


    ax.scatter(sal_1208, psu_1208.temp.values, c=colours[0], marker='+')
    ax.scatter(sal_1209, psu_1209.temp.values, c=colours[1], marker='+')

    if save_fig:
        plt.savefig("figures/densities/All_densities.png", format='png', dpi=300)
    else:
        plt.show()


if __name__ == "__main__":
    plot_all_densities(False)