import os

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import StrMethodFormatter


def format_degrees(value):
    return f'{value:.2f} °'


def changepoints_depth():
    # --- LOAD CHANGEPOINT DATA ---
    change_data = pd.read_csv("data/comparisons/PlioVAR_changepoints.csv")

    pacific = change_data[change_data.ocean == "pacific"]
    indian = change_data[change_data.ocean == "indian"]

    fig, axs = plt.subplots(
        nrows=2,
        figsize=(8, 8),
        sharex='all'
    )

    pac_01 = axs[0].scatter(x=pacific.latitude, y=(pacific.depth * -1), c=pacific.changepoint, vmin=1500, vmax=3500)
    axs[0].set(xlim=(-90, 90), ylim=(-5000, 0), title="Pacific Ocean", ylabel="Depth (m)")

    axs[1].scatter(x=indian.latitude, y=(indian.depth * -1), c=indian.changepoint, vmin=1500, vmax=3500)
    axs[1].set(xlim=(-90, 90), ylim=(-5000, 0), title="Indian Ocean", ylabel="Depth (m)", xlabel="Latitude", )
    axs[1].xaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))

    fig.colorbar(pac_01, ax=[axs[0], axs[1]], label="Most likely changepoint (ka)")

    plt.show()


if __name__ == "__main__":

    if not os.path.isdir("data/cores"):
        os.chdir('../..')

    changepoints_depth()
