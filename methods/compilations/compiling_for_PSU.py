import pandas as pd
import os


def compile_for_psu():

    trace_data = pd.read_csv("data/1209_TraceMetals.csv")
    isotope_data = pd.read_csv('data/ODP1209_cibs.csv')

    new_data = trace_data.merge(isotope_data, how='inner', on='age_ka')

    new_data.to_csv("data/607_together.csv")


if __name__ == "__main__":
    # Change to the relevant directory
    os.chdir("../..")

    compile_for_psu()

