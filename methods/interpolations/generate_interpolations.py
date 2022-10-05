import numpy as np
import scipy.interpolate as interpol


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
