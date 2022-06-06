import matplotlib.pyplot as plt
import pandas as pd


d18O_1209 = pd.read_csv("data/ODP1209_cibs.csv")
d18O_1208 = pd.read_csv("data/ODP1208_cibs.csv")

tm_1209 = pd.read_csv("data/1209_TraceMetals_rmv.csv")
tm_1208 = pd.read_csv("data/1208_TraceMetals.csv")


fig, axs = plt.subplots(3)

fig.suptitle("Comparison of {} and Mg/Ca trace metals".format(r'$\delta^{18}$O'))

axs[0].plot(d18O_1208.age_ka, d18O_1208.d13C, marker='+', color='b', label='ODP 1208')
axs[0].plot(d18O_1209.age_ka, d18O_1209.d13C, marker='+', color='r', label="ODP 1209")
axs[0].legend()
axs[0].set(xlim=[2550, 2800], ylabel=r'$\delta^{13}$C')

axs[1].plot(d18O_1208.age_ka, d18O_1208.d18Oadj, marker='+', color='b', label='ODP 1208')
axs[1].plot(d18O_1209.age_ka, d18O_1209.d18Oadj, marker='+', color='r', label="ODP 1209")
axs[1].legend()
axs[1].set(xlim=[2550, 2800], ylabel=r'$\delta^{18}$O')
axs[1].invert_yaxis()

axs[2].plot(tm_1208.age_ka, tm_1208.MgCa, marker='+', color='b', label="ODP 1208")
axs[2].plot(tm_1209.age_ka, tm_1209.MgCa, marker='+', color='r', label="ODP 1209")
axs[2].legend()
axs[2].set(xlim=[2550, 2800], xlabel="Age (ka)", ylabel="Mg/Ca")

plt.show()
