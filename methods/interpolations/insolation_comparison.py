import matplotlib.pyplot as plt
import numpy as np
from climlab import constants as const
from climlab.solar.insolation import daily_insolation
from climlab.solar.orbital import OrbitalTable

from methods.figures.tick_dirs import tick_dirs
from methods.interpolations.binning_records import binning_multiple_series
from methods.interpolations.filter_data import filter_difference
from objects.core_data.isotopes import iso_1208, iso_1209


def generate_solstice_insolation_record(age_min: float, age_max: float, latitude: float):
    age_ka = np.arange((age_max * -1), (age_min * -1))
    orb = OrbitalTable.interp(kyear=age_ka)
    lat = np.linspace(-90, 90, 181)
    days = np.linspace(1., 50.) / 50 * const.days_per_year
    q_orb = daily_insolation(lat, days, orb)
    age_ka = age_ka * -1
    insolation = q_orb[(90 + latitude), 23, :]
    insolation = insolation[::-1]
    return age_ka, insolation


def generate_ann_mean_insolation_record(age_min: float, age_max: float, latitude: float):
    age_ka = np.arange((age_max * -1), (age_min * -1))
    orb = OrbitalTable.interp(kyear=age_ka)
    lat = np.linspace(-90, 90, 181)
    days = np.linspace(1., 50.) / 50 * const.days_per_year
    q_orb = daily_insolation(lat, days, orb)
    q_annual = np.mean(q_orb, axis=1)  # time average over the year
    age_ka = age_ka * -1
    insolation = q_annual[(90 + latitude), :]
    insolation = insolation[::-1]
    return age_ka, insolation


def insolation_comparison(age_min: float, age_max: float):
    # --------------- GENERATE DIFFERENCES ---------------
    resampling_freq = 5.0  # Resampling frequency in ka
    filter_period = 3.0
    resampled_data = binning_multiple_series(
        iso_1208, iso_1209,
        names=["1208", "1209"],
        fs=resampling_freq,
        start=int(age_min),
        end=int(age_max)
    ).dropna()
    # Filter the difference in d18O
    filtered_1208, filtered_1209 = filter_difference(resampled_data, filter_period)
    resampled_data["difference_d18O"] = resampled_data.d18O_unadj_mean_1208 - resampled_data.d18O_unadj_mean_1209

    fig, axs = plt.subplots(
        nrows=4,
        figsize=(12, 8),
        sharex="all",
    )
    fig.subplots_adjust(hspace=0)

    latitude = 65
    age_ka, insol = generate_solstice_insolation_record(age_min, age_max, latitude)
    _, insol_eq = generate_solstice_insolation_record(age_min, age_max, 0)

    axs[0].plot(age_ka, insol)
    axs[0].set(ylabel='Summer solstice insolation at {}{}N\n({})'.format(latitude, r'$\degree$', r'W m$^{-1}$'))

    axs[1].plot(age_ka, (insol - insol_eq))
    axs[1].set(
        ylabel='Summer solstice insolation gradient ({}{}N - 0{})\n({})'.format(latitude, r'$\degree$', r'$\degree$',
                                                                                r'W m$^{-1}$'))

    axs[2].plot(iso_1208.age_ka, iso_1208.d18O_unadj, label="1208")
    axs[2].plot(iso_1209.age_ka, iso_1209.d18O_unadj, label="1209")
    axs[2].set(ylabel="{} ({})".format(r'$\delta^{18}$O', u'\u2030'))
    axs[2].invert_yaxis()
    axs[2].legend(frameon=False)

    axs[3].plot(resampled_data.age_ka, (filtered_1208 - filtered_1209))  # Plot the filtered difference
    axs[3].set(ylabel="{}-ka filtered {} ({})".format(filter_period, r'$\Delta \delta^{18}$O', u'\u2030'),
               xlabel="Age (ka)", xlim=[age_min, age_max])
    axs[3].invert_yaxis()

    tick_dirs(axs, 4, int(age_min), int(age_max), False)

    plt.show()


if __name__ == "__main__":
    insolation_comparison(age_min=2350, age_max=3600)
