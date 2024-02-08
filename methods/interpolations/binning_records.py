from numpy import arange
from pandas import DataFrame

from objects.core_data.isotopes import iso_1208, iso_1209


def binning_multiple_series(
        *data_series: DataFrame,
        names: list[str] = None,
        start: int = 2400,
        end: int = 3600,
        fs: float = 5.0,
        value: str = "d18O_unadj", ) -> DataFrame:
    # -------------- CHECK INPUTS --------------
    if len(names) != len(data_series):
        raise ValueError("There must be the same number of names as there are data series supplied to this function")

    # -------------- INITIALISE ARRAY ----------------
    # Define the age array
    age_array = arange(start, end, fs)
    # Interp space
    gap = fs / 2

    # ------------ CLEAN INPUTS ---------------------
    # Drop any N/A values and duplicate values and sort the dataset in ascending order
    for to_be_cleaned in data_series:
        to_be_cleaned = to_be_cleaned.dropna(subset=[value, "age_ka"])
        to_be_cleaned = to_be_cleaned.sort_values(by="age_ka")
        to_be_cleaned = to_be_cleaned.drop_duplicates(subset='age_ka')

    # ------------ OBTAIN VALUES ------------------
    raw_values = []
    for age in age_array:
        series_values = {"age_ka": age}
        for i in range(len(names)):
            value_avg = data_series[i][data_series[i].age_ka.between(age - gap, age + gap)][value].mean()
            name = f'{value}_mean_{names[i]}'
            series_values[name] = value_avg
        raw_values.append(series_values)

    return DataFrame.from_records(raw_values)


def binning_frame(database: DataFrame, age_min: int = 2300, age_max: int = 3600, freq: float = 5.0,
                  value: str = "d18O_unadj") -> DataFrame:
    age_array = arange(age_min, age_max, freq)  # Define the age array
    gap = freq / 2  # Interp space
    raw_values = []
    for age in age_array:
        value_avg = database[database.age_ka.between(age - gap, age + gap)][value].mean()
        raw_values.append({"age_ka": age, value: value_avg})

    return DataFrame.from_records(raw_values)


def ideal_binning_interval(
        *data_series: DataFrame,
        names: list[str] = None,
        start: int = 2400,
        end: int = 3600,
        value: str = "d18O_unadj",
        upper_value: int = 50) -> tuple[int, float]:
    max_size, interval = 0, 0
    for i in range(upper_value):
        try_series = binning_multiple_series(*data_series, names=names, start=start, end=end,
                                             fs=float((i+1)/10), value=value)
        series_size = try_series.dropna().size
        if series_size > max_size:
            max_size = series_size
            interval = float(i/10)
    return max_size, interval


if __name__ == "__main__":
    print(ideal_binning_interval(iso_1208, iso_1209, names=["1208", "1209"], upper_value=70))
    #  IDEAL BINNING INTERVALS  (No. Records, Interval in ka)
    #  Isotope = (1008, 1.9)
    #  PSU = (264, 1.5)
    #  Isotopes and Sea Levels = (1344, 1.9)