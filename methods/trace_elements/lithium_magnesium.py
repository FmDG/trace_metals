"""
This file produces a plot that summarises the usefulness of Mg/Li as a palaeothermometer at Site 1209.
"""

import matplotlib.pyplot as plt

from methods.figures.tick_dirs import tick_dirs
from objects.arguments.args_Nature import colours
from objects.core_data.trace_elements import te_1209


def lithium_plots():
    # Set the ages
    min_age, max_age = 2400, 2900

    # Trim 1209
    trimmed_1209 = te_1209.loc[te_1209.age_ka < max_age].copy()

    # Define Mg/Li
    trimmed_1209["MgLi"] = (trimmed_1209.MgCa / trimmed_1209.LiCa)
    trimmed_1209["MgCa_norm"] = (trimmed_1209.MgCa - trimmed_1209.MgCa.min()) / (
                trimmed_1209.MgCa.max() - trimmed_1209.MgCa.min())
    trimmed_1209["MgLi_norm"] = (trimmed_1209.MgLi - trimmed_1209.MgLi.min()) / (
                trimmed_1209.MgLi.max() - trimmed_1209.MgLi.min())

    trimmed_1209["dMg"] = trimmed_1209.MgCa_norm - trimmed_1209.MgLi_norm

    # Set up the plots
    num_plots = 4
    fig, axs = plt.subplots(
        num_plots,
        1,
        sharex="all",
        figsize=(8, 8)
    )

    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    # Title for the plot
    fig.suptitle("Trace Metal Data from 1209")

    # Plot the Mg/Ca ratio at 1209
    axs[0].plot(trimmed_1209.age_ka, trimmed_1209.MgCa, color=colours[0], marker='+')
    # Label the y-axis
    axs[0].set(ylabel='Mg/Ca (mmol/mol)')

    # Plot the Mg/Li ratio at 1209
    axs[1].plot(trimmed_1209.age_ka, trimmed_1209.MgLi, color=colours[1], marker='+')
    # Label the y-axis
    axs[1].set(ylabel='Mg/Li (mmol/mol)')

    # Plot the difference between the Mg/Li and Mg/Ca ratio at 1209
    axs[2].plot(trimmed_1209.age_ka, trimmed_1209.dMg, color=colours[2], marker='+')
    # Label the y-axis
    axs[2].set(ylabel=r'Mg/Ca$_{norm}$ - Mg/Li$_{norm}$')

    # Plot the B/Ca ratio at 1209
    axs[3].plot(trimmed_1209.age_ka, trimmed_1209.BCa, color=colours[3], marker='+')
    # Label the y-axis
    axs[3].set(ylabel='B/Ca ({}mol/mol)'.format(r'$\mu$'))

    tick_dirs(
        axs=axs,
        num_plots=num_plots,
        min_age=min_age,
        max_age=max_age,
        legend=False
    )

    plt.show()


if __name__ == "__main__":
    lithium_plots()
