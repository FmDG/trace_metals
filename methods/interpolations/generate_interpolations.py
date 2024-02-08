import numpy as np
import pandas as pd
import scipy.interpolate as interpol
from pandas import DataFrame
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

from objects.core_data.isotopes import iso_1208, iso_1209


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
        value: str = "d18O_unadj") -> pd.DataFrame:
    """
    Resamples a dataset at a given time resolution.

    Args:
        data_series (DataFrame): Input pandas DataFrame containing age and value data.
        start (int, optional): Start age for resampling. Default is 2400.
        end (int, optional): End age for resampling. Default is 3600.
        fs (float, optional): Time step for resampling. Default is 5.0.
        value (str, optional): Name of the value column to be resampled. Default is "d18O_unadj".

    Returns:
        Tuple[np.ndarray, List[float]]: A tuple containing two elements:
            - age_array (np.ndarray): An array of ages at which resampling was performed.
            - d18O_values (List[float]): A list of resampled values corresponding to the ages in age_array.

    The function resamples the input dataset at the specified time resolution, generating an age array and a list
    of resampled values. It drops N/A values, removes duplicates, and sorts the dataset by age before resampling.

    Note:
        This function assumes that the input DataFrame `data_series` contains columns 'age_ka' and `value`.

    Examples:
        >>> import pandas as pd
        >>> import numpy as np
        >>> data = pd.DataFrame({'age_ka': [2400, 2500, 2600, 2700, 2800], 'temperature': [1.1, 1.2, 1.3, 1.4, 1.5]})
        >>> resampled_data = resampling(data, start=2400, end=2800, fs=100, value='temperature')
    """
    # -------------- INITIALISE ARRAY ----------------
    # Define the age array
    age_array = np.arange(start, end, fs)
    # Interp space
    gap = fs / 2

    # ------------ CLEAN INPUTS ---------------------
    # Drop any N/A values and duplicate values and sort the dataset in ascending order
    data_series = data_series.dropna(subset=[value, "age_ka"])
    data_series = data_series.sort_values(by="age_ka")
    data_series = data_series.drop_duplicates(subset='age_ka')

    # ------------ OBTAIN VALUES ------------------
    raw_values = []
    for age in age_array:
        value_avg = data_series[data_series.age_ka.between(age - gap, age + gap)][value].mean()
        raw_values.append({"age_ka": age, "value_avg": value_avg})

    return DataFrame.from_records(raw_values)


def resample_both(fs: float = 5.0, min_age: int = 2300, max_age: int = 3700, value: str = "d18O_unadj") -> pd.DataFrame:
    """
     Resamples two datasets and calculates the difference between them at regular age intervals.

    Args:
        fs (float, optional): Time step for resampling. Default is 5.0.
        min_age (int, optional): Minimum age for resampling. Default is 2300.
        max_age (int, optional): Maximum age for resampling. Default is 3700.
        value (string, optional): Value in the dataframe to resample. Default is 'd18O_uandj'

    Returns:
        pd.DataFrame: A pandas DataFrame containing resampled age values, d18O_1208, d18O_1209, and d18O_difference.

    This function generates an age array at specified intervals and resamples two datasets, 'iso_1208' and 'iso_1209', at each age point.
    It calculates the difference between the corresponding 'd18O_unadj' values in both datasets and returns the results in a DataFrame.

    Note:
        - The 'iso_1208' and 'iso_1209' DataFrames are assumed to be available in the global scope.
        - The function relies on the 'age_ka' and 'd18O_unadj' columns in the input DataFrames.

    Example:
        >>> resampled_data = resample_both(fs=10, min_age=2400, max_age=3600)
        >>> print(resampled_data)
    """
    age_array = np.arange(min_age, max_age, fs)

    interpolated_values = []

    for age in age_array:
        avg_1208 = iso_1208[iso_1208.age_ka.between(age - (fs / 2), age + (fs / 2))][value].mean()
        avg_1209 = iso_1209[iso_1209.age_ka.between(age - (fs / 2), age + (fs / 2))][value].mean()
        difference = avg_1208 - avg_1209
        interpolated_values.append(
            {"age_ka": age, "d18O_1208": avg_1208, "d18O_1209": avg_1209, "d18O_difference": difference})

    return DataFrame.from_records(interpolated_values)


def linear_regression(dataset: pd.DataFrame, value_1: str = "d13C", value_2: str = "BCa"):
    """
    Perform linear regression analysis on two variables within a given dataset.

    Parameters:
    - dataset (pd.DataFrame): The Pandas DataFrame containing the data for linear regression analysis.
    - value_1 (str): The name of the independent variable for the regression analysis. Default is 'd13C'.
    - value_2 (str): The name of the dependent variable for the regression analysis. Default is 'BCa'.

    Returns:
    - new_x (np.ndarray): The array of independent variable values for the regression line.
    - new_y (np.ndarray): The array of predicted dependent variable values for the regression line.
    - m (np.ndarray): The slope of the regression line.
    - c (float): The y-intercept of the regression line.
    - r_sq (float): The coefficient of determination (R-squared) for the regression analysis.

    The function performs linear regression analysis on the specified variables ('value_1' and 'value_2') within the
    provided dataset. It returns the arrays of new x and y values for the regression line, as well as the slope ('m'),
    y-intercept ('c'), and coefficient of determination ('r_sq').

    The default variables for regression are 'd13C' as the independent variable and 'BCa' as the dependent variable.

    Usage:
    new_x, new_y, slope, intercept, r_squared = linear_regression(dataset, 'variable1', 'variable2')
    """
    old_x = dataset[value_1].to_numpy().reshape(-1, 1)
    old_y = dataset[value_2].to_numpy().reshape(-1, 1)
    new_x = np.linspace(dataset[value_1].min(), dataset[value_1].max(), num=100).reshape(-1, 1)
    model = LinearRegression().fit(old_x, old_y)
    new_y = model.predict(new_x)
    m, c = model.coef_, model.intercept_
    r_sq = model.score(old_x, old_y)
    return new_x, new_y, m, c, r_sq


def linear_relations(ax: plt.axis, dataset: pd.DataFrame, value_1: str, value_2: str, age_cutoff: bool = False):
    """
    Plot linear regression lines between two variables from a given dataset.

    Parameters:
    - ax (matplotlib.axis.Axis): The matplotlib axis where the plot will be drawn.
    - dataset (pd.DataFrame): The Pandas DataFrame containing the data for analysis.
    - value_1 (str): The name of the independent variable for the regression analysis.
    - value_2 (str): The name of the dependent variable for the regression analysis.
    - age_cutoff (bool): If True, perform separate linear regressions for data above and below a specified age threshold.
                        Default is False.

    Returns:
    - ax (matplotlib.axis.Axis): The updated matplotlib axis with linear regression lines.

    The function performs linear regression analysis on the specified variables ('value_1' and 'value_2') within the
    provided dataset. It then plots the regression lines on the given axis ('ax').

    If 'age_cutoff' is True, the dataset is split into two frames based on an age threshold (3000 ka by default),
    and separate regression lines are plotted for each frame. If False, a single regression line is plotted for
    the entire dataset.

    The linear regression results, including the equation of the regression line and the coefficient of determination
    (R-squared), are displayed in the legend for each line.

    Usage:
    linear_relations(ax, dataset, 'variable1', 'variable2', age_cutoff=True)
    """
    if age_cutoff:
        threshold = 2700  # cut-off in ka
        frames = [dataset[dataset.age_ka < threshold], dataset[dataset.age_ka > threshold]]
    else:
        frames = [dataset]
    for frame in frames:
        x_new, y_new, m, c, r_sq = linear_regression(frame, value_1, value_2)
        ax.plot(x_new, y_new, label="y={:.2f}x + {:.2f} ({} = {:.2f})".format(m[0][0], c[0], r'$R^2$', r_sq))
    return ax
