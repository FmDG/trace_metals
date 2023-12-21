import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":
    new_data = pd.read_csv("data/new_data.csv")
    old_data = pd.read_csv("data/cores/1209_cibs.csv")

    new_data = new_data.sort_values(by="mcd")
    new_data = new_data.dropna(subset="d18O")

    old_data = old_data.sort_values(by="mcd")
    old_data = old_data.dropna(subset="d18O")

    fig, ax = plt.subplots()

    ax.plot(old_data.mcd, old_data.d18O_unadj, marker="+", color="blue", label="Old Data")
    ax.scatter(new_data.mcd, new_data.new_d18O, marker="+", color="red", label="New Data (sure)")
    ax.scatter(new_data.mcd, new_data.unsure_d18O, marker="+", color="green", label="New Data (unsure)")

    ax.legend(shadow=False, frameon=True)
    ax.set(xlabel="Depth (mcd)", ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"), xlim=[33, 39])

    plt.show()
