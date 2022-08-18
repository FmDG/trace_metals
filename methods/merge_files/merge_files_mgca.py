import os

import pandas as pd


os.chdir("../../data/PSU_Solver/sets/")
traces = pd.read_csv("1208_te.csv")
isotopes = pd.read_csv("1208_d18O_cibs.csv")


traces.age_ka = traces.age_ka.astype(int)
isotopes.age_ka = isotopes.age_ka.astype(int)
final = pd.merge(traces, isotopes, on='age_ka', how='outer')

final.to_csv("1208_together_02.csv")
