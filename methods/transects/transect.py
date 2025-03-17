import os

import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata, RegularGridInterpolator
import numpy as np


def show_transect():
    transect_data = pd.read_csv('data/misc/Section_Data_01.csv')

    grid_x, grid_y = np.meshgrid(np.linspace(-5, 50, 1000), np.linspace(0, 6000, 1000), indexing='ij')

    grid_z1 = griddata((transect_data.latitude, transect_data.depth), transect_data.salinity, (grid_x, grid_y), method='linear')
    # grid_RGI = RegularGridInterpolator((grid_x, grid_y), (transect_data.latitude, transect_data.depth, transect_data.salinity))
    fig, ax = plt.subplots(
    )


    # ax.imshow(grid_z1.T, aspect='auto')
    ax.scatter(data=transect_data, x='latitude', y='depth', c='salinity', marker='o')
    ax.invert_yaxis()

    # axs[2].imshow(grid_x, grid_y, grid_RGI((grid_x, grid_y)))

    plt.show()


if __name__ == "__main__":
    os.chdir('../..')
    show_transect()

