from pandas import DataFrame

from methods.interpolations.binning_records import binning_multiple_series, binning_frame
from methods.interpolations.filter_data import filter_difference
from methods.interpolations.rolling_pearson import rolling_pearson
from objects.core_data.isotopes import iso_1208, iso_1209
from insolation_comparison import generate_insolation_frame


def insol_correlation(insol_frame: DataFrame, resampled_data: DataFrame, age_min: int = 2350, age_max: int = 3600,
                      resampling_freq: float = 5.0) -> DataFrame:
    # --------------- RESAMPLE INSOLATION ---------------
    resampled_insol = binning_frame(insol_frame, age_min, age_max, resampling_freq, "solstice_insolation")

    # COMBINE INTO ONE DATAFRAME AND THEN DROP ALL THE NANS
    combined_frame = resampled_insol.merge(resampled_data, on="age_ka")
    combined_frame = combined_frame.dropna(subset=["difference_d18O", "solstice_insolation"], how="any")

    # --------------- ROLLING CORRELATIONS ---------------
    return rolling_pearson(combined_frame, "difference_d18O", "solstice_insolation", age_min, age_max, window=100)
