import os

from pandas import read_csv

if not os.path.isdir("data/cores"):
    os.chdir('../..')

# Load the Oxygen Isotope datasets
iso_925 = read_csv("data/ceara_rise/925_d18O.csv").dropna(subset="d18O_corr").sort_values(by="age_ka")
iso_927 = read_csv("data/ceara_rise/927_d18O.csv").dropna(subset="d18O_corr").sort_values(by="age_ka")
iso_929 = read_csv("data/ceara_rise/929_d18O.csv").dropna(subset="d18O_corr").sort_values(by="age_ka")

iso_925_cibs = iso_925[iso_925.type == "CWUE"]
iso_929_cibs = iso_929[iso_929.type == "CWUE"]
