import matplotlib.pyplot as plt

from insolation_comparison import generate_insolation_frame
from insolation_difference_correlation import insol_correlation
from methods.figures.tick_dirs import tick_dirs
from methods.interpolations.binning_records import binning_multiple_series
from methods.interpolations.filter_data import filter_difference
from objects.core_data.isotopes import iso_1208, iso_1209


def insolation_plots(age_min: float = 2300, age_max: float = 3600, save_fig: bool = False):
    # --------------- GENERATE DIFFERENCES ---------------
    resampling_freq = 5.0  # Resampling frequency in ka
    filter_period = 5.0
    resampled_data = binning_multiple_series(
        iso_1208, iso_1209,
        names=["1208", "1209"],
        fs=resampling_freq,
        start=int(age_min),
        end=int(age_max)
    ).dropna()
    # Filter the difference in d18O
    filtered_1208, filtered_1209 = filter_difference(resampled_data, filter_period)
    resampled_data["difference_d18O"] = resampled_data.d18O_unadj_mean_1208 - resampled_data.d18O_unadj_mean_1209

    latitude = 65
    insol_frame = generate_insolation_frame(age_min, age_max, latitude=latitude)

    corr_insol_frame = insol_correlation(insol_frame, resampled_data, int(age_min), int(age_max), resampling_freq)

    num_plots = 5
    fig, axs = plt.subplots(
        nrows=num_plots,
        figsize=(12, 12),
        sharex="all",
    )
    fig.subplots_adjust(hspace=0)

    axs[0].plot(insol_frame.age_ka, insol_frame.summer_insolation, c="k")
    axs[0].set(ylabel='Summer solstice insolation at {}{}N\n({})'.format(latitude, r'$\degree$', r'W m$^{-1}$'))

    axs[1].plot(insol_frame.age_ka, insol_frame.summer_gradient, c="k")
    axs[1].set(
        ylabel='Summer solstice insolation gradient ({}{}N - 0{})\n({})'.format(latitude, r'$\degree$', r'$\degree$',
                                                                                r'W m$^{-1}$'))

    axs[2].plot(resampled_data.age_ka, (filtered_1208 - filtered_1209), c="k")  # Plot the filtered difference
    axs[2].set(ylabel="{}-ka filtered {} ({})".format(filter_period, r'$\Delta \delta^{18}$O', u'\u2030'))
    axs[2].invert_yaxis()

    axs[3].plot(corr_insol_frame.age_ka, (corr_insol_frame.r ** 2), c="k")
    axs[3].set(ylabel=r'Correlation, $R^{2}$')

    axs[4].plot(corr_insol_frame.age_ka, corr_insol_frame.p, c="k")
    axs[4].axhline(0.05, c='r', ls="--", label="p = 0.05")
    axs[4].legend(frameon=False)
    axs[4].set(ylabel="Significance, p-value", xlabel="Age (ka)", yscale="log")
    axs[4].invert_yaxis()

    # fig.suptitle(r'Correlation between the Summer Insolation at 65$\degree$N and $\Delta \delta^{18}$O')

    tick_dirs(axs, num_plots, int(age_min), int(age_max), False)

    if save_fig:
        plt.savefig("figures/Correlation_Insolation_d18O_Difference.pdf", format="pdf")
    else:
        plt.show()


if __name__ == "__main__":
    insolation_plots(age_min=2350, age_max=3600, save_fig=False)
