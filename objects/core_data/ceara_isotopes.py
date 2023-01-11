import os

from pandas import read_csv


if not os.path.isdir("data/cores"):
    os.chdir('../..')

# Load the Oxygen Isotope datasets
iso_925 = read_csv("data/ceara_rise/925_d18O.csv").sort_values(by="age_ka")
iso_926 = read_csv("data/ceara_rise/926_d18O.csv").sort_values(by="age_ka")
iso_927 = read_csv("data/ceara_rise/927_d18O.csv").sort_values(by="age_ka")
iso_928 = read_csv("data/ceara_rise/928_d18O.csv").sort_values(by="age_ka")
iso_929 = read_csv("data/ceara_rise/929_d18O.csv").sort_values(by="age_ka")