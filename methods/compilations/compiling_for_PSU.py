import pandas as pd
import os


def compile_for_psu():

    trace_data = pd.read_csv("data/comparisons/607_te.csv")
    isotope_data = pd.read_csv('data/comparisons/607_d18O.csv')

    trace_data.age_ka = trace_data.age_ka.astype("int")

    new_data = trace_data.merge(isotope_data, how='inner', on='age_ka')

    new_data.to_csv("data/607_together.csv")


if __name__ == "__main__":
    # Change to the relevant directory
    os.chdir("../..")

    compile_for_psu()

