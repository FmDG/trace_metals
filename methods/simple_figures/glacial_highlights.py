import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

from methods.figures.tick_dirs import tick_dirs
from methods.interpolations.generate_interpolations import generate_interpolation
from objects.arguments.args_brewer import args_1209, args_1208, fill_1208, fill_1209
from objects.core_data.isotopes import iso_1209, iso_1208
from objects.core_data.lr04 import iso_lr04
from objects.core_data.psu import psu_1208, psu_1209

# Marine Isotope Stages
interglacials = [
    [3592, 3619, "Gi1"], [3566, 3578, "MG11"], [3532, 3546, "MG9"], [3471, 3517, "MG7"], [3387, 3444, "MG5"],
    [3347, 3372, "MG3"], [3312, 3332, "MG1"], [3238, 3264, "M1"], [3184, 3212, "KM5"], [3150, 3167, "KM3"],
    [3097, 3119, "KM1"], [3055, 3087, "K1"], [3025, 3039, "G21"], [2982.5, 2999, "G19"], [2937, 2966, "G17"],
    [2893, 2913, "G15"], [2858, 2876, "G13"], [2820, 2838, "G11"], [2777, 2798, "G9"], [2730, 2759, "G7"],
    [2690, 2704, "G5"], [2652, 2681, "G3"], [2614, 2638, "G1"], [2575, 2595, "103"], [2540, 2554, "101"],
    [2494, 2510, "99"], [2477, 2452, "97"], [2407, 2427, "95"]
]

glacials = [
    [3578, 3592, "MG12"], [3546, 3566, "MG10"], [3517, 3532, "MG8"], [3444, 3471, "MG6"], [3372, 3387, "MG4"],
    [3332, 3347, "MG2"], [3264, 3312, "M2"], [3212, 3238, "KM6"], [3167, 3184, "KM4"], [3119, 3150, "KM2"],
    [3087, 3097, "K2"], [3039, 3055, "G22"], [2999, 3025, "G20"], [2966, 2982.5, "G18"], [2913, 2937, "G16"],
    [2876, 2893, "G14"], [2838, 2858, "G12"], [2798, 2820, "G10"], [2759, 2777, "G8"], [2704, 2730, "G6"],
    [2681, 2690, "G4"], [2638, 2652, "G2"], [2595, 2614, "104"], [2554, 2575, "102"], [2510, 2540, "100"],
    [2477, 2494, "98"], [2427, 2452, "96"], [2387, 2407, "94"]
]


def glacial_highlights(age_min: int = 2400, age_max: int = 2900, save_fig: bool = False):
    # We use a simple 1D interpolation, with a density of "freq"
    freq = 0.1
    interp_lr04, age_array = generate_interpolation(iso_lr04, fs=freq, start=age_min, end=age_max, pchip=False,
                                                    value="d18O")

    threshold = 3.64
    glacials_thresh = (interp_lr04 > threshold)

    # Generate a plot to display this
    num_plots = 2
    fig, axs = plt.subplots(num_plots, sharex="all", figsize=(14, 6))
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    # Plot the oxygen isotope records from LR04
    # axs[0].plot(age_array, interp_lr04, label="LR04", c='k')
    # axs[0].fill_between(age_array, interp_lr04, threshold, fc='b', ec=None, alpha=0.2)
    # axs[0].set(ylabel='Benthic {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    # axs[0].plot([age_min, age_max], [threshold, threshold], '--', color='k', linewidth=1.0, label='Threshold = {} {}'.format(threshold, u"\u2030"))

    # Plot the oxygen isotope records from 1208 and 1209
    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)
    axs[0].set(ylabel='Benthic {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))

    # PSU BWT estimates
    axs[1].plot(psu_1208.age_ka, psu_1208.temp, **args_1208)
    axs[1].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, **fill_1208)
    axs[1].plot(psu_1209.age_ka, psu_1209.temp, **args_1209)
    axs[1].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, **fill_1209)
    axs[1].set(ylabel="BWT ({})".format(u'\N{DEGREE SIGN}C'))

    # Label the position of the glacials
    axs[0].fill_between(age_array, (glacials_thresh * 5), 0.25, fc='b', ec=None, alpha=0.1, label="Glacial periods")
    axs[1].fill_between(age_array, ((glacials_thresh * 10) - 5), -5, fc='b', ec=None, alpha=0.1,
                        label="Glacial periods")
    axs[0].set_ylim(4, 2)
    axs[1].set_ylim(-2.5, 4.0)

    # Remove the various axes to clean up the plot
    tick_dirs(axs, num_plots=num_plots, min_age=age_min, max_age=age_max, legend=False)

    axs[0].legend(frameon=False, shadow=False)

    # Save the figure if required
    if save_fig:
        plt.savefig("figures/presentation/Figure_2.png", format="png", dpi=300)
    else:
        plt.show()


def glacial_highlights_isotopes(age_min: int = 2400, age_max: int = 2900, save_fig: bool = False):
    # We use a simple 1D interpolation, with a density of "freq"
    freq = 0.1
    interp_lr04, age_array = generate_interpolation(iso_lr04, fs=freq, start=age_min, end=age_max, pchip=False,
                                                    value="d18O")

    threshold = 3.64
    glacials_hits = (interp_lr04 > threshold)

    # Generate a plot to display this
    fig, ax = plt.subplots(1, sharex="all", figsize=(14, 6))
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    # Plot the oxygen isotope records from 1208 and 1209
    ax.plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)
    ax.plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)
    ax.set(ylabel='Benthic {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    ax.invert_yaxis()

    '''
    # Label the position of the glacials
    for section in warm_sections:
        ax.axvspan(xmin=section[0], xmax=section[1], fc="r", ec=None, alpha=0)
    for section in cold_sections:
        ax.axvspan(xmin=section[0], xmax=section[1], fc="b", ec=None, alpha=0.05)

    for section in cold_sections:
        ax.annotate(section[2], (((section[0] + section[1]) / 2 - 2.5), 3.67), fontsize="xx-small")
    '''
    ax.fill_between(age_array, (glacials_hits * 5), 0.25, fc='b', ec=None, alpha=0.05, label=None)
    ax.set_ylim(4, 2)

    ax.legend(frameon=False, shadow=False)

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_minor_locator(AutoMinorLocator(20))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))

    # Set the bottom axis on and label it with the age.
    ax.set(xlabel='Age (ka)', xlim=[age_min, age_max])

    # Save the figure if required
    if save_fig:
        plt.savefig("figures/presentation/glacials_times.png", format="png", dpi=300)
    else:
        plt.show()


if __name__ == "__main__":
    glacial_highlights_isotopes(
        save_fig=True,
        age_max=3600,
        age_min=2400
    )
