import os

import pandas as pd

if not os.path.isdir("data/comparisons"):
    os.chdir('../..')

# Load the Alkenone SST datasets
sst_593 = pd.read_csv("data/comparisons/alkenones/593_alkenones.csv")  # New Zealand
sst_594 = pd.read_csv("data/comparisons/alkenones/594_alkenones.csv")  # New Zealand
sst_846 = pd.read_csv("data/comparisons/alkenones/846_alkenones.csv")  # EEP, Near Mexico
sst_1012 = pd.read_csv("data/comparisons/alkenones/1012_alkenones.csv")  # California
sst_1208 = pd.read_csv("data/comparisons/alkenones/1208_alkenones.csv")  # NW Pacific
sst_1417 = pd.read_csv("data/comparisons/alkenones/1417_alkenones.csv")  # Gulf of Alaska
sst_882 = pd.read_csv("data/comparisons/alkenones/882_alkenones.csv")  # Gulf of Okhotsk
sst_806 = pd.read_csv("data/comparisons/alkenones/806_alkenones.csv")  # WEP, Near New Guinea