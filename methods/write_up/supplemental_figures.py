import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import AutoMinorLocator
from matplotlib import rcParams

from objects.core_data.isotopes import iso_1209, iso_1208
from objects.core_data.trace_elements import te_1209
import objects.args_Nature as args_Nat
from methods.interpolations.generate_interpolations import resampling
from methods.figures.tick_dirs import tick_dirs

rcParams["pdf.fonttype"] = 42
rcParams['ps.fonttype'] = 42


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
    axs[1].scatter(te_1209.mcd, te_1209.AlCa, label='Al/Ca', color=args_Nat.colours[1], marker='+')
    axs[1].scatter(te_1209[te_1209.AlCa > 120].mcd, te_1209[te_1209.AlCa > 120].AlCa, color='r', marker='+')
    axs[1].axhline(120, ls='--', lw='0.8', color='r', label='Threshold')

    # Mn/Ca
    axs[2].scatter(te_1209.mcd, te_1209.MnCa, label='Mn/Ca', color=args_Nat.colours[2], marker='+')
    axs[2].scatter(te_1209[te_1209.MnCa > 120].mcd, te_1209[te_1209.MnCa > 120].MnCa, color='r', marker='+')
    axs[2].axhline(120, ls='--', lw='0.8', color='r', label='Threshold')

    # Fe/Ca
    axs[3].scatter(te_1209.mcd, te_1209.FeCa, label='Fe/Ca', color=args_Nat.colours[3], marker='+')
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
        plt.savefig("figures/paper/Figure_S1.svg", format="svg")
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
    axs[2].scatter(te_1209.AlCa, te_1209.MgCa, marker='+', label='Al/Ca', color=args_Nat.colours[1])
    axs[2].scatter(te_1209[te_1209.AlCa > 120].AlCa, te_1209[te_1209.AlCa > 120].MgCa, marker='+', color='r')
    axs[2].set( xlabel='Al/Ca ({})'.format(r'$\mu$mol/mol'))

    # Mn/Ca
    axs[0].scatter(te_1209.MnCa, te_1209.MgCa, marker='+', label='Mn/Ca', color=args_Nat.colours[2])
    axs[0].scatter(te_1209[te_1209.MnCa > 120].MnCa, te_1209[te_1209.MnCa > 120].MgCa, marker='+', color='r')
    axs[0].set(xlabel='Mn/Ca ({})'.format(r'$\mu$mol/mol'))

    # Fe/Ca
    axs[1].scatter(te_1209.FeCa, te_1209.MgCa, marker='+', label='Fe/Ca', color=args_Nat.colours[3])
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
        plt.savefig("figures/paper/Figure_S2.svg", format="svg", dpi=300)
    else:
        plt.show()


# FIGURE S3 is a modelling output from the Burls et al., 2017 model and so is not generated here.

def figure_s4(save_fig: bool = False, sampling_frequency: float = 5, dropna: bool = False):
    """
    This figure shows the interpolated difference in the d18O_c record of 1208 and 1209
    :param save_fig: determines whether this figure needs to be saved to Figure_S4.svg
    :param sampling_frequency: the frequency (in ka) that is resampled to
    :param dropna: whether to drop the NAN values in the resampling.
    :return:
    """
    # ------------------- PREPROCESSING -------------
    age_array, values_1208 = resampling(
        iso_1208,
        start=2400,
        end=3600,
        fs=sampling_frequency,
        value="d18O_unadj"
    )
    _, values_1209 = resampling(
        iso_1209,
        start=2400,
        end=3600,
        fs=sampling_frequency,
        value="d18O_unadj"
    )

    # Join the new data together in one DataFrame
    new_data = pd.DataFrame(list(zip(values_1208, values_1209)), columns=['d18O_1208', 'd18O_1209'])
    new_data['age_ka'] = age_array.tolist()

    new_data["difference"] = new_data.d18O_1208 - new_data.d18O_1209
    if dropna:
        new_data = new_data.dropna(subset='difference')

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

    # ------------- PLOT DATA -------------------
    # d18O original data
    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_Nat.args_1208)
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_Nat.args_1209)

    # Plot the interpolated differences
    axs[1].plot(new_data.age_ka, new_data.difference, **args_Nat.args_diff)
    axs[1].fill_between(new_data.age_ka, new_data.difference, **args_Nat.fill_diff)

    # ------------- FORMAT AXES ----------------
    # -- Label the axis --
    axs[0].set(ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[1].set(ylabel='{} ({} VPDB)'.format(r'$\Delta \delta^{18}$O', u"\u2030"))

    # Invert the axes
    axs[0].invert_yaxis()
    axs[1].invert_yaxis()

    tick_dirs(axs=axs, num_plots=2, min_age=2400, max_age=3600, legend=False)

    # Add a legend
    axs[0].legend(shadow=False, frameon=False)

    # Save the figure or show it
    if save_fig:
        plt.savefig("figures/paper/Figure_S4.svg", format='svg')
    else:
        plt.show()


def figure_s5(save_fig: bool = False):
    pass


if __name__ == "__main__":
    figure_s1(save_fig=True)
    figure_s2(save_fig=True)
    figure_s4(save_fig=True, sampling_frequency=5, dropna=False)
