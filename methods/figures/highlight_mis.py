import matplotlib.pyplot as plt
from objects.misc.mis_boundaries import mis_boundaries


def highlight_mis(axs) -> None:
    # ------------- HIGHLIGHT MIS ---------------
    for ax in axs:
        # Highlight MIS G6 (2.704 - 2.730 Ma)
        ax.axvspan(
            xmin=2704,
            xmax=2730,
            ec=None,
            fc="blue",
            alpha=0.1
        )


def highlight_mis_single(ax) -> None:
    # Highlight MIS G6 (2.704 - 2.730 Ma)
    ax.axvspan(
        xmin=2704,
        xmax=2730,
        ec=None,
        fc="blue",
        alpha=0.1
    )


def highlight_all_mis(ax: plt.axis) -> plt.axis:
    for index, row in mis_boundaries.iterrows():
        if row["glacial"] == "glacial":
            ax.axvspan(row["age_start"], row["age_end"], fc='tab:blue', ec=None, alpha=0.1)
        else:
            ax.axvspan(row["age_start"], row["age_end"], fc='tab:red', ec=None, alpha=0.1)
    return ax
