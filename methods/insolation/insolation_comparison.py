import numpy as np
from pandas import DataFrame
from climlab.solar.insolation import daily_insolation
from climlab.solar.orbital import OrbitalTable


def generate_solstice_insolation_record(age_min: float, age_max: float, latitude: float, summer: bool = True):
    age_ka = np.arange((age_max * -1), (age_min * -1))
    orb = OrbitalTable.interp(kyear=age_ka)
    if summer:
        q_orb = daily_insolation(lat=latitude, day=172, orb=orb)
    else:
        q_orb = daily_insolation(lat=latitude, day=355, orb=orb)
    age_ka = age_ka * -1
    insolation = q_orb[::-1]
    return age_ka, insolation


def generate_insolation_frame(age_min: float, age_max: float, latitude: float):
    age_ka, insol = generate_solstice_insolation_record(age_min, age_max, latitude, summer=True)
    _, insol_eq = generate_solstice_insolation_record(age_min, age_max, 0, summer=True)
    _, insol_winter = generate_solstice_insolation_record(age_min, age_max, latitude, summer=True)
    _, insol_winter_eq = generate_solstice_insolation_record(age_min, age_max, 0, summer=True)
    return DataFrame({"age_ka": age_ka, "summer_insolation": insol, "summer_gradient": (insol - insol_eq),
                      "winter_insolation": insol_winter, "winter_gradient": (insol_winter - insol_winter_eq)})
