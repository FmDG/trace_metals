import matplotlib.pyplot as plt

from objects.args_brewer import args_1209, args_1208
from objects.core_data.isotopes import iso_1208, iso_1209

if __name__ == "__main__":
    # Define the plot
    fig, axs = plt.subplots(
        nrows=2,
        ncols=2,
        sharex="row",
        sharey="row"
    )

    fig.subplots_adjust(hspace=0, wspace=0)

    # Make plots
    axs[0, 0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)
    axs[0, 1].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)
    axs[1, 0].plot(iso_1208.age_ka, iso_1208.d13C, **args_1208)
    axs[1, 1].plot(iso_1209.age_ka, iso_1209.d13C, **args_1209)

    axs[0, 0].invert_yaxis()
    axs[0, 1].invert_yaxis()

    axs[0, 0].legend(shadow=False, frameon=False)
    axs[0, 1].legend(shadow=False, frameon=False)

    axs[0, 0].set(xlim=[2300, 3500], ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    axs[1, 0].set(xlim=[2300, 3500], ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{13}$C', u"\u2030"), xlabel="Age (ka)")

    plt.show()



