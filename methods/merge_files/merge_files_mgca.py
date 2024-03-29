import os

import pandas as pd

def merge_1208_files():
    traces = pd.read_csv("data/cores/1208_te.csv")
    isotopes = pd.read_csv("data/cores/1208_cibs.csv")

    # Merge the two datasets
    final = pd.merge(traces, isotopes, on='mcd', how='outer')

    final.to_csv("data/1208_merged.csv")


if __name__ == "__main__":
    os.chdir("../..")
    merge_1208_files()

'''
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

newly.to_csv("1208_together_cibs_02.csv")'''
