from pandas import DataFrame

from methods.interpolations.low_pass_filter import butter_lowpass_filter


def filter_difference(resampled_data: DataFrame, filter_period: float = 10.0):
    # --------------- RESAMPLE ISOTOPE DATA ---------------
    resampled_1209 = resampled_data.d18O_unadj_mean_1209.to_numpy()
    resampled_1208 = resampled_data.d18O_unadj_mean_1208.to_numpy()

    # --------------- FILTER PARAMETERS ---------------
    fs = 2  # Sample rate, in ka
    cutoff = 1.0 / filter_period  # Desired cutoff frequency of the filter, in 1\ka
    nyq = 0.5 * fs  # Nyquist Frequency
    order = 2  # Order of the filter

    # --------------- FILTER DATA ---------------
    filtered_1209 = butter_lowpass_filter(resampled_1209, cutoff, fs, order, nyq)
    filtered_1208 = butter_lowpass_filter(resampled_1208, cutoff, fs, order, nyq)
    return filtered_1208, filtered_1209
