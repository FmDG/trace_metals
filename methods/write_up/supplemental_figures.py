import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

import objects.arguments.args_Nature as args_Nat
from methods.density.average_densities import average_cdt, plot_density_diff
from methods.density.density_plots import density_plot
from methods.figures.highlight_mis import highlight_mis
from methods.figures.tick_dirs import tick_dirs
from methods.interpolations.binning_records import binning_multiple_series
from methods.interpolations.filter_data import filter_difference
from methods.interpolations.rolling_pearson import rolling_pearson
from objects.core_data.isotopes import iso_1209, iso_1208
from objects.core_data.lr04 import iso_probstack
from objects.core_data.psu import psu_core_tops_1209, psu_core_tops_1208
from objects.core_data.trace_elements import te_1209


def processing_thresholds(data_set, threshold):
    excess_mn = data_set.MnCa > threshold
    excess_al = data_set.AlCa > threshold
    excess_fe = data_set.FeCa > threshold
    total_excess = excess_mn + excess_fe + excess_al
    return total_excess


def figure_s1(save_fig: bool = False):
    """
    Supplemental Figure. Showing the Mg/Ca, Mn/Ca, Al/Ca, and Fe/Ca values with depth.
    Highlighting the values that are outside the threshold.
    :param save_fig: Save Figure as Figure_S1.svg
    :return:
    """

    # -------------- PREPROCESSING ------------------
    # Determine the values that are in excess of the 120 mmol/mol threshold
    te_1209['excess'] = processing_thresholds(te_1209, 120)

    # -------------- DEFINE FIGURE ------------------
    fig, axs = plt.subplots(
        nrows=4,
        ncols=1,
        figsize=(11, 8),
        sharex="all",
    )

    # ------------ PLOT DATA -----------------------
    # Plot the Mg/Ca data, everything above threshold is highlighted in red
    axs[0].scatter(te_1209.mcd, te_1209.MgCa, label='Included', color=args_Nat.colours[0], marker='+')
    axs[0].scatter(
        te_1209[te_1209['excess']].mcd, te_1209[te_1209['excess']].MgCa,
        label='Excluded',
        color='r',
        marker='+'
    )
    axs[0].legend(shadow=False, frameon=True)

    # Al/Ca
    axs[1].scatter(te_1209.mcd, te_1209.AlCa, label='Al/Ca', color=args_Nat.colours[0], marker='+')
    axs[1].scatter(te_1209[te_1209.AlCa > 120].mcd, te_1209[te_1209.AlCa > 120].AlCa, color='r', marker='+')
    axs[1].axhline(120, ls='--', lw='0.8', color='r', label='Threshold')

    # Mn/Ca
    axs[2].scatter(te_1209.mcd, te_1209.MnCa, label='Mn/Ca', color=args_Nat.colours[0], marker='+')
    axs[2].scatter(te_1209[te_1209.MnCa > 120].mcd, te_1209[te_1209.MnCa > 120].MnCa, color='r', marker='+')
    axs[2].axhline(120, ls='--', lw='0.8', color='r', label='Threshold')

    # Fe/Ca
    axs[3].scatter(te_1209.mcd, te_1209.FeCa, label='Fe/Ca', color=args_Nat.colours[0], marker='+')
    axs[3].scatter(te_1209[te_1209.FeCa > 120].mcd, te_1209[te_1209.FeCa > 120].FeCa, color='r', marker='+')
    axs[3].axhline(120, ls='--', lw='0.8', color='r', label='Threshold')

    # ----------------- FORMAT PLOT ---------------------

    # Define the axes
    axs[0].set(ylabel='Mg/Ca ({})'.format('mmol/mol'))
    axs[1].set(ylabel='Al/Ca ({})'.format(r'$\mu$mol/mol'))
    axs[2].set(ylabel='Mn/Ca ({})'.format(r'$\mu$mol/mol'))
    axs[3].set(ylabel='Fe/Ca ({})'.format(r'$\mu$mol/mol'))

    # For every axis
    for q in range(4):
        # Remove the left/right axes to make the plot look cleaner
        if q % 2 == 1:
            axs[q].yaxis.set(ticks_position="right", label_position='right')
            axs[q].spines['left'].set_visible(False)
        else:
            axs[q].spines['right'].set_visible(False)
        # Remove the top axis
        axs[q].spines['top'].set_visible(False)
        # Add small ticks
        axs[q].xaxis.set_minor_locator(AutoMinorLocator(20))
        axs[q].yaxis.set_minor_locator(AutoMinorLocator(5))

    # Set the bottom axis on and label it with the depth.
    axs[3].spines['bottom'].set_visible(True)
    axs[3].set(xlabel='Depth (mcd)')

    # -------------------- EXPORT FIGURE -------------------------
    # Save figure if needed.
    if save_fig:
        plt.savefig("figures/paper/Figure_S1.pdf", format='pdf')
    else:
        plt.show()


def figure_s2(save_fig: bool = False):
    """
    Generates figure S2. A set of cross-plots showing Mg/Ca against Mn/Ca, Fe/Ca etc... to show that there is no
    correlation between contaminants and measured values.
    :param save_fig: boolean to describe if we want to save this figure as Figure_S2.svg
    :return: no return
    """

    # ---------------- DEFINE FIGURE --------------------
    fig, axs = plt.subplots(
        nrows=1,
        ncols=3,
        sharey='all',
        figsize=(15, 5)
    )
    # Reduce space between axes
    fig.subplots_adjust(hspace=0.1, wspace=0.1)

    # --------------- PLOT DATA ------------------------

    # Al/Ca
    axs[2].scatter(te_1209.AlCa, te_1209.MgCa, marker='+', label='Al/Ca', color=args_Nat.colours[0])
    axs[2].scatter(te_1209[te_1209.AlCa > 120].AlCa, te_1209[te_1209.AlCa > 120].MgCa, marker='+', color='r')
    axs[2].set(xlabel='Al/Ca ({})'.format(r'$\mu$mol/mol'))

    # Mn/Ca
    axs[0].scatter(te_1209.MnCa, te_1209.MgCa, marker='+', label='Mn/Ca', color=args_Nat.colours[0])
    axs[0].scatter(te_1209[te_1209.MnCa > 120].MnCa, te_1209[te_1209.MnCa > 120].MgCa, marker='+', color='r')
    axs[0].set(xlabel='Mn/Ca ({})'.format(r'$\mu$mol/mol'))

    # Fe/Ca
    axs[1].scatter(te_1209.FeCa, te_1209.MgCa, marker='+', label='Fe/Ca', color=args_Nat.colours[0])
    axs[1].scatter(te_1209[te_1209.FeCa > 120].FeCa, te_1209[te_1209.FeCa > 120].MgCa, marker='+', color='r')
    axs[1].set(xlabel='Fe/Ca ({})'.format(r'$\mu$mol/mol'))

    # ------------- FORMAT AXES ----------------------
    # Add small ticks to the axes
    for ax in axs:
        ax.xaxis.set_minor_locator(AutoMinorLocator(5))
        ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    # Add
    for ax in axs.flat:
        ax.set(ylabel='Mg/Ca (mmol/mol)')
        ax.label_outer()

    # --------------- EXPORT FIGURE -----------------
    # Save the figure if required
    if save_fig:
        plt.savefig("figures/paper/Figure_S2.pdf", format='pdf')
    else:
        plt.show()


# FIGURE S3 is a modelling output from the Burls et al., 2017 model and so is not generated here.
def figure_s4(save_fig: bool = False, filter_frequency: float = 5):
    """
    This figure shows the interpolated difference in the d18O_c record of 1208 and 1209
    :param save_fig: determines whether this figure needs to be saved to Figure_S4.svg
    :param filter_frequency: the frequency (in ka) that is resampled to
    :return:
    """
    # ------------------- RESAMPLING -------------
    resampling_freq = 3.0  # Resampling frequency in ka
    age_min, age_max = 2350, 3400  # Minimum and maximum ages in ka
    resampled_data = binning_multiple_series(
        iso_1208, iso_1209,
        names=["1208", "1209"],
        fs=resampling_freq,
        start=age_min,
        end=age_max
    ).dropna()
    # Filter the difference in d18O
    filtered_1208, filtered_1209 = filter_difference(resampled_data, filter_frequency)
    # ------------- DEFINE FIGURE --------------------
    fig, axs = plt.subplots(
        nrows=2,
        ncols=1,
        sharex="all",
        figsize=(12, 7)
    )
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    # ------------- HIGHLIGHT MIS ---------------
    highlight_mis(axs)

    # ------------- PLOT DATA -------------------
    # d18O original data
    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_Nat.args_1208)
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_Nat.args_1209)

    # Plot the interpolated differences
    axs[1].plot(resampled_data.age_ka, (resampled_data.d18O_unadj_mean_1208 - resampled_data.d18O_unadj_mean_1209),
                marker="+", color="tab:grey", label=r'$\Delta \delta^{18}$O', alpha=0.7)

    axs[1].plot(resampled_data.age_ka, (filtered_1208 - filtered_1209), color=args_Nat.colours[3])
    axs[1].fill_between(resampled_data.age_ka, (filtered_1208 - filtered_1209), fc=args_Nat.colours[3], alpha=0.1)

    # ------------- FORMAT AXES ----------------
    # -- Label the axis --
    axs[0].set(ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[1].set(ylabel='{} ({} VPDB)'.format(r'$\Delta \delta^{18}$O', u"\u2030"), ylim=[-0.8, 0.2])

    # Invert the axes
    axs[0].invert_yaxis()
    axs[1].invert_yaxis()

    tick_dirs(axs=axs, num_plots=2, min_age=age_min, max_age=age_max, legend=False)

    # Add a legend
    axs[0].legend(shadow=False, frameon=False)

    # Save the figure or show it
    if save_fig:
        plt.savefig("figures/paper/Figure_S4.pdf", format='pdf')
    else:
        plt.show()


def figure_s5(window_size: int = 100, filter_period: float = 4.0, save_fig: bool = False):
    # --------------- GENERATE DIFFERENCES ---------------
    resampling_freq = 5.0  # Resampling frequency in ka
    age_min, age_max = 2400, 3400  # Minimum and maximum ages in ka
    resampled_data = binning_multiple_series(
        iso_1208, iso_1209, iso_probstack,
        names=["1208", "1209", "ProbStack"],
        fs=resampling_freq,
        start=age_min,
        end=age_max
    ).dropna()
    # Filter the difference in d18O
    filtered_1208, filtered_1209 = filter_difference(resampled_data, filter_period)
    resampled_data["difference_d18O"] = resampled_data.d18O_unadj_mean_1208 - resampled_data.d18O_unadj_mean_1209
    rolling_corr_100 = rolling_pearson(resampled_data, "difference_d18O", "d18O_unadj_mean_ProbStack",
                                       window=window_size, start=age_min, end=age_max)
    # --------------- INITIALISE FIGURE ---------------
    num_rows = 5
    fig, axs = plt.subplots(nrows=num_rows, sharex="all", figsize=(12, 16))
    # Reduce the space between axes to 0
    fig.subplots_adjust(hspace=0)

    # --------------- HIGHLIGHT SECTIONS ---------------
    highlight_mis(axs)
    # --------------- PLOT FIGURE ---------------
    probstack = iso_probstack[iso_probstack.age_ka.between(age_min - 10, age_max + 10)]
    axs[0].plot(probstack.age_ka, probstack.d18O_unadj, c="k")  # Plot up oxygen isotope record

    axs[1].plot(resampled_data.age_ka, resampled_data.difference_d18O, c="k")  # Plot the filtered difference

    axs[2].plot(resampled_data.age_ka, (filtered_1208 - filtered_1209), c="k")  # Plot the filtered difference

    axs[3].plot(rolling_corr_100.age_ka, (rolling_corr_100.r ** 2), label="100-ka window",
                c="k")  # Plot the correlation

    axs[4].plot(rolling_corr_100.age_ka, rolling_corr_100.p, c="k")  # Plot the significance
    axs[4].axhline(0.05, c='r', ls="--", label="p = 0.05")
    axs[4].legend(frameon=False)

    # --------------- FORMAT AXES ---------------
    axs[0].set(xlim=[age_min, age_max], ylabel=r'ProbStack $\delta^{18}$O')
    axs[1].set(ylabel='{}'.format(r'$\Delta \delta^{18}$O'))
    axs[2].set(ylabel='{:.0f}-ka filtered {}'.format(filter_period, r'$\Delta \delta^{18}$O'))
    axs[3].set(ylabel=r'Correlation, $R^{2}$')
    axs[3].invert_yaxis()
    axs[4].set(ylabel="Significance, p-value", xlabel="Age (ka)", yscale="log")

    for ax in axs:
        ax.invert_yaxis()

    tick_dirs(axs, num_plots=num_rows, min_age=age_min, max_age=age_max, legend=False)

    # --------------- EXPORT FIGURE ---------------
    if save_fig:
        plt.savefig("figures/paper/Figure_S5.pdf", format='pdf')
    else:
        plt.show()


#  Figure S6 showing insolation correlating with Dd18O is found in the insolation folder.

def figure_s7(save_fig: bool = False):
    """
    Generates Figure S7 - a density plot in temperature salinity space showing Pliocene and modern densities of water
    masses.
    :param save_fig: Boolean to determine whether to save the figure as Figure_S5.pdf
    :return:
    """
    # -------------------- DATA PARAMETERS ----------------------
    # There is some data that this plot requires which is listed below:
    # Timings for glacial and interglacial intervals to be plotted up
    glacial_interval = [2798, 2820, "G10"]
    interglacial_interval = [2730, 2759, "G7"]
    # Modern Measurements
    mod_temp_1209, mod_temp_1208 = 1.805, 1.525
    mod_sal_1209, mod_sal_1208 = 34.61, 34.65
    # Core Top salinity and temperature - 1209
    holocene_sal_1209, holocene_temp_1209 = average_cdt(psu_core_tops_1209, 0, 12)
    # Core Top salinity and temperature - 1208
    holocene_sal_1208, holocene_temp_1208 = average_cdt(psu_core_tops_1208, 0, 12)

    # ------------------ INITIALISE PLOT --------------------------
    # Generate the density plot
    ax = density_plot(min_sal=32.5, max_sal=35.5, min_temp=-4, max_temp=10, lv=15)

    # ------------------ PLOT DATA ------------------------
    # -- Add the Pliocene density differences
    ax = plot_density_diff(ax, age_lower=glacial_interval[0], age_higher=glacial_interval[1], name=glacial_interval[2],
                           marker="s")
    ax = plot_density_diff(ax, age_lower=interglacial_interval[0], age_higher=interglacial_interval[1],
                           name=interglacial_interval[2], marker="^")
    # -- Add modern densities
    ax.scatter(mod_sal_1208, mod_temp_1208, marker='D', label='1208 (Modern)', color=args_Nat.colours[0])
    ax.scatter(mod_sal_1209, mod_temp_1209, marker='D', label='1209 (Modern)', color=args_Nat.colours[1])
    # -- Add core top densities - Holocene
    ax.scatter(holocene_sal_1208, holocene_temp_1208, marker='o', label='1208 (Holocene)', color=args_Nat.colours[0])
    ax.scatter(holocene_sal_1209, holocene_temp_1209, marker='o', label='1209 (Holocene)', color=args_Nat.colours[1])
    # -- Add core top densities - LGM
    # ax.scatter(lgm_sal_1208, lgm_temp_1208, marker='x', label='1208 (LGM)', color=args_Nat.colours[0])
    # ax.scatter(lgm_sal_1209, lgm_temp_1209, marker='x', label='1209 (LGM)', color=args_Nat.colours[1])

    # -------------- FORMAT PLOT ------------------------

    ax.legend(frameon=True, ncol=2)

    # ---------------- EXPORT FIGURE -----------------------
    if save_fig:
        plt.savefig("figures/paper/Figure_S7.pdf", format='pdf')
    else:
        plt.show()


if __name__ == "__main__":
    # figure_s1(save_fig=True)
    # figure_s2(save_fig=True)
    # figure_s4(save_fig=True, filter_frequency=5)
    figure_s5(save_fig=True, filter_period=5)
    # figure_s7(save_fig=False)
