import os

import pandas as pd
import scipy.interpolate as interpol
import numpy as np
import matplotlib.pyplot as plt


def interpolate_isotopes():
    site_1208 = pd.read_csv('data/cores/1208_cibs.csv')
    site_1209 = pd.read_csv('data/cores/1209_cibs.csv')

    site_1208 = site_1208.dropna(subset=["d18O_unadj"])
    site_1209 = site_1209.dropna(subset=["d18O_unadj"])

    # We can use two different interpolation techniques - the first is a simple 1D interpolation, the second is a
    # PChip interpolation

    function_1208 = interpol.interp1d(x=site_1208.age_ka, y=site_1208.d18O_unadj, fill_value="extrapolate")
    function_1209 = interpol.interp1d(x=site_1209.age_ka, y=site_1209.d18O_unadj, fill_value="extrapolate")

    # Age array
    start = 2400
    stop = 3600
    age_array = np.arange(start, stop, 1)

    # Interpolate across this age array
    interpolated_1208 = function_1208(age_array)
    interpolated_1209 = function_1209(age_array)

    fig, axs = plt.subplots(2, sharex="all")
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)

    axs[0].plot(site_1208.age_ka, site_1208.d18O_unadj, label="ODP 1208")
    axs[0].plot(site_1209.age_ka, site_1209.d18O_unadj, label="ODP 1209")
    axs[0].set(ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[0].invert_yaxis()
    axs[0].spines['right'].set_visible(False)
    axs[0].spines['top'].set_visible(False)
    axs[0].spines['bottom'].set_visible(False)
    axs[0].legend()

    axs[1].plot(age_array, (interpolated_1208 - interpolated_1209), label="Difference", c='k')
    axs[1].set(xlabel="Age (ka)", ylabel="Difference in {} ({})".format(r'$\delta^{18}$O', u"\u2030"), xlim=[start, stop], ylim=[-1.0, 0.5])
    # axs[1].axhline(0, ls='--', color='m')
    axs[1].fill_between(age_array, -0.12, 0.12, color='m', alpha=0.2, label=r'$\pm 2 \sigma$')
    axs[1].fill_between(age_array, -0.24, 0.24, color='m', alpha=0.1, label=r'$\pm 6 \sigma$')

    # Fill between regions where d18O goes higher than 2.9 per mil

    axs[1].invert_yaxis()
    axs[1].legend()
    axs[1].yaxis.set(ticks_position="right", label_position='right')
    axs[1].spines['left'].set_visible(False)
    axs[1].spines['top'].set_visible(False)

    plt.show()


if __name__ == "__main__":
    os.chdir('../..')
    interpolate_isotopes()
