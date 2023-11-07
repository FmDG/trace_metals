from numpy import arange
from pandas import DataFrame
from scipy.stats import pearsonr


def rolling_pearson(database: DataFrame, value_01: str, value_02: str, start: int = 2300, end: int = 3600,
                    window: int = 100) -> DataFrame:
    """
    Calculate rolling Pearson correlation coefficients between two variables within a specified age interval.

    Parameters:
    - database (pandas.DataFrame): The DataFrame containing the data.
    - value_01 (str): The name of the first variable to calculate correlation for.
    - value_02 (str): The name of the second variable to calculate correlation for.
    - start (int, optional): The starting age of the age interval (default: 2300).
    - end (int, optional): The ending age of the age interval (default: 3600).
    - window (float, optional): The size of the rolling window for age intervals (default: 100).

    Returns:
    - pandas.DataFrame: A DataFrame with columns 'age_ka', 'age_min', 'age_max', 'r', and 'p' representing the age
      point, lower age limit, upper age limit, Pearson correlation coefficient, and p-value, respectively.

    Raises:
    - ValueError: If the specified window size is greater than the age interval.

    This function calculates Pearson correlation coefficients (r) and p-values (p) for the given two variables
    ('value_01' and 'value_02') in a rolling fashion, where the age interval moves with a specified window size.
    It returns a DataFrame with the calculated values for each age interval.

    The 'start' and 'end' parameters determine the age range over which the correlation is calculated, and the
    'window' parameter defines the width of the rolling window. If 'window' is set to a value larger than the
    difference between 'end' and 'start', a ValueError is raised.

    The resulting DataFrame contains columns 'age_ka' for the center of each age interval, 'age_min' and 'age_max' for
    the lower and upper limits of the age interval, 'r' for the Pearson correlation coefficient, and 'p' for the
    associated p-value.
    """
    # -------------- CHECK ERRORS --------------
    if window > (end - start):
        raise ValueError("Window size is greater than age interval")
    # -------------- INITIALISE ARRAY ----------------
    # Define the age array
    gap = window/2
    age_array = arange((start + gap - 1), (end - gap + 1), 1)

    # ------------ OBTAIN VALUES ------------------
    raw_values = []
    for age in age_array:
        sampling = database[database.age_ka.between(age - gap, age + gap)]
        r, p = pearsonr(sampling[value_01], sampling[value_02])
        series_values = {"age_ka": age, "age_min": (age - gap), "age_max": (age + gap), "r": r, "p": p}
        raw_values.append(series_values)

    return DataFrame.from_records(raw_values)
