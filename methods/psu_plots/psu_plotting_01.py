import pandas as pd
import os

os.chdir("../..")

ages_1208 = pd.read_csv("data/PSU_Solver/PSU_Solver_Age_1208.csv")
temp_1208 = pd.read_csv("data/PSU_Solver/PSU_Solver_Temp_1208.csv")

ages_1209 = pd.read_csv("data/PSU_Solver/PSU_Solver_Age_1209.csv")
temp_1209 = pd.read_csv("data/PSU_Solver/PSU_Solver_Temp_1209.csv")
