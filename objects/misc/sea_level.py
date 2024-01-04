import os

import pandas as pd

if not os.path.isdir("data/misc"):
    os.chdir('../..')


sea_level = pd.read_csv("data/misc/rohling_SL_WH.csv")
