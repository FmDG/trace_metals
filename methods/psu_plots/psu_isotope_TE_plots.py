import matplotlib.pyplot as plt
import pandas as pd
import os

os.chdir("../..")

ox_1208 = pd.read_csv("data/ODP1208_cibs.csv")
ox_1209 = pd.read_csv("data/ODP1209_cibs.csv")

te_1208 = pd.read_csv("data/1208_TraceMetals.csv")
te_1209 = pd.read_csv("data/1209_TraceMetals.csv")

psu_1208 = pd.read_csv("data/PSU_Solver/PSU_data_1208.csv")
psu_1209 = pd.read_csv("data/PSU_Solver/PSU_data_1209.csv")

min_age, max_age = 2400, 3200
colour_1209, colour_1208 = "#F2545B", "#30C5FF"

fig, axs = plt.subplots(5, 1, sharex=True, figsize=(8.25, 11.75))
# Remove horizontal space between axes
fig.subplots_adjust(hspace=0)

fig.suptitle("Comparison of Sites 1208/09")

axs[0].plot(ox_1208.age_ka, ox_1208.d18Oadj, marker='+', color=colour_1208, label='ODP 1208')
axs[0].plot(ox_1209.age_ka, ox_1209.d18Oadj, marker='+', color=colour_1209, label="ODP 1209")
axs[0].legend(loc='upper left', shadow=False, frameon=False, bbox_to_anchor=(0.90, 1.12))
axs[0].set(xlim=[min_age, max_age], ylabel='{} ({})'.format(r'$\delta^{18}$O', u"\u2030"), xlabel='Age (ka)')
axs[0].invert_yaxis()
axs[0].spines['right'].set_visible(False)

axs[1].plot(te_1208.age_ka, te_1208.MgCa, marker='+', color=colour_1208, label="ODP 1208")
axs[1].plot(te_1209.age_ka, te_1209.MgCa, marker='+', color=colour_1209, label="ODP 1209")
axs[1].set(ylabel='{} ({})'.format('Mg/Ca', "mmol/mol"))
axs[1].yaxis.set(ticks_position="right", label_position='right')
axs[1].spines['left'].set_visible(False)

axs[2].plot(psu_1208.age_ka, psu_1208.temp, color=colour_1208, linestyle='-', alpha=1)
axs[2].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_add1, alpha=0.1, facecolor=colour_1208)
axs[2].plot(psu_1209.age_ka, psu_1209.temp, color=colour_1209, linestyle='-', alpha=1)
axs[2].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_add1, alpha=0.1, facecolor=colour_1209)
axs[2].set(ylabel='Modelled {} ({})'.format('Temperature', u'\N{DEGREE SIGN}C'))
axs[2].spines['right'].set_visible(False)

axs[3].plot(psu_1208.age_ka, psu_1208.d18O_sw, color=colour_1208, linestyle='-', alpha=1)
axs[3].fill_between(psu_1208.age_ka, psu_1208.d18O_sw_min1, psu_1208.d18O_sw_add_1, alpha=0.1, facecolor=colour_1208)
axs[3].plot(psu_1209.age_ka, psu_1209.d18O_sw, color=colour_1209, linestyle='-', alpha=1)
axs[3].fill_between(psu_1209.age_ka, psu_1209.d18O_sw_min1, psu_1209.d18O_sw_add_1, alpha=0.1, facecolor=colour_1209)
axs[3].set(ylabel='Modelled {} ({})'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))
axs[3].yaxis.set(ticks_position="right", label_position='right')
axs[3].spines['left'].set_visible(False)

# axs[4].plot(te_1208.age_ka, te_1208.BCa, marker='+', color=colour_1208, label="ODP 1208")
axs[4].plot(te_1209.age_ka, te_1209.Bca, marker='+', color=colour_1209, label="ODP 1209")
axs[4].set(ylabel='{} ({})'.format('B/Ca', r'$\mu$mol/mol'))
axs[4].yaxis.set(ticks_position="left", label_position='left')
axs[4].spines['right'].set_visible(False)


for ax in axs:
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

axs[4].spines['bottom'].set_visible(True)
axs[4].set(xlabel='Age (ka)', xlim=[min_age, max_age])

plt.savefig("Side_03.pdf", format="pdf")

# Comparison Plot of Temperature against d18O
fig, axs = plt.subplots(2, 1, sharex=True)
# Remove horizontal space between axes
fig.subplots_adjust(hspace=0)

fig.suptitle("Comparison of {} and Modelled Temperatures".format(r'$\delta^{18}$O'))

axs[0].plot(ox_1208.age_ka, ox_1208.d18Oadj, marker='+', color=colour_1208, label='ODP 1208')
axs[0].plot(ox_1209.age_ka, ox_1209.d18Oadj, marker='+', color=colour_1209, label="ODP 1209")
axs[0].legend(loc='upper left', shadow=False, frameon=False, bbox_to_anchor=(0.90, 1.05))
axs[0].set(ylabel='{} ({})'.format(r'$\delta^{18}$O', u"\u2030"), xlabel='Age (ka)')
axs[0].invert_yaxis()
axs[0].spines['right'].set_visible(False)


axs[1].plot(psu_1208.age_ka, psu_1208.temp, color=colour_1208, linestyle='-', alpha=1)
axs[1].fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_add1, alpha=0.1, facecolor=colour_1208)
axs[1].plot(psu_1209.age_ka, psu_1209.temp, color=colour_1209, linestyle='-', alpha=1)
axs[1].fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_add1, alpha=0.1, facecolor=colour_1209)
axs[1].set(ylabel='Modelled {} ({})'.format('Temperature', u'\N{DEGREE SIGN}C'))
axs[1].yaxis.set(ticks_position="right", label_position='right')
axs[1].spines['left'].set_visible(False)

for ax in axs:
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

axs[1].spines['bottom'].set_visible(True)
axs[1].set(xlabel='Age (ka)', xlim=[min_age, max_age])

plt.show()
