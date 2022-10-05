
def age_split(data_series, split_point, value="MgCa"):
    # Split the dataframe into two parts
    before = data_series[data_series.age_ka > split_point]
    after = data_series[data_series.age_ka < split_point]
    # Return the means
    return after[value].mean(), after[value].std(), before[value].mean(), before[value].std()


if __name__ == "__main__":
    pass
