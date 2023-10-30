def highlight_mis(axs):
    # ------------- HIGHLIGHT MIS ---------------
    for ax in axs:
        # Highlight MIS 99 (2.494 - 2.51 Ma)
        ax.axvspan(
            xmin=2494,
            xmax=2510,
            ec=None,
            fc='red',
            alpha=0.1
        )
        # Highlight MIS G4 (2.681 - 2.69 Ma)
        ax.axvspan(
            xmin=2681,
            xmax=2690,
            ec=None,
            fc="blue",
            alpha=0.1
        )
