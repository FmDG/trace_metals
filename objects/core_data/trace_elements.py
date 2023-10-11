import os

from pandas import read_csv


if not os.path.isdir("data/cores"):
    os.chdir('../..')

# Load the Trace Element datasets
te_1208 = read_csv("data/cores/1208_te.csv")
te_1209 = read_csv("data/cores/1209_te_new.csv").sort_values(by=['mcd'])

