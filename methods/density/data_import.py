import os

from pandas import read_csv

if not os.path.isdir("data/sea_levels"):
    os.chdir('../..')

# Load the Sea Level Isotope datasets
modelled_sl = read_csv("data/sea_levels/rohling_SL.csv")
