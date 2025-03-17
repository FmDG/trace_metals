import matplotlib.pyplot as plt
import numpy as np

def colour_map():
    space = np.linspace(34.2, 34.7, 101)
    fig, ax = plt.subplots()

    ax.scatter(np.zeros(101), space, c=space, cmap='viridis_r')

    # plt.show()
    plt.savefig("ColourBar.pdf")





if __name__ == "__main__":
    colour_map()