import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

os.chdir("../..")

psu_1208 = pd.read_csv("data/PSU_Solver/PSU_data_1208.csv")
psu_1209 = pd.read_csv("data/PSU_Solver/PSU_data_1209.csv")

temp_min, temp_max = -8, 8
age_min, age_max = 2400, 3300

# noinspection PyTypeChecker
fig, axs = plt.subplots(3, 1, sharex=True)
# Remove horizontal space between axes
fig.subplots_adjust(hspace=0)


axs[0].plot(psu_1208.age_ka, psu_1208.temp, color='green', linestyle='-', alpha=0.5)
axs[0].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_add1, alpha=0.1, facecolor='green')
# axs[0].fill_between(psu_1208.age_ka, psu_1208.temp_min2, psu_1208.temp_add2, alpha=0.05, facecolor='green')


axs[1].plot(psu_1209.age_ka, psu_1209.temp, color='red', linestyle='-', alpha=0.5)
axs[1].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_add1, alpha=0.1, facecolor='red')
# axs[1].fill_between(psu_1209.age_ka, psu_1209.temp_min2, psu_1209.temp_add2, alpha=0.05, facecolor='red')

axs[2].plot(psu_1208.age_ka, psu_1208.temp, color='green', linestyle='-', alpha=1)
axs[2].plot(psu_1209.age_ka, psu_1209.temp, color='red', linestyle='-', alpha=1)

for ax in axs:
    ax.set(xlim=[age_min, age_max], ylim=[temp_min, temp_max], ylabel='Temperature ({}C)'.format(u'\N{DEGREE SIGN}'),
           yticks=np.arange(temp_min + 1, temp_max, 2))

axs[2].set(ylim=[-3, 4], yticks=np.arange(-3, 4, 1))

fig, ax = plt.subplots()
ax.plot(psu_1208.age_ka, psu_1208.temp, color='green', linestyle='-', alpha=0.5)
ax.fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_add1, alpha=0.05, facecolor='green')
# axs[0].fill_between(psu_1208.age_ka, psu_1208.temp_min2, psu_1208.temp_add2, alpha=0.05, facecolor='green')

ax.plot(psu_1209.age_ka, psu_1209.temp, color='red', linestyle='-', alpha=0.5)
ax.fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_add1, alpha=0.05, facecolor='red')
# axs[1].fill_between(psu_1209.age_ka, psu_1209.temp_min2, psu_1209.temp_add2, alpha=0.05, facecolor='red')



plt.show()
