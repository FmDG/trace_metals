import os

import pandas as pd

os.chdir('../..')
cores = [607, 1208, 1209]
for core in cores:
    # Load the datasets
    ages = pd.read_csv("data/PSU_Solver/RUN_5/{}_ages.csv".format(core), names=['age_ka'])
    d18O_sw = pd.read_csv("data/PSU_Solver/RUN_5/{}_d18O_sw.csv".format(core),
                          names=['d18O_sw', 'd18O_min1', 'd18O_plus1', 'd18O_min2', 'd18O_plus2'])
    salinity = pd.read_csv("data/PSU_Solver/RUN_5/{}_sal.csv".format(core),
                           names=['salinity', 'sal_min1', 'sal_plus1', 'sal_min2', 'sal_plus2'])
    temp = pd.read_csv("data/PSU_Solver/RUN_5/{}_temp.csv".format(core),
                       names=['temp', 'temp_min1', 'temp_plus1', 'temp_min2', 'temp_plus2'])
    final = pd.concat([ages, d18O_sw, salinity, temp])

    final.to_csv("data/PSU_Solver/RUN_5/{}_run.csv".format(core))
