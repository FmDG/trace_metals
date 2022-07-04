import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns


def solve_approximations():
    # Change to the relevant directory
    os.chdir("../..")

    # Load the modelling data
    t_1209 = pd.read_csv("data/1209_together_cib.csv")
    t_1208 = pd.read_csv("data/1208_together_uvi.csv")

    _, axs = plt.subplots(2, 2)

    sns.scatterplot(data=t_1209, x="MgCa", y='d18O', hue="age_ka", ax=axs[0, 0])
    axs[0, 0].set(xlabel="Mg/Ca (1209)", ylabel=r"$\delta^{18}$O (1209)")

    sns.scatterplot(data=t_1209, x="MgCa", y='d13C', hue="age_ka", ax=axs[0, 1])
    axs[0, 1].set(xlabel="Mg/Ca (1209)", ylabel=r"$\delta^{13}$C (1209)")

    sns.scatterplot(data=t_1208, x="MgCa", y='d18O', hue="age_ka", ax=axs[1, 0])
    axs[1, 0].set(xlabel="Mg/Ca (1208)", ylabel=r"$\delta^{18}$O (1208)")

    sns.scatterplot(data=t_1208, x="MgCa", y='d13C', hue="age_ka", ax=axs[1, 1])
    axs[1, 1].set(xlabel="Mg/Ca (1208)", ylabel=r"$\delta^{13}$C (1208)")

    plt.show()


if __name__ == "__main__":
    solve_approximations()
