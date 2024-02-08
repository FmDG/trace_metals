import matplotlib.pyplot as plt

from methods.changepoints.age_split import age_split, plot_split
from objects.core_data.isotopes import iso_1209, iso_1208
from objects.core_data.psu import psu_1208, psu_1209
from objects.arguments.met_brewer import Juarez as addColours
from objects.arguments.args_Nature import args_1209, args_1208
from methods.figures.highlight_mis import highlight_all_mis_greyscale

def change_points_mean(save_fig: bool = False):
    # Limit the 1209 PSU data to the last 3.0 Ma
    psu_1209_use = psu_1209[psu_1209.age_ka < 2900]

    changepoint_G6 = 2.730
    changepoint_G6 = 2.704
    # Load the datasets
    te_1209 = {
        "data": psu_1209_use,
        "changepoint": 2702.9,
        "value": "temp",
        "axis": 'BWT ({})'.format(u'\N{DEGREE SIGN}C'),
        "label": '1209 BWT',
        "invert": False,
    }
    te_1208 = {
        "data": psu_1208,
        "changepoint": 2687.2,
        "value": "temp",
        "axis": 'BWT ({})'.format(u'\N{DEGREE SIGN}C'),
        "label": '1208 BWT',
        "invert": False,
    }

    d18o_1209 = {
        "data": iso_1209,
        "changepoint": 2729.5,
        "value": "d18O_unadj",
        "axis": r'$\delta^{18}$O',
        "label": '1209 {}'.format(r'$\delta^{18}$O'),
        "invert": True,
    }
    d18o_1208 = {
        "data": iso_1208,
        "changepoint": 2729.0,
        "value": "d18O_unadj",
        "axis": r'$\delta^{18}$O',
        "label": '1208 {}'.format(r'$\delta^{18}$O'),
        "invert": True,
    }

    items = [te_1208, te_1209, d18o_1208, d18o_1209]

    # Plot up the data
    fig, axs = plt.subplots(
        nrows=2,
        ncols=2,
        sharex='all',
        figsize=(12, 8)
    )
    # Remove horizontal space between axes
    fig.subplots_adjust(
        hspace=0,
        wspace=0
    )

    i, j = 0, 0
    c = 0

    for x in items:
        # Return the means and standard deviations
        after_mean, after_error, before_mean, before_error = age_split(x['data'], x['changepoint'], x['value'])

        axs[i, j].plot(
            x['data'].age_ka, x['data'][x['value']],
            marker='+',
            label=x['label']
        )
        c += 1

        axs[i, j].plot(
            [x['data'].age_ka.min(), x['changepoint']], [after_mean, after_mean],
            label=f'Post-{x["changepoint"]} kyr = {after_mean:.2} ± {after_error:.1}',
            color=addColours[1]
        )
        axs[i, j].fill_between(
            [x['data'].age_ka.min(), x['changepoint']],
            [after_mean - after_error, after_mean - after_error],
            [after_mean + after_error, after_mean + after_error],
            alpha=0.1,
            color=addColours[1]
        )
        axs[i, j].plot(
            [x['changepoint'], x['data'].age_ka.max()],
            [before_mean, before_mean],
            label=f'Pre-{x["changepoint"]} kyr = {before_mean:.2} ± {before_error:.1}',
            color=addColours[2]
        )
        axs[i, j].fill_between(
            [x['changepoint'], x['data'].age_ka.max()],
            [before_mean - before_error, before_mean - before_error],
            [before_mean + before_error, before_mean + before_error],
            alpha=0.1,
            color=addColours[2]
        )

        axs[i, j].set(
            ylabel=x['axis'],
            xlabel='Age (ka)',
            xlim=[2400, 3400]
        )

        if x['invert']:
            axs[i, j].invert_yaxis()

        axs[i, j].axvline(x['changepoint'], color='r', ls='--')
        axs[i, j].legend(
            frameon=False,
            shadow=False
        )

        j += 1
        if j > 1:
            j = 0
            i += 1

    for ax in axs.flat:
        ax.label_outer()

    # Save the figure if required
    if save_fig:
        plt.savefig("figures/changepoints/changepoint_means.png", format="png", dpi=300)
    else:
        plt.show()



def bayesian_changepoint(save_fig: bool = False) -> None:

    fig, axs = plt.subplots(
        nrows=1,
        ncols=2,
        figsize=(8, 4),
        sharex="all",
        sharey="row"
    )
    '''
    axs[0, 0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, alpha=0.5, **args_1208)
    print("-----\n1208 d18O")
    plot_split(axs[0, 0], iso_1208, 2725, "d18O_unadj")
    axs[0, 0].set(ylabel="{} ({})".format(r'$\delta^{18}$O', u'\u2030'), title="1208")

    axs[0, 1].plot(iso_1209.age_ka, iso_1209.d18O_unadj, alpha=0.5, **args_1209)
    print("-----\n1209 d18O")
    plot_split(axs[0, 1], iso_1209, 2725, "d18O_unadj")
    axs[0, 1].set(title="1209", xlim=[2400, 3300])
    axs[0, 1].invert_yaxis()'''
    for ax in axs:
        ax = highlight_all_mis_greyscale(ax)

    max_age = 3000
    psu_1208_new = psu_1208[psu_1208.age_ka < max_age]

    axs[0].plot(psu_1208_new.age_ka, psu_1208_new.temp, alpha=0.5, **args_1208)
    print("-----\n1208 BWT")
    plot_split(axs[0], psu_1208_new, 2725, "temp")
    axs[0].set(ylabel=r'BWT ($\degree$C)', xlabel="Age (ka)")

    axs[1].plot(psu_1209.age_ka, psu_1209.temp, alpha=0.5, **args_1209)
    print("-----\n1209 BWT")
    plot_split(axs[1], psu_1209, 2725, "temp")
    axs[1].set(xlabel="Age (ka)", xlim=[2400, max_age])


    fig.tight_layout()

    if save_fig:
        plt.savefig("figures/changepoints/bayesian_changepoints.png", format="png", dpi=300)
    else:
        plt.show()


if __name__ == "__main__":
    # change_points_mean(save_fig=False)
    bayesian_changepoint(save_fig=False)
