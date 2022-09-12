import pandas as pd
import os
import matplotlib.pyplot as plt


def mag_suss():
    # Load data
    mag_1208 = pd.read_csv("data/mag_suss/1208_mags.csv")
    mag_1209 = pd.read_csv("data/mag_suss/1209_mags.csv")

    mag_1209 = mag_1209.sort_values(by='Magnetic Suscept.')
    mag_1208 = mag_1208.sort_values(by='Magnetic Suscept.')

    # Convert to age model

    fig, ax = plt.subplots()

    print(mag_1208.columns)
    print(mag_1209.columns)

    ax.plot(mag_1208['Depth (mbsf)'], mag_1208['Magnetic Suscept.'], label="1208")
    ax.plot(mag_1209['Depth (mbsf)'], mag_1209['Magnetic Suscept.'], label="1209")

    ax.legend(frameon=False)

    plt.show()


if __name__ == "__main__":
    os.chdir("../..")
    mag_suss()
