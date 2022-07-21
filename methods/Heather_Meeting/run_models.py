import os

import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Helvetica"

os.chdir('../..')

# Load the datasets
data_607 = pd.read_csv("data/PSU_Solver/RUN_5/607_run.csv")
data_1209 = pd.read_csv("data/PSU_Solver/RUN_5/1209_run.csv")
data_1208 = pd.read_csv("data/PSU_Solver/RUN_5/1208_run.csv")

# Load the trace metal data
te_607 = pd.read_csv("data/PSU_Solver/sets/607_MgCa.csv")
te_1208 = pd.read_csv("data/stacks/1208_TraceMetals.csv")
te_1209 = pd.read_csv("data/stacks/1209_TraceMetals.csv")

# The iNHG Filler
x_inhg = [2550, 2750]
min_inhg = [-1000, -1000]
max_inhg = [1000, 1000]


# colours = ['#1b9e77', '#d95f02', '#7570b3']
colours = ['r', 'b', 'g']


num_plots = 3
save_fig = True
min_age, max_age = 2400, 2900
alpha = 0.1

# Define figure
if save_fig:
    fig, axs = plt.subplots(num_plots, 1, sharex=True, figsize=(16, 16))
else:
    fig, axs = plt.subplots(num_plots, 1, sharex=True)
# Remove horizontal space between axes
fig.subplots_adjust(hspace=0)

for ax in axs:
    # ax.fill_between(x_inhg, min_inhg, max_inhg, alpha=alpha, facecolor='c')
    pass


# Plot the TE
axs[0].plot(te_1208.age_ka, te_1208.MgCa, marker='+', color=colours[0], label="ODP 1208")
axs[0].plot(te_1209.age_ka, te_1209.MgCa, marker='+', color=colours[1], label="ODP 1209")
# Label the y-axis
axs[0].set(ylabel='{} ({})'.format('Mg/Ca', "mmol/mol"), ylim=[0.65, 1.35])

# Plot the Modelled Temp
axs[1].plot(data_1208.age_ka, data_1208.temp, marker='+', color=colours[0], label="ODP 1208")
axs[1].fill_between(data_1208.age_ka, data_1208.temp_min1, data_1208.temp_plus1, alpha=alpha, facecolor=colours[0])
axs[1].plot(data_1209.age_ka, data_1209.temp, marker='+', color=colours[1], label="ODP 1209")
axs[1].fill_between(data_1209.age_ka, data_1209.temp_min1, data_1209.temp_plus1, alpha=alpha, facecolor=colours[1])
axs[1].plot(data_607.age_ka, data_607.temp, marker='+', color=colours[2], label="ODP 607")
axs[1].fill_between(data_607.age_ka, data_607.temp_min1, data_607.temp_plus1, alpha=alpha, facecolor=colours[2])
# Label the y-axis
axs[1].set(ylabel='Modelled {} ({})'.format('Temperature', u'\N{DEGREE SIGN}C'), ylim=[-4.2, 6.5])

# Plot the Modelled d18O
axs[2].plot(data_1208.age_ka, data_1208.d18O_sw, marker='+', color=colours[0], label="ODP 1208")
axs[2].fill_between(data_1208.age_ka, data_1208.d18O_min1, data_1208.d18O_plus1, alpha=alpha, facecolor=colours[0])
axs[2].plot(data_1209.age_ka, data_1209.d18O_sw, marker='+', color=colours[1], label="ODP 1209")
axs[2].fill_between(data_1209.age_ka, data_1209.d18O_min1, data_1209.d18O_plus1, alpha=alpha, facecolor=colours[1])
axs[2].plot(data_607.age_ka, data_607.d18O_sw, marker='+', color=colours[2], label="ODP 607")
axs[2].fill_between(data_607.age_ka, data_607.d18O_min1, data_607.d18O_plus1, alpha=alpha, facecolor=colours[2])
# Label the y-axis
axs[2].set(ylabel='Modelled {} ({})'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"), ylim=[-1.1, 1.9])

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
axs[1].legend(loc='upper left', shadow=False, frameon=False)

plt.savefig("figures/PSU_runs/run_05.png", format='png')
# plt.show()

