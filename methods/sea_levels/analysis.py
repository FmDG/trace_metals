from methods.interpolations.binning_records import binning_multiple_series
from methods.interpolations.filter_data import filter_difference
from objects.core_data.isotopes import iso_1209, iso_1208


resampling_freq = 3.0  # Resampling frequency in ka
age_min, age_max = 2350, 3600  # Minimum and maximum ages in ka
resampled_data = binning_multiple_series(
    iso_1208, iso_1209,
    names=["1208", "1209"],
    fs=resampling_freq,
    start=age_min,
    end=age_max
).dropna()
# Filter the difference in d18O
filtered_1208, filtered_1209 = filter_difference(resampled_data, 5)

