import os

import pandas as pd


if not os.path.isdir("data/cores"):
    os.chdir('../..')

# Load the Oxygen Isotope datasets - Uvigerina
core_top_1209 = pd.read_csv("data/comparisons/1209_core_tops_uvi.csv")
core_top_1208 = pd.read_csv("data/comparisons/1208_core_tops_uvi.csv")



