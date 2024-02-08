import matplotlib.pyplot as plt


def draw_arrows(ax: plt.axis, ratio: float = 0.1, left: int = 1) -> plt.axis:
    x_point = 1.01
    if left % 2 == 1:
        x_point = -0.01
    ax.annotate('', xy=(x_point, ratio), xytext=(x_point, 0.9), xycoords='axes fraction',
                arrowprops=dict(arrowstyle="<->", color='k'))
    return ax