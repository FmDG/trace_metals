import pandas as pd
import matplotlib.pyplot as plt
import os

# Change to the correct directory
os.chdir("../..")

# Load the colour palette
colours = ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e']

# Set the age limits
age_min, age_max = 2400, 3200

# Load the datasets
te_1209 = pd.read_csv("data/comparisons/1209_te.csv")
te_1208 = pd.read_csv("data/comparisons/1208_te.csv")
te_607 = pd.read_csv("data/comparisons/607_te.csv")
te_u1313 = pd.read_csv("data/comparisons/U1313_te.csv")

# Set up the figure
fig, axs = plt.subplots(1, 1)

axs.plot(te_1209.age_ka, te_1209.MgCa, marker='+', color=colours[1], label="1209")
axs.plot(te_1208.age_ka, te_1208.MgCa, marker='+', color=colours[2], label="1208")
axs.plot(te_607.age_ka, te_607.MgCa, marker='+', color=colours[3], label="607")
axs.plot(te_u1313.age_ka, te_u1313.MgCa, marker='+', color=colours[4], label="U1313")

axs.legend()

axs.set(xlim=[age_min, age_max])

plt.show()
