from matplotlib.pyplot import subplots, savefig, show

from binning_records import binning_multiple_series
from filter_data import filter_difference
from methods.figures.tick_dirs import tick_dirs
from objects.args_Nature import args_1209, args_1208
from objects.core_data.isotopes import iso_1208, iso_1209
from rolling_correlations import rolling_correlation
from rolling_pearson import rolling_pearson
from methods.figures.highlight_mis import highlight_mis


def plot_filtered_diff(filter_period: float, save_fig: bool = False):
    # --------------- GENERATE DIFFERENCES ---------------
    resampling_freq = 5.0  # Resampling frequency in ka
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
    rolling_diff = rolling_correlation(window_size=20, frequency=5.0).dropna()  # Generate rolling correlations

    # --------------- DEFINE FIGURE ---------------
    n_figures = 4  # Number of sub-figures
    fig, axs = subplots(
        nrows=n_figures,
        sharex="all",
        figsize=(12, 9)
    )
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    # --------------- HIGHLIGHT MIS ---------------
    highlight_mis(axs)

    # --------------- PLOT DATA ---------------
    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)  # Plot raw isotope d18O data
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)

    axs[1].plot(iso_1208.age_ka, iso_1208.d18O_unadj)  # Plot the 1208 d18O record

    axs[2].axhline(0, c="k", lw=1.0)  # Plot the 0 line
    axs[2].plot(resampled_data.age_ka, (filtered_1208 - filtered_1209),
                label="Filtered Difference ({:.0f} ka)".format(filter_period), c="tab:gray")  # Plot the filtered diff
    axs[2].fill_between(resampled_data.age_ka, (filtered_1208 - filtered_1209), fc="tab:gray", alpha=0.3)

    axs[3].plot(rolling_diff.med_age, (rolling_diff.corr_1208_diff ** 2),
                label="1208 {}-{}".format(r'$\delta^{18}$O', r'$\Delta \delta^{18}$O'))  # Plot the rolling R^2

    # --------------- FORMAT AXES ---------------
    tick_dirs(axs, num_plots=n_figures, min_age=age_min, max_age=age_max, legend=True)
    # Label the axes
    axs[0].set(ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[1].set(ylabel='1208 {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[2].set(ylabel='{} ({} VPDB)'.format(r'$\Delta \delta^{18}$O', u"\u2030"))
    axs[3].set(ylabel="{} on {:.0f}-ka rolling window".format(r'$R^{2}$',
                                                              (rolling_diff.max_age - rolling_diff.min_age).median()),
               ylim=[1, 0])

    fig.suptitle("Effect of {:.0f}-ka low pass filter".format(filter_period))

    for ax in axs:
        ax.invert_yaxis()  # Invert y-axis due to d18O conventions

    # --------------- EXPORT FIGURE ---------------
    if save_fig:
        savefig("figures/interpolations/correlation_highlights.png".format(filter_period), format="png",
                dpi=300)
    else:
        show()


def plot_rolling_corr(window_size: int = 100, filter_period: float = 4.0, save_fig: bool = False):
    # --------------- GENERATE DIFFERENCES ---------------
    resampling_freq = 5.0  # Resampling frequency in ka
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
    resampled_data["difference_d18O"] = resampled_data.d18O_unadj_mean_1208 - resampled_data.d18O_unadj_mean_1209
    rolling_corr_100 = rolling_pearson(resampled_data, "difference_d18O", "d18O_unadj_mean_1208",
                                       window=window_size, start=age_min, end=age_max)
    # --------------- INITIALISE FIGURE ---------------
    num_rows = 6
    fig, axs = subplots(nrows=num_rows, sharex="all", figsize=(12, 16))
    fig.suptitle("Correlation between {} and 1208 {}".format(r'$\Delta \delta^{18}$O', r'$\delta^{18}$O'))
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    # --------------- HIGHLIGHT SECTIONS ---------------
    # 3100 - 2930
    # 2720 - 2540
    # 3210 - 3260
    for ax in axs:
        ax.axvspan(2540, 2720, fc="tab:blue", ec=None, alpha=0.1)
        ax.axvspan(2930, 3110, fc="tab:blue", ec=None, alpha=0.1)
        ax.axvspan(3200, 3260, fc="tab:blue", ec=None, alpha=0.1)

    # --------------- PLOT FIGURE ---------------
    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, label="1208")  # Plot up oxygen isotope record
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, label="1209")  # Plot up oxygen isotope record
    axs[0].legend(frameon=False)

    axs[1].plot(resampled_data.age_ka, resampled_data.d18O_unadj_mean_1208)  # Plot up oxygen isotope record

    axs[2].plot(resampled_data.age_ka, resampled_data.difference_d18O)  # Plot the filtered difference

    axs[3].plot(resampled_data.age_ka, (filtered_1208 - filtered_1209))  # Plot the filtered difference

    axs[4].plot(rolling_corr_100.age_ka, (rolling_corr_100.r ** 2), label="100-ka window")  # Plot the correlation

    axs[5].plot(rolling_corr_100.age_ka, rolling_corr_100.p)  # Plot the significance
    axs[5].axhline(0.05, c='r', ls="--", label="p = 0.05")
    axs[5].legend(frameon=False)

    # --------------- FORMAT AXES ---------------
    axs[0].set(ylabel=r'$\delta^{18}$O')
    axs[1].set(xlim=[age_min, age_max], ylabel=r'1208 $\delta^{18}$O')
    axs[2].set(ylabel='{}'.format(r'$\Delta \delta^{18}$O'))
    axs[3].set(ylabel='{:.0f}-ka filtered {}'.format(filter_period, r'$\Delta \delta^{18}$O'))
    axs[4].set(ylabel=r'Correlation, $R^{2}$')
    axs[4].invert_yaxis()
    axs[5].set(ylabel="Significance, p-value", xlabel="Age (ka)", yscale="log")

    for ax in axs:
        ax.invert_yaxis()

    tick_dirs(axs, num_plots=num_rows, min_age=age_min, max_age=age_max, legend=False)

    # --------------- EXPORT FIGURE ---------------
    if save_fig:
        savefig("figures/interpolations/pearson_correlation_highlight.png".format(filter_period), format="png",
                dpi=300)
    else:
        show()


if __name__ == "__main__":
    plot_rolling_corr(save_fig=True, filter_period=5)
    # plot_filtered_diff(filter_period=5, save_fig=False)
