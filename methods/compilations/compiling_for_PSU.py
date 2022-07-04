import pandas as pd
import os

os.chdir("../..")

trace_data = pd.read_csv("data/comparisons/607_te.csv")
isotope_data = pd.read_csv('data/comparisons/607_d18O.csv')

trace_data.age_ka = trace_data.age_ka.astype("int")

new_data = trace_data.merge(isotope_data, how='inner', on='age_ka')

new_data.to_csv("data/607_together.csv")

