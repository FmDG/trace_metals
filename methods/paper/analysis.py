from methods.interpolations.binning_records import binning_multiple_series
from methods.interpolations.filter_data import filter_difference
from objects.core_data.isotopes import iso_1209, iso_1208
from objects.core_data.alkenones import sst_846, sst_1208
from objects.misc.sea_level import sea_level
from methods.interpolations.rolling_pearson import rolling_spearman, rolling_pearson


resampling_freq = 3.0  # Resampling frequency in ka
age_min, age_max = 2350, 3450  # Minimum and maximum ages in ka
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
resampled_data["filtered_difference"] = (filtered_1208 - filtered_1209).tolist()
resampled_data["difference_d18O"] = resampled_data.d18O_unadj_mean_1208 - resampled_data.d18O_unadj_mean_1209
rolling_corr_spear = rolling_spearman(resampled_data, "difference_d18O", "d18O_unadj_mean_sea_level",
                                      window=100, start=age_min, end=age_max)
rolling_corr_pears = rolling_pearson(resampled_data, "difference_d18O", "d18O_unadj_mean_sea_level",
                                     window=100, start=age_min, end=age_max)


resampled_SST_1208 = binning_multiple_series(
    sst_846, sst_1208,
    names=["846", "1208"],
    start=age_min,
    end=age_max,
    value="SST",
    fs=2
).dropna()
resampled_SST_1208["difference_SST"] = resampled_SST_1208.SST_mean_846 - resampled_SST_1208.SST_mean_1208
sst_post = resampled_SST_1208[resampled_SST_1208.age_ka.between(2490, 2730)].difference_SST
sst_pre = resampled_SST_1208[resampled_SST_1208.age_ka.between(2730, 2900)].difference_SST

sst_gradients = {"sst_grad_1": [sst_post.mean(), sst_post.std()], "sst_grad_2": [sst_pre.mean(), sst_pre.std()]}

