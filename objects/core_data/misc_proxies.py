import os

import pandas as pd

if not os.path.isdir("data/cores"):
    os.chdir('../..')

# Load the Oxygen Isotope datasets - Uvigerina
opal_882 = pd.read_csv("data/cores/882_opal.csv")

productivity_1208 = pd.read_csv('data/cores/1208_productivity.csv')
