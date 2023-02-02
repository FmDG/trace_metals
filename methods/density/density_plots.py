import numpy as np
import gsw
import matplotlib.pyplot as plt


def density_plot(min_temp: int = -4, max_temp=15, min_sal=33, max_sal=36, save_fig: bool = False) -> int:
    """
    This function uses the Gibbs Seawater (GSW) library to generate a contour plot of density (sigma-theta)
    given minimum and maximum temperature and salinity values. It takes four parameters, min_temp, max_temp,
    min_sal and max_sal, as input and plots the density contours of the resulting temperature-salinity space.
    It also labels the axes, contour lines and titles the plot.
    :param save_fig: boolean - deciding whether you want to save the figure.
    :param min_temp: minimum temperature of the plot
    :param max_temp: maximum temperature of the plot
    :param min_sal: minimum salinity of the plot
    :param max_sal: maximum salinity of the plot
    :return: density plot
    """
    # Define the temperature and salinity space
    temperatures = np.linspace(min_temp, max_temp, 156)
    salinity = np.linspace(min_sal, max_sal, 156)
    # Create a mesh of this space
    temp, sal = np.meshgrid(temperatures, salinity)
    # Generate a density space using this mesh
    densities = gsw.sigma0(sal, temp)

    # Create the figure
    fig, ax = plt.subplots()
    # Generate contours in density space for each T and S point
    contours = ax.contour(sal, temp, densities, colors="grey", zorder=1)
    # Label the density contours
    plt.clabel(contours, fontsize=10, inline=False, fmt="%.1f")
    # Label the axes
    ax.set(xlabel=r'Salinity ($‰$)', ylabel=r'Temperature ($^\circ$C)', title="Temperature-Salinity Plot")

    plt.tight_layout()

    # Save the figure if required
    if save_fig:
        plt.savefig("figures/Density.png", format="png", dpi=300)
    else:
        plt.show()

    return 1


if __name__ == "__main__":
    density_plot(
        save_fig=False
    )
