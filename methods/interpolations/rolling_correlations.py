from pandas import DataFrame

from methods.interpolations.binning_records import binning_multiple_series
from objects.core_data.isotopes import iso_1208, iso_1209


def rolling_correlation(window_size: int = 20, frequency: float = 5.0):
    # Bin the records at frequency above
    joint_records = binning_multiple_series(iso_1209, iso_1208, names=["1209", "1208"], start=2350, end=3600,
                                            fs=frequency, value="d18O_unadj").dropna()
    # Compute the difference in the mean d18O values
    joint_records["difference_d18O"] = joint_records.d18O_unadj_mean_1208 - joint_records.d18O_unadj_mean_1209

    correlations_1208 = joint_records.difference_d18O.rolling(window_size).corr(
        other=joint_records.d18O_unadj_mean_1208)
    correlations_1209 = joint_records.difference_d18O.rolling(window_size).corr(
        other=joint_records.d18O_unadj_mean_1209)
    entrants = {"max_age": joint_records.age_ka.rolling(window_size).max(),
                "min_age": joint_records.age_ka.rolling(window_size).min(),
                "med_age": joint_records.age_ka.rolling(window_size).median(),
                "corr_1208_diff": correlations_1208,
                "corr_1209_diff": correlations_1209
                }
    return DataFrame(entrants)
