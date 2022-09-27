import os

import pandas as pd

os.chdir("../../data/PSU_Solver/sets/")
traces = pd.read_csv("1208_te.csv")
isotopes = pd.read_csv("1208_d18O_cibs.csv")

# Turn the age into integers
traces.age_ka = traces.age_ka.astype(int)
isotopes.age_ka = isotopes.age_ka.astype(int)

# Merge the two datasets
final = pd.merge(traces, isotopes, on='age_ka', how='outer')

#  Sort the values by a certain value
final = final.sort_values(by="age_ka")
final = final.reset_index()


age = []
iso = []
tel = []


for x in range(final.shape[0]):
    if x == 0:
        select = final.iloc[[0, 1]]
    elif x == (final.shape[0] - 1):
        select = final.iloc[[final.shape[0] - 2, final.shape[0] - 1]]
    else:
        select = final.iloc[[(x - 1), x, (x + 1)]]

    age.append(select.age_ka.mean())
    iso.append(select.d18O_unadj.mean())
    tel.append(select.MgCa.mean())

newly = pd.DataFrame(list(zip(age, iso, tel)), columns=['age_ka', 'd18O', 'MgCa'])

newly.to_csv("1208_together_cibs_02.csv")
