import numpy as np
from pandas import DataFrame
from climlab import constants as const
from climlab.solar.insolation import daily_insolation
from climlab.solar.orbital import OrbitalTable


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


def generate_insolation_frame(age_min: float, age_max: float, latitude: float):
    age_ka, insol = generate_solstice_insolation_record(age_min, age_max, latitude)
    _, insol_ann = generate_ann_mean_insolation_record(age_min, age_max, latitude)
    _, insol_eq = generate_solstice_insolation_record(age_min, age_max, 0)
    return DataFrame({"age_ka": age_ka, "solstice_insolation": insol, "annual_insolation": insol_ann,
                      "solstice_insolation_gradient": (insol - insol_eq), "equatorial_insolation": insol_eq})
