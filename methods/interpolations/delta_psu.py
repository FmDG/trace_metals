import matplotlib.pyplot as plt

from generate_interpolations import resampling, resample_both
from methods.figures.highlight_mis import highlight_mis
from methods.figures.tick_dirs import tick_dirs
from objects.arguments.args_Nature import args_1208, args_1209, args_diff
from objects.core_data.isotopes import iso_1209, iso_1208
from objects.core_data.psu import psu_1208, psu_1209


def resampled_difference(value: str, resampling_freq: float = 5.0, age_min: int = 2400, age_max: int = 2900):
    # ------------------- RESAMPLE TEMP OUTPUTS -------------------
    resampled_1208 = resampling(psu_1208, age_min, age_max, resampling_freq, value).rename(
        columns={"age_ka": "age_ka", "value_avg": "value_1208"}
    )
    resampled_1209 = resampling(psu_1209, age_min, age_max, resampling_freq, value).rename(
        columns={"age_ka": "age_ka", "value_avg": "value_1209"}
    )
    # Combine the resampled PSU outputs and calculate differences
    resampled_merged = resampled_1208.merge(resampled_1209, on="age_ka").dropna()
    resampled_merged["difference"] = resampled_merged.value_1208 - resampled_merged.value_1209

    return resampled_merged


def delta_temp(save_fig: bool = False):
    """
        Plot temperature data and temperature differences between two datasets.

        Args:
            save_fig (bool, optional): If True, save the figure as an image. Default is False.

        This function generates a plot showing temperature data from two datasets ('psu_1208' and 'psu_1209') and their differences.
        It includes highlights for MIS intervals and custom styling for the plots. The figure is displayed or saved based on the 'save_fig' parameter.

        Note:
            - This function assumes that 'psu_1208' and 'psu_1209' DataFrames are available in the global scope.
            - It relies on custom functions like 'resampling', 'highlight_mis', 'tick_dirs', and styling arguments ('args_1208', 'args_1209', 'args_diff').

        Example:
            delta_temp(save_fig=False)  # Plot and display the figure
            delta_temp(save_fig=True)   # Plot and save the figure as an image
        """
    # ------------------- ERROR HANDLING -------------------
    if not isinstance(save_fig, bool):
        raise ValueError("save_fig must be of type bool")

    # ------------------- INITIALISE VALUES -------------------
    age_min, age_max = 2400, 2900  # min and max ages in ka
    resampling_freq = 5.0

    # ------------------- RESAMPLE TEMP OUTPUTS -------------------
    resampled_temp = resampled_difference("temp", resampling_freq, age_min, age_max)

    # ------------------- INITIALISE FIGURE -------------------
    n_figures = 3
    fig, axs = plt.subplots(
        nrows=n_figures,
        sharex="all",
        figsize=(12, 8)
    )
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    # Highlight the MIS intervals
    highlight_mis(axs)
    # ------------------- PLOT FIGURE -------------------
    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)

    axs[1].plot(psu_1208.age_ka, psu_1208.temp, **args_1208)
    axs[1].plot(psu_1209.age_ka, psu_1209.temp, **args_1209)

    axs[2].plot(resampled_temp.age_ka, resampled_temp.difference, **args_diff)
    axs[2].axhline(0, c="k")

    # ------------------- FORMAT AXES -------------------
    axs[0].set(ylabel="{} ({})".format(r'$\delta^{18}$O', u"\u2030"))
    axs[1].set(ylabel="BWT ({})".format(u'\N{DEGREE SIGN}C'))
    axs[2].set(ylabel="{}BWT ({})".format(r'$\Delta$', u'\N{DEGREE SIGN}C'))

    axs[0].invert_yaxis()

    tick_dirs(axs, n_figures, age_min, age_max, legend=True)

    if save_fig:
        plt.savefig("figures/delta_figures/delta_temp.png", format="png", dpi=300)
    else:
        plt.show()


def delta_d18o_sw(save_fig: bool = False):
    """
        Plot d18O_sw data and d18O_sw differences between two datasets.

        Args:
            save_fig (bool, optional): If True, save the figure as an image. Default is False.

        This function generates a plot showing d18Osw data from two datasets ('psu_1208' and 'psu_1209') and their differences.
        It includes highlights for MIS intervals and custom styling for the plots. The figure is displayed or saved based on the 'save_fig' parameter.

        Note:
            - This function assumes that 'psu_1208' and 'psu_1209' DataFrames are available in the global scope.
            - It relies on custom functions like 'resampling', 'highlight_mis', 'tick_dirs', and styling arguments ('args_1208', 'args_1209', 'args_diff').

        Example:
            delta_d18o_sw(save_fig=False)  # Plot and display the figure
            delta_d18o_sw(save_fig=True)   # Plot and save the figure as an image
        """
    # ------------------- ERROR HANDLING -------------------
    if not isinstance(save_fig, bool):
        raise ValueError("save_fig must be of type bool")

    # ------------------- INITIALISE VALUES -------------------
    age_min, age_max = 2400, 2900  # min and max ages in ka
    resampling_freq = 5.0

    # ------------------- RESAMPLE d18O_sw OUTPUTS -------------------
    resampled_merged = resampled_difference("d18O_sw", resampling_freq, age_min, age_max)

    # ------------------- INITIALISE FIGURE -------------------
    n_figures = 3
    fig, axs = plt.subplots(
        nrows=n_figures,
        sharex="all",
        figsize=(12, 8)
    )
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    # Highlight the MIS intervals
    highlight_mis(axs)
    # ------------------- PLOT FIGURE -------------------
    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)

    axs[1].plot(psu_1208.age_ka, psu_1208.d18O_sw, **args_1208)
    axs[1].plot(psu_1209.age_ka, psu_1209.d18O_sw, **args_1209)

    axs[2].plot(resampled_merged.age_ka, resampled_merged.difference, **args_diff)
    axs[2].axhline(0, c="k")

    # ------------------- FORMAT AXES -------------------
    axs[0].set(ylabel="{} ({})".format(r'$\delta^{18}$O', u"\u2030"))
    axs[1].set(ylabel="{} ({})".format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))
    axs[2].set(ylabel="{} ({})".format(r'$\Delta \delta^{18}$O$_{sw}$', u"\u2030"))

    tick_dirs(axs, n_figures, age_min, age_max, legend=True)  # Add minor ticks to axis
    for ax in axs:
        ax.invert_yaxis()  # Invert y-axis for d18O

    if save_fig:
        plt.savefig("figures/delta_figures/delta_d18O_sw.png", format="png", dpi=300)
    else:
        plt.show()


def delta_psu(save_fig: bool = False):
    """
        Plot temperature data and temperature differences between two datasets.

        Args:
            save_fig (bool, optional): If True, save the figure as an image. Default is False.

        This function generates a plot showing temperature data from two datasets ('psu_1208' and 'psu_1209') and their differences.
        It includes highlights for MIS intervals and custom styling for the plots. The figure is displayed or saved based on the 'save_fig' parameter.

        Note:
            - This function assumes that 'psu_1208' and 'psu_1209' DataFrames are available in the global scope.
            - It relies on custom functions like 'resampling', 'highlight_mis', 'tick_dirs', and styling arguments ('args_1208', 'args_1209', 'args_diff').

        Example:
            delta_temp(save_fig=False)  # Plot and display the figure
            delta_temp(save_fig=True)   # Plot and save the figure as an image
        """
    # ------------------- ERROR HANDLING -------------------
    if not isinstance(save_fig, bool):
        raise ValueError("save_fig must be of type bool")

    # ------------------- INITIALISE VALUES -------------------
    age_min, age_max = 2400, 2900  # min and max ages in ka
    resampling_freq = 5.0

    # ------------------- RESAMPLE OUTPUTS -------------------
    resampled_temp = resampled_difference("temp", resampling_freq, age_min, age_max)
    resampled_d18_o = resampled_difference("d18O_sw", resampling_freq, age_min, age_max)
    resampled_iso = resample_both(resampling_freq, age_min, age_max).dropna()

    # ------------------- INITIALISE FIGURE -------------------
    n_figures = 6
    fig, axs = plt.subplots(
        nrows=n_figures,
        sharex="all",
        figsize=(12, 16)
    )
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    # Highlight the MIS intervals
    highlight_mis(axs)
    # ------------------- PLOT FIGURE -------------------
    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)  # Initial d18O values
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)

    axs[1].plot(resampled_iso.age_ka, resampled_iso.d18O_difference, **args_diff)  # 5-ka rolling difference in d18O

    axs[2].plot(psu_1208.age_ka, psu_1208.temp, **args_1208)  # Initial PSU Temperature estimates.
    axs[2].plot(psu_1209.age_ka, psu_1209.temp, **args_1209)

    axs[3].plot(resampled_temp.age_ka, resampled_temp.difference, **args_diff)  # 5-ka rolling difference
    axs[3].axhline(0, c="k")

    axs[4].plot(psu_1208.age_ka, psu_1208.d18O_sw, **args_1208)  # Initial PSU d18O_sw estimates
    axs[4].plot(psu_1209.age_ka, psu_1209.d18O_sw, **args_1209)

    axs[5].plot(resampled_d18_o.age_ka, resampled_d18_o.difference, **args_diff)  # 5-ka rolling difference
    axs[5].axhline(0, c="k")

    axs[0].set(ylabel="{} ({})".format(r'$\delta^{18}$O', u"\u2030"))
    axs[1].set(ylabel="{} ({})".format(r'$\Delta \delta^{18}$O', u"\u2030"))
    axs[2].set(ylabel="BWT ({})".format(u'\N{DEGREE SIGN}C'))
    axs[3].set(ylabel="{}BWT ({})".format(r'$\Delta$', u'\N{DEGREE SIGN}C'))
    axs[4].set(ylabel="{} ({})".format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))
    axs[5].set(ylabel="{} ({})".format(r'$\Delta \delta^{18}$O$_{sw}$', u"\u2030"))

    axs[0].invert_yaxis()
    axs[1].invert_yaxis()
    axs[3].invert_yaxis()
    axs[4].invert_yaxis()

    tick_dirs(axs, n_figures, age_min, age_max, legend=True)

    if save_fig:
        plt.savefig("figures/delta_figures/delta_psu.png", format="png", dpi=300)
    else:
        plt.show()


if __name__ == '__main__':
    delta_temp(save_fig=True)
    delta_d18o_sw(save_fig=True)
    delta_psu(save_fig=True)
