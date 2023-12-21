def highlight_mis(axs):
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
