from scipy.signal import butter, filtfilt


def butter_lowpass_filter(data, cutoff, fs, order, nyq):
    """
    Apply a Butterworth low-pass filter to the input data.

    Parameters:
    - data (array-like): The input time-series data to be filtered.
    - cutoff (float): The cutoff frequency (in Hertz) of the low-pass filter.
    - fs (float): The sampling frequency (in Hertz) of the input data.
    - order (int): The order of the Butterworth filter.
    - nyq (float): The Nyquist frequency, which is half of the sampling frequency (fs / 2).

    Returns:
    - y (array-like): The filtered output data.

    The function computes a Butterworth low-pass filter with the specified 'cutoff' frequency, 'order', and 'fs'.
    It then applies this filter to the input data and returns the filtered output in 'y'.

    The 'nyq' parameter is calculated as half of the sampling frequency, and 'normal_cutoff' is the normalized
    cutoff frequency with respect to the Nyquist frequency.

    The 'butter' function from the scipy.signal library is used to obtain the filter coefficients 'b' and 'a'.
    Subsequently, the 'filtfilt' function is used to apply the filter to the input data, resulting in 'y'.

    This function is useful for smoothing and removing high-frequency noise from time-series data.

    Usage:
    filtered_data = butter_lowpass_filter(data, cutoff=5.0, fs=100.0, order=4, nyq=50.0)
    """
    normal_cutoff = (cutoff / nyq)
    # Get the filter coefficients
    b, a = butter(N=order, Wn=normal_cutoff, btype='low', analog=False, output='ba', fs=fs)
    y = filtfilt(b, a, data)
    return y
