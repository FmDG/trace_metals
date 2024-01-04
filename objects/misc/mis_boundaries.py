import os

import pandas as pd

if not os.path.isdir("data/misc"):
    os.chdir('../..')


mis_boundaries = pd.read_csv("data/misc/MIS_boundaries.csv")
