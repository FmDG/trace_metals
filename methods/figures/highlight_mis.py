def highlight_mis(axs):
    # ------------- HIGHLIGHT MIS ---------------
    for ax in axs:
        # Highlight MIS G4 (2.681 - 2.69 Ma)
        ax.axvspan(
            xmin=2681,
            xmax=2690,
            ec=None,
            fc="blue",
            alpha=0.1
        )
