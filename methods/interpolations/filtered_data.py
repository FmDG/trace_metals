import matplotlib.pyplot as plt

from methods.interpolations.low_pass_filter import butter_lowpass_filter
from methods.interpolations.generate_interpolations import resample_both
from objects.core_data.isotopes import iso_1208, iso_1209


def filter_difference(save_fig: bool = False):
    """
    Filter the difference between two isotope datasets and plot the results.

    Args:
        save_fig (bool, optional): If True, save the resulting figure as "filtered_data.png"
                                    in the "figures/interpolations" directory. Default is False.

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
    age_min, age_max = 2300, 3700
    fs = 4.0
    # --------------- RESAMPLE ISOTOPE DATA ---------------
    resampled_data = resample_both(fs, age_min, age_max).dropna()
    resampled_1209 = resampled_data.d18O_1209.to_numpy()
    resampled_1208 = resampled_data.d18O_1208.to_numpy()

    # --------------- FILTER PARAMETERS ---------------
    sample_period = (age_max - age_min)  # Sample Period in ka
    fs = 2  # sample rate, ka
    cutoff = 0.1  # desired cutoff frequency of the filter, 1\ka, slightly higher than actual 1.2 Hz
    nyq = 0.5 * fs  # Nyquist Frequency
    order = 2  # sin wave can be approx represented as quadratic
    n = int(sample_period * fs)  # total number of samples

    y_1209 = butter_lowpass_filter(resampled_1209, cutoff, fs, order, nyq)
    y_1208 = butter_lowpass_filter(resampled_1208, cutoff, fs, order, nyq)

    # --------------- DEFINE FIGURE ---------------
    n_figures = 3
    fig, axs = plt.subplots(
        nrows=n_figures,
        sharex="all",
        figsize=(12, 7)
    )
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, label="1208")
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, label="1209")

    axs[1].plot(resampled_data.age_ka, resampled_data.d18O_difference, label="Difference")
    axs[1].plot(resampled_data.age_ka, (y_1208 - y_1209), label="Filtered Difference")

    axs[2].plot(resampled_data.age_ka, resampled_data.d18O_1208, label="1208")
    axs[2].plot(resampled_data.age_ka, resampled_data.d18O_1209, label="1209")

    axs[2].plot(resampled_data.age_ka, y_1208, label="Filtered 1208")
    axs[2].plot(resampled_data.age_ka, y_1209, label="Filtered 1209")

    for ax in axs:
        ax.set(xlim=(age_min, age_max))
        ax.legend()
        ax.invert_yaxis()

    if save_fig:
        plt.savefig("figures/interpolations/filtered_data.png", format="png")
    else:
        plt.show()


if __name__ == "__main__":
    filter_difference(
        save_fig=False
    )
