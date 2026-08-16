import matplotlib.pyplot as plt
import numpy as np

def colour_map():
    space = np.arange(-15, -8, 0.1)
    fig, ax = plt.subplots()

    ax.scatter(np.zeros(len(space)), space, c=space, cmap='viridis')

    # plt.show()
    plt.savefig("ColourBar.pdf")



if __name__ == "__main__":
    colour_map()