import matplotlib.pyplot as plt

from methods.interpolations.low_pass_filter import butter_lowpass_filter
from methods.interpolations.generate_interpolations import resample_both
from objects.core_data.isotopes import iso_1208, iso_1209


def filter_difference(save_fig: bool = False):
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

    plt.show()


if __name__ == "__main__":
    filter_difference()
