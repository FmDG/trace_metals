import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

os.chdir("../..")

psu_1208 = pd.read_csv("data/PSU_Solver/PSU_data_1208.csv")
psu_1209 = pd.read_csv("data/PSU_Solver/PSU_data_1209.csv")

fig, axs = plt.subplots(2, 1, sharex=True)
# Remove horizontal space between axes
fig.subplots_adjust(hspace=0)


axs[0].plot(psu_1208.age_ka, psu_1208.temp, color='green', linestyle='-', alpha=0.5)
axs[0].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_add1, alpha=0.1, facecolor='green')
axs[0].fill_between(psu_1208.age_ka, psu_1208.temp_min2, psu_1208.temp_add2, alpha=0.05, facecolor='green')


axs[1].plot(psu_1209.age_ka, psu_1209.temp, color='red', linestyle='-', alpha=0.5)
axs[1].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_add1, alpha=0.1, facecolor='red')
axs[1].fill_between(psu_1209.age_ka, psu_1209.temp_min2, psu_1209.temp_add2, alpha=0.05, facecolor='red')

for ax in axs:
    ax.set(xlim=[2400, 3300], ylim=[-8, 8], ylabel='Temperature ({}C)'.format(u'\N{DEGREE SIGN}'),
           yticks=np.arange(-7, 8, 2))

plt.show()
