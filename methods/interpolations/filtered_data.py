import matplotlib.pyplot as plt
from pandas import DataFrame

from methods.interpolations.low_pass_filter import butter_lowpass_filter
from methods.interpolations.binning_records import binning_multiple_series
from methods.figures.tick_dirs import tick_dirs
from methods.figures.highlight_mis import highlight_mis
from objects.core_data.isotopes import iso_1208, iso_1209
from objects.args_Nature import args_1209, args_1208


def filter_difference(resampled_data: DataFrame, filter_period: float = 10.0):
    # --------------- RESAMPLE ISOTOPE DATA ---------------
    resampled_1209 = resampled_data.d18O_unadj_mean_1209.to_numpy()
    resampled_1208 = resampled_data.d18O_unadj_mean_1208.to_numpy()

    # --------------- FILTER PARAMETERS ---------------
    fs = 2  # Sample rate, in ka
    cutoff = 1.0 / filter_period  # Desired cutoff frequency of the filter, in 1\ka
    nyq = 0.5 * fs  # Nyquist Frequency
    order = 2  # Order of the filter

    # --------------- FILTER DATA ---------------
    filtered_1209 = butter_lowpass_filter(resampled_1209, cutoff, fs, order, nyq)
    filtered_1208 = butter_lowpass_filter(resampled_1208, cutoff, fs, order, nyq)
    return filtered_1208, filtered_1209


def plot_filtered_diff(filter_period: float, save_fig: bool = False):
    # --------------- GENERATE FILTERED DIFFERENCES ---------------
    resampling_freq = 4.0  # Resampling frequency in ka
    age_min, age_max = 2300, 3600  # Minimum and maximum ages in ka
    resampled_data = binning_multiple_series(
        iso_1208, iso_1209,
        names=["1208", "1209"],
        fs=resampling_freq,
        start=age_min,
        end=age_max
    ).dropna()
    # Filter the difference in d18O
    filtered_1208, filtered_1209 = filter_difference(resampled_data, filter_period)

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

    axs[1].plot(iso_1208.age_ka, iso_1208.d18O_unadj)

    axs[2].axhline(0, c="k")  # Plot the 0 line
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
        plt.savefig("figures/interpolations/filtered_data_{:.0f}ka_highlights.png".format(filter_period), format="png", dpi=300)
    else:
        plt.show()


if __name__ == "__main__":
    plot_filtered_diff(
        save_fig=False,
        filter_period=4
    )
