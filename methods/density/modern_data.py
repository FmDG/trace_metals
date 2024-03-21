import os

import pandas as pd
import matplotlib.pyplot as plt


os.chdir("../..")

def show_modern_salinity(save_fig: bool = False) -> None:
    fig, ax = plt.subplots(
        figsize=(8, 8)
    )
    modern_data = pd.read_csv("data/modern_pacific_data.csv")
    modern_data = modern_data[modern_data.Depth.between(500, 5000)]
    north_pacific = modern_data[modern_data.Latitude > 0]
    south_pacific = modern_data[modern_data.Latitude < 0]
    ax.scatter(modern_data.d18O, modern_data.Depth, marker="+")
    ax.scatter(north_pacific.d18O, north_pacific.Depth, label="North Pacific", marker="+")
    ax.scatter(south_pacific.d18O, south_pacific.Depth, label="South Pacific", marker="+")
    ax.set(xlabel="d18O", ylabel="Depth")
    ax.legend()

    if save_fig:
        plt.savefig("figures/modern_salinity")
    else:
        plt.show()


if __name__ == "__main__":
    show_modern_salinity(save_fig=False)