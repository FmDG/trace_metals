from objects.misc.sea_level import sea_level


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
    return d18o_sw - age_info.Dd18O_ice


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
    add_salinity = age_info.Dd18O_ice * 1.1
    return salinity + add_salinity


def full_inverse_salinity(d18o: float, age: float) -> float:
    adjusted_d18_o = age_d18o_correction(d18o, age)
    salinity_calc = salinity_calculation_np(adjusted_d18_o)
    salinity_final = inverse_age_d18o_correction(salinity_calc, age)
    return salinity_final
