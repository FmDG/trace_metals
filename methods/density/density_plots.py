import numpy as np
import gsw
import matplotlib.pyplot as plt
import pandas as pd

from objects.colours import colours_extra


def density_plot(min_temp: int = -4, max_temp=15, min_sal=33, max_sal=36):
    """
    This function uses the Gibbs Seawater (GSW) library to generate a contour plot of density (sigma-theta)
    given minimum and maximum temperature and salinity values. It takes four parameters, min_temp, max_temp,
    min_sal and max_sal, as input and plots the density contours of the resulting temperature-salinity space.
    It also labels the axes, contour lines and titles the plot.
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

    return ax


def modern_plot(min_temp: int = -4, max_temp=20, min_sal=33, max_sal=36, save_fig: bool = False) -> int:

    ax = density_plot()

    # Create a 10% of the range
    sal_offset = (max_sal - min_sal)/100
    temp_offset = (max_temp - min_temp)/100

    cdt_data = pd.DataFrame(data=[{"temp": 1.7, "sal": 34.4, "label": "1209"}, {"temp": 1.3, "sal": 34.4, "label": "1208"}],)

    ax.scatter(cdt_data.sal, cdt_data.temp, marker='+', c=['r', 'b'])
    for i in range(cdt_data.shape[0]):
        plt.text(x=cdt_data.sal[i] + sal_offset, y=cdt_data.temp[i] + temp_offset, s=cdt_data.label[i])

    # NADW has a temperature of 2 - 4 °C with a salinity of 34.9-35.0 psu
    ax.fill([34.9, 34.9, 35.0, 35.0, 34.9], [2.0, 4.0, 4.0, 2.0, 2.0], label='NADW', c=colours_extra[0], alpha=0.5)
    # AABW has temperatures ranging from −0.8°C to 2°C (35°F), salinities from 34.6 to 34.7
    ax.fill([34.6, 34.6, 34.7, 34.7, 34.6], [2.0, -0.8, -0.8, 2.0, 2.0], label='AABW', c=colours_extra[1], alpha=0.5)
    # In the Pacific Ocean, it has a temperature of 0.1 to 2.0 °C. The salinity of CDW is 34.62 to 34.73
    ax.fill([34.62, 34.62, 34.73, 34.73, 34.62], [2.0, 0.1, 0.1, 2.0, 2.0], label='CDW', c=colours_extra[2], alpha=0.5)
    # Typical temperature values for the AAIW are 3-7°C, and a salinity of 34.2-34.4 psu upon initial formation
    ax.fill([34.2, 34.2, 34.4, 34.4, 34.2], [3.0, 7.0, 7.0, 3.0, 3.0], label='AAIW', c=colours_extra[3], alpha=0.5)

    ax.legend()

    plt.tight_layout()

    # Save the figure if required
    if save_fig:
        plt.savefig("figures/Density.png", format="png", dpi=300)
    else:
        plt.show()

    return 1


if __name__ == "__main__":
    modern_plot(
        save_fig=False
    )
