import matplotlib.pyplot as plt
import pandas as pd
import os

# Settings
min_age, max_age = 2450, 2850
display = True
saveFig = False

# Features
MgCa = True
BCa = False
modelled_Temp = True
modelled_d18O = False
d13C = True
d18O = True

# Decide on the colours for 1208 and 1209
colour_1209, colour_1208 = "#1b9e77", "#d95f02"

# ----------------------------------- IMPLEMENTATION ---------------------------------------------
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
num_plots = (MgCa + BCa + modelled_d18O + modelled_Temp + d13C + d18O)
if num_plots == 0:
    raise ValueError("At least one kind of plot must be selected")

# Define figure
if saveFig:
    fig, axs = plt.subplots(num_plots, 1, sharex=True, figsize=(8.25, 11.75))
else:
    fig, axs = plt.subplots(num_plots, 1, sharex=True)

# Remove horizontal space between axes
fig.subplots_adjust(hspace=0)

fig.suptitle("Comparison of Sites 1208/09\n ({} - {} ka)".format(min_age, max_age))


plot_num = 0
if d18O:
    axs[plot_num].plot(ox_1208.age_ka, ox_1208.d18Oadj, marker='+', color=colour_1208, label='ODP 1208')
    axs[plot_num].plot(ox_1209.age_ka, ox_1209.d18Oadj, marker='+', color=colour_1209, label="ODP 1209")
    axs[plot_num].set(xlim=[min_age, max_age], ylabel='{} ({})'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[plot_num].invert_yaxis()
    plot_num += 1

if d13C:
    axs[plot_num].plot(ox_1208.age_ka, ox_1208.d13C, marker='+', color=colour_1208, label='ODP 1208')
    axs[plot_num].plot(ox_1209.age_ka, ox_1209.d13C, marker='+', color=colour_1209, label="ODP 1209")
    axs[plot_num].set(xlim=[min_age, max_age], ylabel='{} ({})'.format(r'$\delta^{13}$C', u"\u2030"))
    plot_num += 1

if MgCa:
    axs[plot_num].plot(te_1208.age_ka, te_1208.MgCa, marker='+', color=colour_1208, label="ODP 1208")
    axs[plot_num].plot(te_1209.age_ka, te_1209.MgCa, marker='+', color=colour_1209, label="ODP 1209")
    axs[plot_num].set(ylabel='{} ({})'.format('Mg/Ca', "mmol/mol"))
    plot_num += 1

if BCa:
    axs[plot_num].scatter(te_1209.age_ka, te_1209.Bca, marker='+', color=colour_1209, label="ODP 1209")
    axs[plot_num].set(ylabel='{} ({})'.format('B/Ca', r'$\mu$mol/mol'))
    plot_num += 1

if modelled_Temp:
    axs[plot_num].plot(psu_1208.age_ka, psu_1208.temp, color=colour_1208, linestyle='-', label="ODP 1208")
    axs[plot_num].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_add1, alpha=0.1,
                               facecolor=colour_1208)
    axs[plot_num].plot(psu_1209.age_ka, psu_1209.temp, color=colour_1209, linestyle='-', label="ODP 1209")
    axs[plot_num].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_add1, alpha=0.1,
                               facecolor=colour_1209)
    axs[plot_num].set(ylabel='Modelled {} ({})'.format('Temperature', u'\N{DEGREE SIGN}C'))
    plot_num += 1

if modelled_d18O:
    axs[plot_num].plot(psu_1208.age_ka, psu_1208.d18O_sw, color=colour_1208, linestyle='-', label="ODP 1208")
    axs[plot_num].fill_between(psu_1208.age_ka, psu_1208.d18O_sw_min1, psu_1208.d18O_sw_add_1, alpha=0.1,
                               facecolor=colour_1208)
    axs[plot_num].plot(psu_1209.age_ka, psu_1209.d18O_sw, color=colour_1209, linestyle='-', label="ODP 1209")
    axs[plot_num].fill_between(psu_1209.age_ka, psu_1209.d18O_sw_min1, psu_1209.d18O_sw_add_1, alpha=0.1,
                               facecolor=colour_1209)
    axs[plot_num].set(ylabel='Modelled {} ({})'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))
    plot_num += 1

for q in range(num_plots):
    if q % 2 == 1:
        axs[q].yaxis.set(ticks_position="right", label_position='right')
        axs[q].spines['left'].set_visible(False)
    else:
        axs[q].spines['right'].set_visible(False)

for ax in axs:
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

axs[(num_plots - 1)].spines['bottom'].set_visible(True)
axs[(num_plots - 1)].set(xlabel='Age (ka)', xlim=[min_age, max_age])


axs[0].legend(loc='upper left', shadow=False, frameon=False)

if saveFig:
    plt.savefig("figure_01.pdf", format="pdf")

if display:
    plt.show()
