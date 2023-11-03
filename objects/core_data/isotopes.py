import os

from pandas import read_csv

if not os.path.isdir("data/cores"):
    os.chdir('../..')

# Load the Oxygen Isotope datasets
iso_1208 = read_csv("data/cores/1208_cibs.csv").dropna(subset="d18O_unadj")
iso_1209 = read_csv('data/cores/1209_cibs.csv').dropna(subset="d18O_unadj")
iso_607 = read_csv("data/cores/607_cibs.csv")
iso_1313 = read_csv("data/cores/U1313_cibs_adj.csv")
iso_849 = read_csv("data/cores/849_cibs_adj.csv").dropna(subset="d18O")

iso_849["d18O_unadj"] = iso_849['d18O'] - 0.64
