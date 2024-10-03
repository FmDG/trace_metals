import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

alphabet = ["(a)", "(b)", "(c)", "(d)", "(e)", "(f)", "(g)"]

def tick_dirs(axs: list[plt.Axes], num_plots: int, min_age: int, max_age: int, legend: bool = True) -> list[plt.Axes]:
    for q in range(num_plots):
        # Remove the left/right axes to make the plot look cleaner
        if q % 2 == 1:
            axs[q].yaxis.set(ticks_position="right", label_position='right')
            axs[q].spines['left'].set_visible(False)
        else:
            axs[q].spines['right'].set_visible(False)
        # axs[q].set_title(alphabet[q], y=0.9, x=-0.05)
        axs[q].spines['top'].set_visible(False)
        axs[q].spines['bottom'].set_visible(False)
        axs[q].xaxis.set_minor_locator(AutoMinorLocator(20))
        axs[q].yaxis.set_minor_locator(AutoMinorLocator(5))
        if legend:
            axs[q].legend(shadow=False, frameon=False)

    # Set the bottom axis on and label it with the age.
    secax = axs[0].secondary_xaxis('top')
    secax.set(xlabel="Age (ka)")
    secax.xaxis.set_minor_locator(AutoMinorLocator(10))
    axs[0].spines['top'].set_visible(True)
    axs[(num_plots - 1)].spines['bottom'].set_visible(True)
    axs[(num_plots - 1)].set(xlabel='Age (ka)', xlim=[min_age, max_age])
    return axs


def tick_dirs_single(ax: plt.axis, min_age: int, max_age: int, legend: bool = True) -> plt.axis:
    # -- Label the axis --
    ax.set(xlabel="Age (ka)", xlim=[min_age, max_age])

    # Add a legend
    if legend:
        ax.legend(shadow=False, frameon=False)

    # Add the spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_minor_locator(AutoMinorLocator(20))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    return ax

def tick_dirs_ncols(axs, num_plots: int, min_age: int, max_age: int, legend: bool = True, ncols: int = 2) -> list[plt.Axes]:
    for i in range(ncols):
        for q in range(num_plots):
            # Remove the left/right axes to make the plot look cleaner
            if q % 2 == 1:
                axs[q, i].yaxis.set(ticks_position="right", label_position='right')
                axs[q, i].spines['left'].set_visible(False)
            else:
                axs[q, i].spines['right'].set_visible(False)
            axs[q, i].spines['top'].set_visible(False)
            axs[q, i].spines['bottom'].set_visible(False)
            axs[q, i].xaxis.set_minor_locator(AutoMinorLocator(20))
            axs[q, i].yaxis.set_minor_locator(AutoMinorLocator(5))
            if legend:
                axs[q, i].legend(shadow=False, frameon=False)

        # Set the bottom axis on and label it with the age.
        secax = axs[0, i].secondary_xaxis('top')
        secax.set(xlabel="Age (ka)")
        secax.xaxis.set_minor_locator(AutoMinorLocator(10))
        axs[0, i].spines['top'].set_visible(True)
        axs[(num_plots - 1), i].spines['bottom'].set_visible(True)
        axs[(num_plots - 1), i].set(xlabel='Age (ka)', xlim=[min_age, max_age])
    return axs