import matplotlib.pyplot as plt

from objects.core_data.core_tops import core_top_1209, core_top_1208


def core_top_uvi():
    fig, ax = plt.subplots()

    ax.scatter(core_top_1208.depth, core_top_1208.d18O, label="1208")
    ax.scatter(core_top_1209.mcd, core_top_1209.d18O, label="1209")

    ax.legend()

    plt.show()


if __name__ == "__main__":
    core_top_uvi()
