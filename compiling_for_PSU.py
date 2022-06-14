import pandas as pd

trace_data = pd.read_csv("data/1208_TraceMetals.csv")
isotope_data = pd.read_csv('data/ODP1208_cibs.csv')

new_data = trace_data.merge(isotope_data, how='inner', on='age_ka')

new_data.to_csv("data/1208_together.csv")

trace_data = pd.read_csv("data/1209_TraceMetals.csv")
isotope_data = pd.read_csv('data/ODP1209_uvi.csv')

new_data = trace_data.merge(isotope_data, how='inner', on='age_ka')

new_data.to_csv("data/1209_together_uvi.csv")

