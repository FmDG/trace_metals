import os

import pandas as pd


def compile_full_data():
    # Load dataset
    raw_data = pd.read_csv("data/cores/1209_complete.csv")
    # Remove non TE data
    te_data = raw_data.dropna(subset="LiCa")
    # Export to 1209_te.csv
    te_data.to_csv("data/cores/1209_te.csv")
    # Compile the PSU ready dataset
    """
    Column 1 - time (kyrs BP ONLY)
    Column 2 - foram-d18O (permil)
    Column 3 - foram-Mg/Ca (mmol/mol)
    """
    to_psu = te_data[["age_ka", "d18O", "MgCa"]]

    to_psu.to_csv("data/1209_cibs_unadj.csv")


if __name__ == "__main__":
    os.chdir("../..")
    compile_full_data()
