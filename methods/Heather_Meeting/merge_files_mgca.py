import os

import pandas as pd


os.chdir("../../data/PSU_Solver/sets/")
traces = pd.read_csv("849_MgCa.csv")
isotopes = pd.read_csv("849_d18O.csv")


traces.age_ka = traces.age_ka.astype(int)
isotopes.age_ka = isotopes.age_ka.astype(int)
final = pd.merge(traces, isotopes, on='age_ka')

final.to_csv("849_together.csv")
