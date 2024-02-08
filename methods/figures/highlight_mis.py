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
    for _, row in mis_boundaries.iterrows():
        if row["glacial"] == "glacial":
            ax.axvspan(row["age_start"], row["age_end"], fc='tab:blue', ec=None, alpha=0.1)
        else:
            ax.axvspan(row["age_start"], row["age_end"], fc='tab:red', ec=None, alpha=0.1)
        ax.annotate(row["interval"], xy=[row["age_start"] + 4, -3])
    return ax


def highlight_all_mis_greyscale(ax: plt.axis, annotate: bool = False) -> plt.axis:
    for _, row in mis_boundaries.iterrows():
        if row["glacial"] == "glacial":
            ax.axvspan(row["age_start"], row["age_end"], fc='tab:grey', ec=None, alpha=0.1)
        mid_point = ((row["age_start"] + row["age_end"])/2) - 3
        if annotate:
            ax.annotate(row["interval"], xy=[mid_point, -52])
    return ax
