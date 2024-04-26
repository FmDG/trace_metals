import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

from methods.figures.tick_dirs import tick_dirs
from methods.interpolations.generate_interpolations import generate_interpolation
from objects.arguments.args_Nature import args_1209, args_1208, args_diff
from objects.core_data.isotopes import iso_1209, iso_1208


def interpolations_glacials(age_min: int = 2400, age_max: int = 3400, window: int = 40, save_fig: bool = False):
    # We use a simple 1D interpolation, with a density of "freq"
    freq = 0.1
    interp_1208, age_array = generate_interpolation(iso_1208, fs=freq, start=age_min, end=age_max, pchip=False)
    interp_1209, _ = generate_interpolation(iso_1209, fs=freq, start=age_min, end=age_max, pchip=False)

    threshold = 3.0
    glacials = (interp_1208 > threshold)

    # Filter interpolation function over "window" ka, with a polynomial function of order "n"
    n = 3
    filtered_diff = savgol_filter((interp_1208 - interp_1209), int(window / freq + 1), n)

    # Generate a plot to display this
    num_plots = 3
    fig, axs = plt.subplots(num_plots, sharex="all", figsize=(15, 10))
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    # Plot the oxygen isotope records from 1208 and 1209
    axs[0].plot(age_array, interp_1208, label="1208", c='k')
    axs[0].fill_between(age_array, interp_1208, threshold, fc='b', ec=None, alpha=0.2)
    axs[0].set(ylabel='Benthic {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[0].plot([age_min, age_max], [threshold, threshold], '--', color='k', linewidth=1.0,
                label='Threshold = {} {}'.format(threshold, u"\u2030"))

    # Plot the oxygen isotope records from 1208 and 1209
    axs[1].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)
    axs[1].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)
    axs[1].set(ylabel='Benthic {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))

    # Plot the difference between the isotope records
    axs[2].plot(age_array, (interp_1208 - interp_1209), **args_diff)
    axs[2].plot(age_array, filtered_diff, label="Rolling mean ({} ka)".format(window), c='k')
    axs[2].set(xlabel="Age (ka)", ylabel="Difference in {} ({})".format(r'$\delta^{18}$O', u"\u2030"),
               xlim=[age_min, age_max], ylim=[-0.8, 0.2])

    # Label the position of the glacials
    axs[2].fill_between(age_array, ((glacials * -10) + 0.25), 0.25, fc='b', ec=None, alpha=0.1, label="Glacial periods")

    for ax in axs:
        ax.invert_yaxis()

    # Remove the various axes to clean up the plot
    tick_dirs(axs, num_plots=num_plots, min_age=age_min, max_age=age_max)

    # Show the plot
    if save_fig:
        plt.savefig("figures/interpolations/figure_01.png", format='png', dpi=300)
    else:
        plt.show()


def glacial_delta(age_min: int = 2400, age_max: int = 2750):
    # We use a simple 1D interpolation, with a density of "freq"
    freq = 0.1

    subset_1208, _ = generate_interpolation(iso_1208, fs=freq, start=age_min, end=age_max, pchip=False)
    subset_1209, _ = generate_interpolation(iso_1209, fs=freq, start=age_min, end=age_max, pchip=False)

    threshold = 3.0
    subset_diff = subset_1208 - subset_1209

    # Determine the difference during glacial and interglacial periods
    diff_glacial = subset_diff[subset_1208 > threshold]
    diff_interglacial = subset_diff[subset_1208 <= threshold]

    return diff_glacial.mean(), diff_glacial.std(), diff_interglacial.mean(), diff_interglacial.std()


if __name__ == "__main__":
    g_mean, g_std, ig_mean, ig_std = glacial_delta()
    print(f"Glacial Dd18O = \t\t{g_mean:.6f} ± {g_std:.6f} \nInterglacial Dd18O = \t{ig_mean:.6f} ± {ig_std:.6f}")
