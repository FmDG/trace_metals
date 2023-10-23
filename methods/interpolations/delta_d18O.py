import matplotlib.pyplot as plt
from pandas import read_csv, DataFrame
from numpy import arange

from objects.core_data.isotopes import iso_1208, iso_1209

from objects.args_Nature import colours, args_1208, args_1209, args_diff
from methods.interpolations.generate_interpolations import resampling
from methods.figures.tick_dirs import tick_dirs


def delta_d18o(save_fig: bool = False):
    """
    This figure shows the interpolated difference in the d18O_c record of 1208 and 1209
    :param save_fig: determines whether this figure needs to be saved to Figure_S4.svg
    :return:
    """
    # --------------- LOAD MIS BOUNDARIES ---------------
    mis_boundaries = read_csv("data/comparisons/MIS_Boundaries.csv")

    # These lists hold the information on the glacial and interglacial d18O averages
    glacial_info = []
    interglacial_info = []

    # --------------- RESAMPLE THE 1208 and 1209 DATA ---------------

    # Define the age array
    fs = 5.0
    age_array = arange(2300, 3700, fs)

    interpolated_values = []

    for age in age_array:
        avg_1208 = iso_1208[iso_1208.age_ka.between(age - (fs/2), age + (fs/2))]["d18O_unadj"].mean()
        avg_1209 = iso_1209[iso_1209.age_ka.between(age - (fs/2), age + (fs/2))]["d18O_unadj"].mean()
        difference = avg_1208 - avg_1209
        interpolated_values.append({"age_ka": age, "d18O_1208": avg_1208, "d18O_1209": avg_1209, "d18O_difference": difference})

    interpolated_frame = DataFrame.from_records(interpolated_values)

    # --------------- DETERMINE INTERVAL INFORMATION ---------------
    # Iterate over the rows of the MIS boundaries
    for index, row in mis_boundaries.iterrows():
        # For each MIS interval, find the average d18O for 1209 and 1208
        values_1209 = iso_1209[iso_1209.age_ka.between(row.age_start, row.age_end)].d18O_unadj
        values_1208 = iso_1208[iso_1208.age_ka.between(row.age_start, row.age_end)].d18O_unadj
        values_difference = interpolated_frame[interpolated_frame.age_ka.between(row.age_start, row.age_end)].d18O_difference
        info = {"age_ka": ((row.age_start + row.age_end) / 2),
                "mean_1209": values_1209.mean(), "std_1209": values_1209.std(),
                "mean_1208": values_1208.mean(), "std_1208": values_1208.std(),
                "max_1209": values_1209.max(), "max_1208": values_1208.max(),
                "min_1209": values_1209.min(), "min_1208": values_1208.min(),
                "difference_d18O": values_difference.mean(), "difference_std": values_difference.std()
                }
        # Add this information to the correct list
        if int(index) % 2 == 0:
            glacial_info.append(info)
        else:
            interglacial_info.append(info)
    # Convert the lists into dataframes
    glacials = DataFrame.from_records(glacial_info)
    interglacials = DataFrame.from_records(interglacial_info)
    # --------------- INITIALISE FIGURE ---------------
    fig, axs = plt.subplots(
        nrows=5,
        ncols=1,
        sharex="all",
        figsize=(12, 14)
    )
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    # --------------- HIGHLIGHT MIS ---------------
    for ax in axs:
        # Highlight MIS 99 (2.494 - 2.51 Ma)
        ax.axvspan(
            xmin=2494,
            xmax=2510,
            ec=None,
            fc='red',
            alpha=0.1
        )
        # Highlight MIS G4 (2.681 - 2.69 Ma)
        ax.axvspan(
            xmin=2681,
            xmax=2690,
            ec=None,
            fc="blue",
            alpha=0.1
        )
        ax.invert_yaxis()
        ax.set(xlabel="Age (ka)", xlim=(2300, 3700))

    # --------------- PLOT DATA ---------------
    # d18O original data
    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)

    # Plot the interpolated differences
    axs[1].errorbar(
        glacials.age_ka, (glacials.mean_1208 - glacials.mean_1209),
        # yerr=(glacials.std_1209 + glacials.std_1208),
        marker="D", c="tab:blue", label="Glacials"
    )
    axs[1].errorbar(
        interglacials.age_ka, (interglacials.mean_1208 - interglacials.mean_1209),
        # yerr=(interglacials.std_1209 + interglacials.std_1208),
        marker="o", c="tab:orange", label="Interglacials"
    )

    axs[2].plot(
        glacials.age_ka, glacials.difference_d18O,
        marker="D", c="tab:blue", label="Glacials"
    )
    axs[2].plot(
        interglacials.age_ka, interglacials.difference_d18O,
        marker="o", c="tab:orange", label="Interglacials"
    )

    axs[3].plot(
        glacials.age_ka, (glacials.max_1208 - glacials.max_1209),
        marker="D", c="tab:blue", label="Glacials"
    )
    axs[3].plot(
        interglacials.age_ka, (interglacials.min_1208 - interglacials.min_1209),
        marker="o", c="tab:orange", label="Interglacials"
    )

    axs[4].plot(interpolated_frame.age_ka, interpolated_frame.d18O_difference, **args_diff)

    axs[1].axhline(0, c='k', lw=1.0)
    axs[2].axhline(0, c='k', lw=1.0)
    axs[3].axhline(0, c='k', lw=1.0)
    axs[4].axhline(0, c='k', lw=1.0)

    # ------------- FORMAT AXES ----------------
    # -- Label the axis --
    axs[0].set(ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[1].set(ylabel='{} Mean {} ({} VPDB)'.format(r'$\Delta$', r'$\delta^{18}$O', u"\u2030"), ylim=(0.3, -0.7))
    axs[2].set(ylabel='Mean {} ({} VPDB)'.format(r'$\Delta \delta^{18}$O', u"\u2030"), ylim=(0.3, -0.7))
    axs[3].set(ylabel='Min/Max {} ({} VPDB)'.format(r'$\Delta \delta^{18}$O', u"\u2030"), ylim=(0.3, -0.7))
    axs[4].set(ylabel='Rolling {} ({} VPDB)'.format(r'$\Delta \delta^{18}$O', u"\u2030"), ylim=(0.3, -0.7))

    tick_dirs(axs, num_plots=5, min_age=2300, max_age=3700, legend=False)

    # Add a legend
    axs[0].legend(shadow=False, frameon=False)
    axs[1].legend(shadow=False, frameon=False)

    # Save the figure or show it
    if save_fig:
        plt.savefig("figures/paper/Figure_S4.pdf", format='pdf')
    else:
        plt.show()


if __name__ == "__main__":
    delta_d18o(
        save_fig=True
    )
