import os

import matplotlib.pyplot as plt
import pandas as pd

from objects.colours import colours_extra as colours


def ceara_sites(save_fig: bool = False, highlights: bool = False, sites: list = None, figure_name: str = "figure_01",
                age_min: int = 2400, age_max: int = 3300):
    """
    GENERATES PLOT FOR CEARA RISE d18O
    The function generates a plot from age_max to age_min of the d18O values from sites in the Ceara Rise from the data
    derived from Wilkens et al., 2017. This also highlights the regions that will be focussed on in the second chapter
    of my PhD project.
    :param save_fig: boolean, determines if the resultant figure should be saved to the ceara_rise folder in the
    figures' directory.
    :param highlights: boolean, determines if the focus regions should be highlighted on the figure.
    :param sites: list of integers, the names of the sites that will appear on the figures. The Ceara Rise is the
    location of the ODP Site 925, 926, 927, 928 and 929.
    :param figure_name: string, determine the name of the resultant file if "save_fig" is selected.
    :param age_min: integer, the minimum age of the plot.
    :param age_max: integer, the maximum age of the plot.
    :return:
    """

    # If there are no sites, then by default site 925, 927 and 929 are selected.
    if sites is None:
        sites = [925, 927, 929]
    else:
        # Checks that the sites are actually present on the Ceara Rise
        for x in sites:
            if x not in [925, 926, 927, 928, 929]:
                raise ValueError("Sites not in the Ceara Rise")

    # Generates a figure
    fig, ax = plt.subplots(
        figsize=(9, 6.5),
        sharex='all'
    )

    # If highlights are selected, the areas filled in a faint colour before any of the data is plotted.
    if highlights:
        ax.fill_between([2500, 2550], [1, 1], [5, 5], fc="b", ec=None, alpha=0.08, label="MIS 100, 99")
        ax.fill_between([3200, 3210], [1, 1], [5, 5], fc="r", ec=None, alpha=0.08, label="MIS KM5c")

    # Select every site
    for x in range(len(sites)):
        site_name = sites[x]
        site_data = pd.read_csv("data/ceara_rise/{}_d18O.csv".format(str(site_name))).sort_values(by="age_ka")
        # For each site, plot the age against the corrected d18O from Wilkens 2017
        ax.plot(
            site_data.age_ka, site_data.d18O_corr, marker="+", color=colours[x], label="ODP {}".format(site_name)
        )

    # Set the plot parameters.
    ax.set(
        ylabel='{} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"),
        xlabel='Age (ka)',
        xlim=[age_min, age_max],
        ylim=[1, 5]
    )

    # Invert the axis because it is a plot of d18O.
    ax.invert_yaxis()
    ax.legend(frameon=False, shadow=False)

    # Remove unnecessary spines from the plot.
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    if save_fig:
        plt.savefig("figures/ceara_rise/{}.png".format(figure_name), format='png', dpi=150)
    else:
        plt.show()


if __name__ == "__main__":

    # Change the directory to the parent directory
    if not os.path.isdir("data/cores"):
        os.chdir('../..')

    ceara_sites(
        save_fig=False,
        highlights=True
    )
