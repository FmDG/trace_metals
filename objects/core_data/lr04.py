import os

from pandas import read_csv


if not os.path.isdir("data/cores"):
    os.chdir('../..')


# Load the Oxygen Isotope datasets
iso_lr04 = read_csv("data/comparisons/LR04.csv")