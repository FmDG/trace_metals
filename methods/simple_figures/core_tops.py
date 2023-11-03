import matplotlib.pyplot as plt

from objects.core_data.core_tops import core_top_1209, core_top_1208


def core_top_uvi():
    fig, ax = plt.subplots()

    ax.plot(core_top_1208.age_ka, core_top_1208.d18O, label="1208")
    ax.plot(core_top_1209.age_ka, core_top_1209.d18O, label="1209")

    ax.legend()
    ax.invert_yaxis()

    plt.show()


if __name__ == "__main__":
    core_top_uvi()
