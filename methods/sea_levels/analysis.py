from methods.interpolations.binning_records import binning_multiple_series
from methods.interpolations.rolling_pearson import rolling_pearson
from methods.interpolations.filter_data import filter_difference
from objects.core_data.isotopes import iso_1209, iso_1208
from objects.misc.sea_level import sea_level


resampling_freq = 3.0  # Resampling frequency in ka
age_min, age_max = 2350, 3600  # Minimum and maximum ages in ka
sea_level_d18 = sea_level.rename(columns={"SL_m": "d18O_unadj"})
resampled_data = binning_multiple_series(
    iso_1208, iso_1209, sea_level_d18,
    names=["1208", "1209", "sea_level"],
    fs=resampling_freq,
    start=age_min,
    end=age_max
).dropna()
# Filter the difference in d18O
filtered_1208, filtered_1209 = filter_difference(resampled_data, 5)

resampled_data["difference_d18O"] = resampled_data.d18O_unadj_mean_1208 - resampled_data.d18O_unadj_mean_1209
rolling_corr = rolling_pearson(resampled_data, "difference_d18O", "d18O_unadj_mean_sea_level", start=age_min, end=age_max)
