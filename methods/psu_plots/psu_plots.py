import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import os


# ----------------------------------- IMPLEMENTATION ---------------------------------------------

def implement_psu_plots(min_age, max_age, display=True, save_fig=False, figure_name="Full", mg_ca=True,
                        mg_ca_smooth=False, b_ca=True, b_ca_smooth=True, modelled_temp=True, modelled_d18o=False,
                        d13c=False, d18o=True):

    # Decide on the colours for 1208 and 1209
    colour_1209, colour_1208 = "#1b9e77", "#d95f02"

    # Change to the relevant directory
    os.chdir("../..")

    # Load the isotope data
    ox_1208 = pd.read_csv("data/ODP1208_cibs.csv")
    ox_1209 = pd.read_csv("data/ODP1209_cibs.csv")

    # Load the trace element data
    te_1208 = pd.read_csv("data/1208_TraceMetals.csv")
    te_1209 = pd.read_csv("data/1209_TraceMetals.csv")

    # Load the modelling data
    psu_1208 = pd.read_csv("data/PSU_Solver/PSU_data_1208.csv")
    psu_1209 = pd.read_csv("data/PSU_Solver/PSU_data_1209.csv")

    # Count number of plots
    num_plots = (mg_ca + b_ca + modelled_d18o + modelled_temp + d13c + d18o)
    if num_plots == 0:
        raise ValueError("At least one kind of plot must be selected")

    # Define figure
    if save_fig:
        fig, axs = plt.subplots(num_plots, 1, sharex=True, figsize=(8.25, 11.75))
    else:
        fig, axs = plt.subplots(num_plots, 1, sharex=True)

    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    # Name the Plots
    fig.suptitle("Comparison of Sites 1208/09\n ({} - {} ka)".format(min_age, max_age))

    plot_num = 0
    if d18o:
        # Plot the d18O (Cibicidoides) for Sites 1208 and 1209.
        axs[plot_num].plot(ox_1208.age_ka, ox_1208.d18O, marker='+', color=colour_1208, label='ODP 1208')
        axs[plot_num].plot(ox_1209.age_ka, ox_1209.d18O, marker='+', color=colour_1209, label="ODP 1209")
        # Label the y-axis
        axs[plot_num].set(xlim=[min_age, max_age], ylabel='{} ({})'.format(r'$\delta^{18}$O', u"\u2030"))
        # Inver the y-axis
        axs[plot_num].invert_yaxis()
        plot_num += 1

    if d13c:
        # Plot the d13C (C. Wuellerstorfi) for Sites 1208 and 1209
        axs[plot_num].plot(ox_1208.age_ka, ox_1208.d13C, marker='+', color=colour_1208, label='ODP 1208')
        axs[plot_num].plot(ox_1209.age_ka, ox_1209.d13C, marker='+', color=colour_1209, label="ODP 1209")
        # Label the y-axis
        axs[plot_num].set(xlim=[min_age, max_age], ylabel='{} ({})'.format(r'$\delta^{13}$C', u"\u2030"))
        plot_num += 1

    if mg_ca:
        # If smooth - add a LOWESS curve through the data points which are scattered
        if mg_ca_smooth:
            # Run the smoothing function
            smoothed_1209 = sm.nonparametric.lowess(exog=te_1209.age_ka, endog=te_1209.MgCa, frac=0.2)
            smoothed_1208 = sm.nonparametric.lowess(exog=te_1208.age_ka, endog=te_1208.MgCa, frac=0.2)
            # plot the smoothing function
            axs[plot_num].plot(smoothed_1209[:, 0], smoothed_1209[:, 1], color=colour_1209)
            axs[plot_num].plot(smoothed_1208[:, 0], smoothed_1208[:, 1], color=colour_1208)
            # Plot the raw data
            axs[plot_num].scatter(te_1208.age_ka, te_1208.MgCa, marker='+', color=colour_1208, label="ODP 1208")
            axs[plot_num].scatter(te_1209.age_ka, te_1209.MgCa, marker='+', color=colour_1209, label="ODP 1209")
        # Else, plot a line connecting all the points
        else:
            axs[plot_num].plot(te_1208.age_ka, te_1208.MgCa, marker='+', color=colour_1208, label="ODP 1208")
            axs[plot_num].plot(te_1209.age_ka, te_1209.MgCa, marker='+', color=colour_1209, label="ODP 1209")
        # Label the y-axis
        axs[plot_num].set(ylabel='{} ({})'.format('Mg/Ca', "mmol/mol"))
        plot_num += 1

    if b_ca:
        # Plot the B/Ca ratio for 1208 and 1209
        axs[plot_num].scatter(te_1209.age_ka, te_1209.Bca, marker='+', color=colour_1209, label="ODP 1209")
        # Label the y-axis
        axs[plot_num].set(ylabel='{} ({})'.format('B/Ca', r'$\mu$mol/mol'))
        if b_ca_smooth:
            # Compute a lowess smoothing of the data
            smoothed = sm.nonparametric.lowess(exog=te_1209.age_ka, endog=te_1209.Bca, frac=0.2)
            # Plot this smoothed data
            axs[plot_num].plot(smoothed[:, 0], smoothed[:, 1], color=colour_1209)
        plot_num += 1

    if modelled_temp:
        # Plot the modelled temperature from the PSU_Solver
        axs[plot_num].plot(psu_1208.age_ka, psu_1208.temp, color=colour_1208, linestyle='-', label="ODP 1208")
        # Fill in the confidence intervals (1 sigma)
        axs[plot_num].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_add1, alpha=0.1,
                                   facecolor=colour_1208)
        axs[plot_num].plot(psu_1209.age_ka, psu_1209.temp, color=colour_1209, linestyle='-', label="ODP 1209")
        axs[plot_num].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_add1, alpha=0.1,
                                   facecolor=colour_1209)
        # Label the y-axis
        axs[plot_num].set(ylabel='Modelled {} ({})'.format('Temperature', u'\N{DEGREE SIGN}C'))
        plot_num += 1

    if modelled_d18o:
        axs[plot_num].plot(psu_1208.age_ka, psu_1208.d18O_sw, color=colour_1208, linestyle='-', label="ODP 1208")
        axs[plot_num].fill_between(psu_1208.age_ka, psu_1208.d18O_sw_min1, psu_1208.d18O_sw_add_1, alpha=0.1,
                                   facecolor=colour_1208)
        axs[plot_num].plot(psu_1209.age_ka, psu_1209.d18O_sw, color=colour_1209, linestyle='-', label="ODP 1209")
        axs[plot_num].fill_between(psu_1209.age_ka, psu_1209.d18O_sw_min1, psu_1209.d18O_sw_add_1, alpha=0.1,
                                   facecolor=colour_1209)
        axs[plot_num].set(ylabel='Modelled {} ({})'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))
        plot_num += 1

    for q in range(num_plots):
        # Remove the left/right axes to make the plot look cleaner
        if q % 2 == 1:
            axs[q].yaxis.set(ticks_position="right", label_position='right')
            axs[q].spines['left'].set_visible(False)
        else:
            axs[q].spines['right'].set_visible(False)
        axs[q].spines['top'].set_visible(False)
        axs[q].spines['bottom'].set_visible(False)

    # Set the bottom axis on and label it with the age.
    axs[(num_plots - 1)].spines['bottom'].set_visible(True)
    axs[(num_plots - 1)].set(xlabel='Age (ka)', xlim=[min_age, max_age])

    # Add a legend to the first plot
    axs[0].legend(loc='upper left', shadow=False, frameon=False)

    # Save the figure if required
    if save_fig:
        plt.savefig("figures/TE_and_PSU_data/{}_{}-{}.pdf".format(figure_name, min_age, max_age), format="pdf")

    # Display the figure if required
    if display:
        plt.show()


if __name__ == "__main__":

    implement_psu_plots(
        min_age=2400,
        max_age=2900,
        display=True,
        save_fig=False,
        figure_name="Full",
        mg_ca=True,
        mg_ca_smooth=False,
        b_ca=True,
        b_ca_smooth=False,
        modelled_temp=False,
        modelled_d18o=False,
        d13c=False,
        d18o=True
    )
