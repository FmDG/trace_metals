from methods.interpolations.binning_records import binning_multiple_series
from methods.interpolations.filter_data import filter_difference
from objects.core_data.isotopes import iso_1209, iso_1208
from objects.core_data.alkenones import sst_846, sst_1208
from objects.misc.sea_level import sea_level
from objects.misc.mis_boundaries import mis_boundaries
from methods.interpolations.rolling_pearson import rolling_spearman, rolling_pearson
from pandas import DataFrame


## ------------- GENERATE DIFFERENCES  -------------
resampling_freq = 2  # Resampling frequency in ka
age_min, age_max = 2200, 3600  # Minimum and maximum ages in ka
resampled_data = binning_multiple_series(
    iso_1208, iso_1209,
    names=["1208", "1209"],
    fs=resampling_freq,
    start=age_min,
    end=age_max
).dropna()
# Filter the difference in d18O
filtered_1208, filtered_1209 = filter_difference(resampled_data, 5)
resampled_data["filtered_difference"] = (filtered_1208 - filtered_1209).tolist()
resampled_data["difference_d18O"] = resampled_data.d18O_unadj_mean_1208 - resampled_data.d18O_unadj_mean_1209


## ------------- GENERATE DIFFERENCES AND LOOK AT CORRELATIONS WITH SEA LEVEL CURVES -------------
sea_level_d18 = sea_level.rename(columns={"SL_m": "d18O_unadj"})
correlate_data = binning_multiple_series(
    iso_1208, iso_1209, sea_level_d18,
    names=["1208", "1209", "sea_level"],
    fs=resampling_freq,
    start=age_min,
    end=age_max
).dropna()
correlate_data["difference_d18O"] = correlate_data.d18O_unadj_mean_1208 - correlate_data.d18O_unadj_mean_1209
rolling_corr_spear = rolling_spearman(correlate_data, "difference_d18O", "d18O_unadj_mean_sea_level",
                                      window=100, start=2400, end=3400)
rolling_corr_pears = rolling_pearson(correlate_data, "difference_d18O", "d18O_unadj_mean_sea_level",
                                     window=100, start=2400, end=3400)

## ------------- RESAMPLE AND LOOK AT DIFFERENCES IN SST RECORDS -------------
resampled_SST = binning_multiple_series(
    sst_846, sst_1208,
    names=["846", "1208"],
    start=age_min,
    end=age_max,
    value="SST",
    fs=resampling_freq
).dropna()
resampled_SST["difference_SST"] = resampled_SST.SST_mean_846 - resampled_SST.SST_mean_1208

resampled_SST['glacial'] = False
for _, row in mis_boundaries.iterrows():
    lower_age = row["age_start"]
    upper_age = row['age_end']
    if row["glacial"] == "glacial":
        resampled_SST.loc[(resampled_SST.age_ka >= lower_age) & (resampled_SST.age_ka < upper_age), 'glacial'] = True

SST_glacials = resampled_SST.loc[resampled_SST.glacial]
SST_interglacials = resampled_SST.loc[~resampled_SST.glacial]

sst_post = resampled_SST[resampled_SST.age_ka.between(2490, 2730)].difference_SST
sst_pre = resampled_SST[resampled_SST.age_ka.between(2730, 2900)].difference_SST

sst_glacial_post = SST_glacials[SST_glacials.age_ka.between(2490, 2730)].difference_SST
sst_glacial_pre = SST_glacials[SST_glacials.age_ka.between(2730, 2900)].difference_SST

sst_interglacial_post = SST_interglacials[SST_interglacials.age_ka.between(2490, 2730)].difference_SST
sst_interglacial_pre = SST_interglacials[SST_interglacials.age_ka.between(2730, 2900)].difference_SST

sst_gradients = {
    "sst_grad_1": [sst_post.mean(), sst_post.std()],
    "sst_grad_2": [sst_pre.mean(), sst_pre.std()],
    "glacial_sst_grad_1": [sst_glacial_post.mean(), sst_glacial_post.std()],
    "glacial_sst_grad_2": [sst_glacial_pre.mean(), sst_glacial_pre.std()],
    "interglacial_sst_grad_1": [sst_interglacial_post.mean(), sst_interglacial_post.std()],
    "interglacial_sst_grad_2": [sst_interglacial_pre.mean(), sst_interglacial_pre.std()]
}


## ------------- GENERATE DIFFERENCES ACCORDING TO GLACIALS OR INTERGLACIALS -------------
input_raw_values_glacials = []
input_raw_values_interglacials = []
for _, row in mis_boundaries.iterrows():
    value_1208 = iso_1208[iso_1208.age_ka.between(row["age_start"], row["age_end"])].d18O_unadj.mean()
    value_1209 = iso_1209[iso_1209.age_ka.between(row["age_start"], row["age_end"])].d18O_unadj.mean()
    glacial = (row["glacial"] == "glacial")
    mid_point = ((row["age_start"] + row["age_end"]) / 2) - 3
    value = {"age_ka": mid_point, "value_1208": value_1208, "value_1209": value_1209}
    if row["glacial"] == "glacial":
        input_raw_values_glacials.append(value)
    else:
        input_raw_values_interglacials.append(value)

glacial_means = DataFrame.from_records(input_raw_values_glacials)
interglacial_means = DataFrame.from_records(input_raw_values_interglacials)


## ------------- COMPARE DIFFERENCES IN SST AND d18O -------------

input_01 = resampled_SST.rename(columns={'difference_SST': 'values'})
input_02 = resampled_data.rename(columns={'difference_d18O': 'values'})

resampled_SST_d18O = binning_multiple_series(
    input_01, input_02,
    names=["SST", "Dd18O"],
    start=age_min,
    end=age_max,
    value="values",
    fs=resampling_freq
).dropna()



rolling_corr_SST_d18O = rolling_pearson(resampled_SST_d18O, "values_mean_Dd18O", "values_mean_SST",
                                     window=100, start=2500, end=3300)