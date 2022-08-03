import pandas as pd
import os
import matplotlib.pyplot as plt


def poster_plot():
    iso_1209 = pd.read_csv("data/cores/1209_cibs.csv")


if __name__ == "__main__":
    # Change to parent directory
    os.chdir("../..")
    # Plot the relevant graphs
    poster_plot()
