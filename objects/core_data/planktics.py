import os

import pandas as pd

if not os.path.isdir("data/comparisons"):
    os.chdir('../..')

# Load the Alkenone SST datasets
planktics_1207 = pd.read_csv("data/comparisons/planktics/planktics_1207A.csv")
planktics_1208 = pd.read_csv("data/comparisons/planktics/planktics_1208.csv").dropna(subset="d18O")
planktics_1209 = pd.read_csv("data/comparisons/planktics/planktics_1209A.csv")