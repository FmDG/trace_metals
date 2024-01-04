import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator


def tick_dirs(axs: list[plt.Axes], num_plots: int, min_age: int, max_age: int, legend: bool = True) -> list[plt.Axes]:
    for q in range(num_plots):
        # Remove the left/right axes to make the plot look cleaner
        if q % 2 == 1:
            axs[q].yaxis.set(ticks_position="right", label_position='right')
            axs[q].spines['left'].set_visible(False)
        else:
            axs[q].spines['right'].set_visible(False)
        axs[q].spines['top'].set_visible(False)
        axs[q].spines['bottom'].set_visible(False)
        axs[q].xaxis.set_minor_locator(AutoMinorLocator(20))
        axs[q].yaxis.set_minor_locator(AutoMinorLocator(5))
        if legend:
            axs[q].legend(shadow=False, frameon=False)

    # Set the bottom axis on and label it with the age.
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



def tick_dirs_both(axs: list[plt.Axes], num_plots: int, min_age: int, max_age: int, legend: bool = True):
    for q in range(num_plots):
        '''if q % 2 == 1:
            axs[q].yaxis.set(ticks_position="right", label_position='right')'''
        axs[q].xaxis.set_minor_locator(AutoMinorLocator(10))
        axs[q].yaxis.set_minor_locator(AutoMinorLocator(5))
        axs[q].tick_params(axis='y', which="both", left=True, right=True, direction="out")
        axs[q].tick_params(axis='x', which="both", top=False, bottom=False)
        axs[q].tick_params(axis="both", which='major', length=6)
        axs[q].tick_params(axis="both", which='minor', length=3)
        if legend:
            axs[q].legend(shadow=False, frameon=False)

    # Set the bottom axis on and label it with the age.
    axs[(num_plots - 1)].tick_params(axis='x', which="both", bottom=True)
    axs[0].tick_params(axis='x', which="both", top=True)
    axs[(num_plots - 1)].set(xlabel='Age (ka)', xlim=[min_age, max_age])
