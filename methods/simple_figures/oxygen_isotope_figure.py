import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

import objects.args_brewer as args
from objects.core_data.isotopes import iso_1208, iso_1209


def oxygen_isotope_figure(age_min: int = 2200, age_max: int = 3700, save_fig: bool = False):
    # Define figure size
    fig, ax = plt.subplots(figsize=(15, 6))

    # d18O original data
    ax.plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args.args_1208)
    ax.plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args.args_1209)

    '''
    This section is a work in progress on how to display the error in the age model.
    There might be something in error envelopes below: 
    http://linked.earth/PyleoTutorials/notebooks/L1_working_with_age_ensembles.html
    # Error calcs
    lower_error = iso_1209.age_ka - iso_1209.lower95_age
    upper_error = iso_1209.upper95_age - iso_1209.age_ka
    asymmetric_error = [lower_error, upper_error]
    ax.errorbar(iso_1209.age_ka, iso_1209.d18O_unadj, yerr=0.05, xerr=asymmetric_error, capsize=2.0, **args.args_1209)
    '''

    # -- Define the axes --
    ax.set(ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))

    # Invert the axes with d18O
    ax.invert_yaxis()

    # Add a legend
    ax.legend(shadow=False, frameon=False)

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_minor_locator(AutoMinorLocator(20))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))

    # Set the bottom axis on and label it with the age.
    ax.set(xlabel='Age (ka)', xlim=[age_min, age_max])

    if save_fig:
        plt.savefig("figures/paper/Figure_1.svg", format="svg", dpi=300)
    else:
        plt.show()


if __name__ == "__main__":
    oxygen_isotope_figure(age_min=2350, age_max=3600, save_fig=True)
