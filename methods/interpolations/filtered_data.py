import matplotlib.pyplot as plt

from methods.interpolations.low_pass_filter import butter_lowpass_filter
from methods.interpolations.generate_interpolations import resample_both
from methods.figures.tick_dirs import tick_dirs
from methods.figures.highlight_mis import highlight_mis
from objects.core_data.isotopes import iso_1208, iso_1209
from objects.args_Nature import args_1209, args_1208, args_diff, fill_diff


def filter_difference(save_fig: bool = False, filter_period: float = 10.0):
    """
    Filter the difference between two isotope datasets and plot the results.

    Args:
        save_fig (bool, optional): If True, save the resulting figure as "filtered_data.png"
                                    in the "figures/interpolations" directory. Default is False.
        filter_period (float, optional): Defines the cut-off period for the low-pass filter

    Returns:
        None

    This function performs the following steps:
    1. Initializes age_min and age_max for the desired age range and sample rate (fs).
    2. Resamples the isotope data in the specified age range, and extracts d18O data.
    3. Defines filter parameters including sample_period, sample rate (fs), cutoff frequency, Nyquist Frequency, and filter order.
    4. Applies a low-pass Butterworth filter to both d18O datasets.
    5. Creates a multi-plot figure to display the original and filtered data.
    6. If save_fig is True, saves the figure as "filtered_data.png"; otherwise, it displays the figure.

    Note:
    - The filter is applied to the difference between the two datasets and also to the individual datasets.
    - The function assumes that the following variables are available in the global scope: iso_1208, iso_1209,
      resample_both, butter_lowpass_filter, and plt (matplotlib.pyplot).

    Example usage:
    filter_difference(save_fig=True)  # Apply filtering and save the resulting figure.
    filter_difference()  # Apply filtering and display the resulting figure.
    """
    # --------------- INITIALISE PARAMETERS ---------------
    age_min, age_max = 2300, 3700  # Age range of the data
    resampling_freq = 4.0  # Resampling Frequency

    # --------------- RESAMPLE ISOTOPE DATA ---------------
    resampled_data = resample_both(resampling_freq, age_min, age_max).dropna()
    resampled_1209 = resampled_data.d18O_1209.to_numpy()
    resampled_1208 = resampled_data.d18O_1208.to_numpy()

    # --------------- FILTER PARAMETERS ---------------
    sample_period = (age_max - age_min)  # Sample Period in ka
    fs = 2  # Sample rate, in ka
    cutoff = 1.0/filter_period  # Desired cutoff frequency of the filter, in 1\ka
    nyq = 0.5 * fs  # Nyquist Frequency
    order = 2  # Order of the filter

    # --------------- FILTER DATA ---------------
    filtered_1209 = butter_lowpass_filter(resampled_1209, cutoff, fs, order, nyq)
    filtered_1208 = butter_lowpass_filter(resampled_1208, cutoff, fs, order, nyq)

    # --------------- DEFINE FIGURE ---------------
    n_figures = 3  # Number of sub-figures
    fig, axs = plt.subplots(
        nrows=n_figures,
        sharex="all",
        figsize=(12, 9)
    )
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    # ------------- HIGHLIGHT MIS ---------------
    highlight_mis(axs)

    # --------------- PLOT DATA ---------------
    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)  # Plot raw isotope d18O data
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)

    axs[1].plot(resampled_data.age_ka, filtered_1208, label="Filtered 1208")  # Plot low-pass filtered data
    axs[1].plot(resampled_data.age_ka, filtered_1209, label="Filtered 1209")

    axs[2].axhline(0, c="k")  # Plot the 0 line

    axs[2].plot(resampled_data.age_ka, resampled_data.d18O_difference, **args_diff)  # Plot up the difference in d18O
    axs[2].plot(resampled_data.age_ka, (filtered_1208 - filtered_1209),
                label="Filtered Difference ({:.0f} ka)".format(filter_period), c="tab:gray")
    axs[2].fill_between(resampled_data.age_ka, (filtered_1208 - filtered_1209), fc="tab:gray", alpha=0.3)

    # --------------- FORMAT AXES ---------------
    tick_dirs(axs, num_plots=n_figures, min_age=age_min, max_age=age_max, legend=True)
    # Label the axes
    axs[0].set(ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[1].set(ylabel='{:.0f}-ka Filtered {} ({} VPDB)'.format(filter_period, r'$\delta^{18}$O', u"\u2030"))
    axs[2].set(ylabel='{} ({} VPDB)'.format(r'$\Delta \delta^{18}$O', u"\u2030"))

    fig.suptitle("Effect of {:.0f}-ka low pass filter".format(filter_period))

    for ax in axs:
        ax.invert_yaxis()  # Invert y-axis due to d18O conventions

    # --------------- EXPORT FIGURE ---------------
    if save_fig:
        plt.savefig("figures/interpolations/filtered_data_{:.0f}ka.png".format(filter_period), format="png", dpi=300)
    else:
        plt.show()


if __name__ == "__main__":
    filter_difference(
        save_fig=False,
        filter_period=5
    )
