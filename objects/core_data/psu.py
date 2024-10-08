import os

from pandas import read_csv

if not os.path.isdir("data/cores"):
    os.chdir('../..')

# Load the PSU datasets
psu_1208 = read_csv("data/cores/1208_psu.csv").dropna()
psu_1209_no_mPWP = read_csv("data/cores/1209_psu.csv").dropna()
psu_607 = read_csv("data/cores/607_psu.csv").dropna()
psu_1313 = read_csv("data/cores/U1313_psu.csv").dropna()

psu_1209 = read_csv("data/cores/1209_psu_mPWP.csv")

psu_core_tops_1209 = read_csv("data/cores/1209_psu_core_tops.csv").dropna()
psu_core_tops_1208 = read_csv("data/cores/1208_core_tops_psu.csv").dropna()

psu_1014 = read_csv("data/cores/1014_psu.csv").dropna()
psu_1018 = read_csv("data/cores/1018_psu.csv").dropna()

psu_1209 = psu_1209.astype("float")
psu_1208 = psu_1208.astype("float")

