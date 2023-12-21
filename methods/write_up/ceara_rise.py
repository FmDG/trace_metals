import os

import matplotlib.pyplot as plt
import pandas as pd

from objects.args_brewer import args_1209, args_1208, args_607, args_925, args_929
from objects.colours import colours_extra as colours
from objects.core_data.ceara_isotopes import iso_925_cibs, iso_929_cibs, iso_925, iso_929
from objects.core_data.isotopes import iso_607, iso_1208, iso_1209


def ceara_sites(save_fig: bool = False, highlights: bool = False, sites: list = None, figure_name: str = "figure_01",
                age_min: int = 2400, age_max: int = 3300):
    """
    GENERATES PLOT FOR CEARÁ RISE d18O
    The function generates a plot from age_max to age_min of the d18O values from sites in the Ceará Rise from the data
    derived from Wilkens et al., 2017. This also highlights the regions that will be focussed on in the second chapter
    of my PhD project.
    :param save_fig: boolean, determines if the resultant figure should be saved to the ceara_rise folder in the
    figures' directory.
    :param highlights: boolean, determines if the focus regions should be highlighted on the figure.
    :param sites: list of integers, the names of the sites that will appear on the figures. The Ceará Rise is the
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
        # Checks that the sites are actually present on the Ceará Rise
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
        ax.axvpsan(xmin=2400, xmax=2550, fc="b", ec=None, alpha=0.08, label="MIS 95-100")
        ax.axvspan(xmin=3100, xmax=3300, fc="r", ec=None, alpha=0.08, label="KM1 - M2")

    # Select every site
    for x in range(len(sites)):
        site_name = sites[x]
        site_data = pd.read_csv("data/ceara_rise/{}_d18O.csv".format(str(site_name))).dropna(
            subset='d18O_corr').sort_values(by="age_ka")
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
    ax.legend(frameon=True, shadow=False, framealpha=1, ncol=2)

    # Remove unnecessary spines from the plot.
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.tight_layout()

    if save_fig:
        plt.savefig("figures/ceara_rise/{}.png".format(figure_name), format='png', dpi=150)
    else:
        plt.show()


def comparison_ceara(save_fig: bool = False, min_age: int = 2400, max_age: int = 4000, cibs_only: bool = True):
    site_1208 = iso_1208[iso_1208.age_ka.between(min_age, max_age)]
    site_1209 = iso_1209[iso_1209.age_ka.between(min_age, max_age)]
    site_607 = iso_607[iso_607.age_ka.between(min_age, max_age)]

    fig, ax = plt.subplots(
        sharex="all",
        figsize=(16, 8)
    )

    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)
    # Name the Plot
    fig.suptitle("Comparison of Pacific and Atlantic Sites")

    # -- Plot the Pacific d18O isotope data --
    ax.plot(site_1208.age_ka, site_1208.d18O_unadj, **args_1208, lw=2.0)
    ax.plot(site_1209.age_ka, site_1209.d18O_unadj, **args_1209, lw=2.0)

    # -- Plot the 607 data --
    ax.plot(site_607.age_ka, site_607.d18O, **args_607, lw=2.0)

    # -- Plot the Ceara Rise data --
    if cibs_only:
        site_925 = iso_925_cibs[iso_925_cibs.age_ka.between(min_age, max_age)]
        site_929 = iso_929_cibs[iso_929_cibs.age_ka.between(min_age, max_age)]
        ax.plot(site_925.age_ka, site_925.d18O, **args_925, lw=2.0)
        ax.plot(site_929.age_ka, site_929.d18O, **args_929, lw=2.0)
    else:
        site_925 = iso_925[iso_925.age_ka.between(min_age, max_age)]
        site_929 = iso_929[iso_929.age_ka.between(min_age, max_age)]
        ax.plot(site_925.age_ka, (site_925.d18O_corr - 0.64), **args_925, lw=2.0)
        ax.plot(site_929.age_ka, (site_929.d18O_corr - 0.64), **args_929, lw=2.0)

    # -- Define the axes --
    ax.set(ylabel="{} (VPDB {})".format(r'$\delta^{18}$O', u"\u2030"), xlabel='Age (ka)', xlim=[min_age, max_age])

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Invert the axes with d18O and add a legend.
    ax.invert_yaxis()
    ax.legend(frameon=True, shadow=False, framealpha=1, ncol=2)

    # Put a tight layout on the plot
    plt.tight_layout()

    # Save the figure if required
    if save_fig:
        plt.savefig("figures/ceara_rise/Figure_comp.png", format="png", dpi=300)
    else:
        plt.show()

    return 1


if __name__ == "__main__":

    # Change the directory to the parent directory
    if not os.path.isdir("data/cores"):
        os.chdir('../..')

    comparison_ceara(
        save_fig=False,
        min_age=2500,
        max_age=3500,
        cibs_only=False
    )
