import matplotlib.pyplot as plt

from generate_interpolations import resampling
from methods.figures.tick_dirs import tick_dirs
from methods.figures.highlight_mis import highlight_mis
from objects.core_data.psu import psu_1208, psu_1209
from objects.core_data.isotopes import iso_1209, iso_1208
from objects.args_Nature import args_1208, args_1209, args_diff


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
            >>> delta_psu(save_fig=False)  # Plot and display the figure
            >>> delta_psu(save_fig=True)   # Plot and save the figure as an image
        """
    # ------------------- ERROR HANDLING -------------------
    if not isinstance(save_fig, bool):
        raise ValueError("save_fig must be of type bool")

    # ------------------- INITIALISE VALUES -------------------
    age_min, age_max = 2400, 2900  # min and max ages in ka
    smoothing_period = 10  # in ka
    resampling_freq = 5.0

    # ------------------- RESAMPLE TEMP OUTPUTS -------------------
    resampled_1208 = resampling(psu_1208, age_min, age_max, resampling_freq, "temp").rename(
        columns={"age_ka": "age_ka", "value_avg": "temp_1208"}
    )
    resampled_1209 = resampling(psu_1209, age_min, age_max, resampling_freq, "temp").rename(
        columns={"age_ka": "age_ka", "value_avg": "temp_1209"}
    )
    # Combine the resampled PSU outputs and calculate differences
    resampled_temp = resampled_1208.merge(resampled_1209, on="age_ka").dropna()
    resampled_temp["difference_temp"] = resampled_temp.temp_1208 - resampled_temp.temp_1209

    # ------------------- INITIALISE FIGURE -------------------
    n_figures = 2
    fig, axs = plt.subplots(
        nrows=n_figures,
        sharex="all",
        figsize=(12, 7)
    )
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    # Highlight the MIS intervals
    highlight_mis(axs)
    # ------------------- PLOT FIGURE -------------------
    axs[0].plot(psu_1208.age_ka, psu_1208.temp, **args_1208)
    axs[0].plot(psu_1209.age_ka, psu_1209.temp, **args_1209)

    axs[1].plot(resampled_temp.age_ka, resampled_temp.difference_temp, **args_diff)
    axs[1].axhline(0, c="k")

    axs[0].set(ylabel="BWT ({})".format(u'\N{DEGREE SIGN}C'))
    axs[1].set(ylabel="{}BWT ({})".format(r'$\Delta$', u'\N{DEGREE SIGN}C'))

    tick_dirs(axs, n_figures, age_min, age_max, legend=True)

    if save_fig:
        pass
    else:
        plt.show()


if __name__ == '__main__':
    delta_psu()
