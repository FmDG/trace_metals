import matplotlib.pyplot as plt
import pandas as pd

from objects.arguments.args_brewer import args_1209, args_1208
from objects.core_data.isotopes import iso_1208, iso_1209

if __name__ == "__main__":
    dataset = pd.read_csv("data/full_new_data.csv")

    dataset = dataset.dropna(subset="d18O_unadj")
    dataset = dataset.sort_values(by="mcd")

    fig, axs = plt.subplots(2, figsize=(14, 7))

    axs[0].plot(dataset.mcd, dataset.d18O_unadj, **args_1209)
    axs[0].set(ylabel="d18O", xlabel="Depth (mcd)", xlim=[33.5, 58.5])
    axs[0].invert_yaxis()

    axs[1].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)
    axs[1].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)
    axs[1].set(ylabel="d18O", xlabel="Age (ka)", xlim=[2340, 3600])
    axs[1].invert_yaxis()
    axs[1].legend(frameon=False)

    plt.savefig("figures/new_data.png", format="png", dpi=300)
    # plt.show()
