from pandas import DataFrame
from numpy import arange


def binning_multiple_series(
        *data_series: DataFrame,
        names: list[str] = None,
        start: int = 2400,
        end: int = 3600,
        fs: float = 5.0,
        value: str = "d18O_unadj",) -> DataFrame:
    # -------------- CHECK INPUTS --------------
    if len(names) != len(data_series):
        raise ValueError("There must be the same number of names as there are data series supplied to this function")

    # -------------- INITIALISE ARRAY ----------------
    # Define the age array
    age_array = arange(start, end, fs)
    # Interp space
    gap = fs/2

    # ------------ CLEAN INPUTS ---------------------
    # Drop any N/A values and duplicate values and sort the dataset in ascending order
    for data_serie in data_series:
        data_serie = data_serie.dropna(subset=[value, "age_ka"])
        data_serie = data_serie.sort_values(by="age_ka")
        data_serie = data_serie.drop_duplicates(subset='age_ka')

    # ------------ OBTAIN VALUES ------------------
    raw_values = []
    for age in age_array:
        series_values = {"age_ka": age}
        for i in range(len(names)):
            value_avg = data_series[i][data_series[i].age_ka.between(age-gap, age+gap)][value].mean()
            name = f'{value}_mean_{names[i]}'
            series_values[name] = value_avg
        raw_values.append(series_values)

    return DataFrame.from_records(raw_values)