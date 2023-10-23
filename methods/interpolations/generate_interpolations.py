import numpy as np
import scipy.interpolate as interpol
from pandas import DataFrame


# Make an array with a spacing of 5 ka, starting at a known start point
# For each point in the array, find the mean of all the points that are within ± 2.5 ka.
# Result

def generate_interpolation(data_series, fs=1.0, start=2400, end=3400, pchip=False, value="d18O_unadj"):
    # Define the age array
    age_array = np.arange(start, end, fs)
    # Drop any N/A values
    data_series = data_series.dropna(subset=[value, "age_ka"])

    # Drop any duplicate values and sort the dataset in ascending order
    data_series = data_series.sort_values(by="age_ka")
    data_series = data_series.drop_duplicates(subset='age_ka')

    if pchip:
        # Interpolate across the dataset using the pChip interpolator
        interpolated_dataset = interpol.pchip_interpolate(xi=data_series.age_ka, yi=data_series[value], x=age_array)
    else:
        function_int = interpol.interp1d(x=data_series.age_ka, y=data_series[value], fill_value="extrapolate")
        # Interpolate across this age array
        interpolated_dataset = function_int(age_array)

    return interpolated_dataset, age_array


def resampling(
        data_series: DataFrame,
        start: int = 2400,
        end: int = 3600,
        fs: float = 5.0,
        value: str = "d18O_unadj") -> tuple[np.ndarray, list[float]]:
    """
    Resamples a dataset at a given time resolution
    :param data_series: input pandas series
    :param start: start age
    :param end: end age
    :param fs: time step
    :param value: input value
    :return: tuple(age_array, list of values)
    """
    # -------------- INITIALISE ARRAY ----------------
    # Define the age array
    age_array = np.arange(start, end, fs)
    # Interp space
    gap = fs/2

    # ------------ CLEAN INPUTS ---------------------
    # Drop any N/A values and duplicate values and sort the dataset in ascending order
    data_series = data_series.dropna(subset=[value, "age_ka"])
    data_series = data_series.sort_values(by="age_ka")
    data_series = data_series.drop_duplicates(subset='age_ka')

    # ------------ OBTAIN VALUES ------------------
    d18O_values = []
    for age in age_array:
        d18O_avg = data_series[data_series.age_ka.between(age-gap, age+gap)][value].mean()
        d18O_values.append(d18O_avg)

    return age_array, d18O_values
