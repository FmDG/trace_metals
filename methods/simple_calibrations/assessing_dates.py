import pandas as pd
import scipy.interpolate as interpol
import matplotlib.pyplot as plt
import os


def check_dates():
    # Load the 1208 data
    cib_1208 = pd.read_csv("data/cores/1208_cibs.csv")
    uvi_1208 = pd.read_csv("data/cores/1208_uvi.csv")

    fig, ax = plt.subplots(figsize=(6, 6))
    fig.suptitle("Difference in Age Models between Venti (2012) and Woodard (2014)")

    ax.plot(cib_1208.age_ka, cib_1208.mcd, label='Venti et al., (2012)')
    ax.plot(uvi_1208.age_ka, uvi_1208.mcd, label="Woodard et al., (2014)")

    ax.legend(frameon=False, shadow=False)

    ax.set(xlim=[2400, 3400], ylim=[110, 160], xlabel="Age (ka)", ylabel="Depth (mcd)")

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.show()



if __name__ == "__main__":
    os.chdir("../..")
    check_dates()
