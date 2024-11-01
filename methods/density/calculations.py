import matplotlib.pyplot as plt

from objects.misc.sea_level import sea_level

'''
Full Inverse Salinity

S_t = S_0 + DS_t
DS_t = Dd18Osw_t * m
d18Osw_t = d18Osw_0 + Dd18Osw_t
d18Osw_t = d18Osw_orig - d18Osw_iv

'''






def age_d18o_correction(d18o_sw: float, age: float) -> float:
    """
    Calculates the offset d18O_sw based on the global sea level change in d18O_sw from Rohling et al., 2021.
    :param d18o_sw: Current d18O_sw
    :param age: Age of the measurement
    :return: Adjusted d18O_sw
    """
    # The sea level database stores ages as floats to the nearest 1 ka.
    age_round = round(age)
    # Find the associated d18O change on the sea level expected for that age.
    age_info = sea_level.loc[sea_level.age_ka == age_round]
    return d18o_sw - age_info.d18Ow_IV


def salinity_calculation_np(d18o: float) -> float:
    """
    Calculates salinity from seawater d18O values. From LeGrande and Schmidt, 2006, for the North Pacific where
    local d18O_sw == 0.44 * Salinity - 15.13;
    :param d18o: the d18O of seawater value
    :return: a salinity value in psu
    """
    m = 1.0 / 0.44
    salinity = m * (d18o + 15.13)
    return salinity


def inverse_age_d18o_correction(salinity: float, age: float) -> float:
    """
    Calculates the actual d18O_sw based on the global sea level change in d18O_sw from Rohling et al., 2021.
    :param salinity: Adjusted d18O_sw
    :param age: Age of the measurement
    :return: Correct d18O_sw
    """
    # The sea level database stores ages as floats to the nearest 1 ka.
    age_round = round(age)
    # Find the associated d18O change on the sea level expected for that age.
    age_info = sea_level.loc[sea_level.age_ka == age_round]
    add_salinity = age_info.d18Ow_IV * 1.1
    return salinity + add_salinity


def sea_level_salinity_change(age:float) -> float:
    # The sea level database stores ages as floats to the nearest 1 ka.
    age_round = round(age)
    # Find the associated change in the sea level expected for that age.
    age_info = sea_level.loc[sea_level.age_ka == age_round]
    # Convert this to a salinity
    rsl = age_info.SL_m.values[0]
    add_salinity = (rsl/3682) * -34.7
    return add_salinity


def full_inverse_salinity(d18o: float, age: float, d18O_sw_modern: float, salinity_modern: float) -> float:
    adjusted_d18_o = age_d18o_correction(d18o, age)
    # Calculates the difference in d18O_sw from this point in time and the modern.
    delta_d18O_sw = adjusted_d18_o - d18O_sw_modern
    # Calculates salinity change from seawater d18O values. From LeGrande and Schmidt, 2006, for the North Pacific where
    # local d18O_sw == 0.44 * Salinity - 15.13;
    delta_salinity = delta_d18O_sw * (1/0.44)
    # Calculates the final salinity from this point in time by adding the change to the modern.
    delta_salinity = delta_salinity + sea_level_salinity_change(age)
    salinity_final = salinity_modern + delta_salinity
    return salinity_final


def bespoke_inverse_salinity(d18O_sw: float, d18O_ivc: float, d18O_sw_modern: float, salinity_modern: float, rsl: float) -> float:
    adjusted_d18o_sw = d18O_sw - d18O_ivc
    delta_d18O_sw = adjusted_d18o_sw - d18O_sw_modern
    delta_salinity = delta_d18O_sw * (1 / 0.44)
    delta_salinity = delta_salinity + ((rsl/3682) * 34.7)
    salinity_final = salinity_modern + delta_salinity
    return salinity_final

