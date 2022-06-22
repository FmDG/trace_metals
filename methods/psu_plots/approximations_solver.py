import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns


# Change to the relevant directory
os.chdir("../..")

# Load the isotope data
ox_1208 = pd.read_csv("data/ODP1208_cibs.csv")
ox_1209 = pd.read_csv("data/ODP1209_cibs.csv")

# Load the trace element data
te_1208 = pd.read_csv("data/1208_TraceMetals.csv")
te_1209 = pd.read_csv("data/1209_TraceMetals.csv")

# Load the modelling data
t_1209 = pd.read_csv("data/1209_together_cib.csv")
t_1208 = pd.read_csv("data/1208_together_uvi.csv")

# Decide on the colours for 1208 and 1209
colour_1209, colour_1208 = "#1b9e77", "#d95f02"

_, axs = plt.subplots(2, 2)

sns.scatterplot(data=t_1209, x="MgCa", y='d18O', hue="age_ka", ax=axs[0, 0])
axs[0, 0].set(xlabel="Mg/Ca (1209)", ylabel="d18O (1209)")

sns.scatterplot(data=t_1209, x="MgCa", y='d13C', hue="age_ka", ax=axs[0, 1])
axs[0, 1].set(xlabel="Mg/Ca (1209)", ylabel="d13C (1209)")

sns.scatterplot(data=t_1208, x="MgCa", y='d18O', hue="age_ka", ax=axs[1, 0])
axs[1, 0].set(xlabel="Mg/Ca (1208)", ylabel="d18O (1208)")

sns.scatterplot(data=t_1208, x="MgCa", y='d13C', hue="age_ka", ax=axs[1, 1])
axs[1, 1].set(xlabel="Mg/Ca (1208)", ylabel="d13C (1208)")

fig, axs = plt.subplots(3, sharex=True)
# Remove horizontal space between axes
fig.subplots_adjust(hspace=0)
# Name the Plot
fig.suptitle("Comparison of Sites 1208")


axs[0].plot(t_1208.age_ka, t_1208.MgCa, color=colour_1208, marker="+")
axs[0].set(ylabel="Mg/Ca")

axs[1].plot(t_1208.age_ka, t_1208.d18O, color=colour_1208, marker="+")
axs[1].set(ylabel="d18O")

axs[2].plot(t_1208.age_ka, t_1208.d13C, color=colour_1208, marker="+")
axs[2].set(ylabel="d13C")

for q in range(3):
    # Remove the left/right axes to make the plot look cleaner
    if q % 2 == 1:
        axs[q].yaxis.set(ticks_position="right", label_position='right')
        axs[q].spines['left'].set_visible(False)
    else:
        axs[q].spines['right'].set_visible(False)
    axs[q].spines['top'].set_visible(False)
    axs[q].spines['bottom'].set_visible(False)

# Set the bottom axis on and label it with the age.
axs[2].spines['bottom'].set_visible(True)
axs[2].set(xlabel='Age (ka)', xlim=[2400, 3400])

plt.show()
