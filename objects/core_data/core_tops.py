import os

import pandas as pd

if not os.path.isdir("data/comparisons"):
    os.chdir('../..')

# Load the Oxygen Isotope datasets - Uvigerina
core_top_1209_uvi = pd.read_csv("data/comparisons/1209_core_tops_uvi.csv")
core_top_1208 = pd.read_csv("data/comparisons/1208_core_tops_uvi.csv")

core_top_1209_cibs = pd.read_csv("data/comparisons/1209_core_tops_cibs.csv")

bordiga_data = pd.read_csv("data/comparisons/1209_bordiga.csv")