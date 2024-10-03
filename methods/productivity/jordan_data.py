from objects.core_data.isotopes import iso_1208, iso_1209
from objects.core_data.psu import psu_1208, psu_1209
from objects.core_data.misc_proxies import productivity_1208
from objects.arguments.args_Nature import args_1209, args_1208
from methods.paper.analysis import resampled_data
from methods.figures.tick_dirs import tick_dirs_ncols
from methods.figures.highlight_mis import highlight_all_mis_greyscale

import matplotlib.pyplot as plt


def jordan_data_present(save_fig: bool = False):
    n_plots = 4
    age_min, age_max = 2400, 3200
    plot_colours = ['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02','#a6761d','#666666']
    print(productivity_1208.columns)
    fig, axs = plt.subplots(
        nrows=n_plots,
        ncols = 2,
        sharex='all',
        figsize = (8, 8)
    )
    ## - Reduce the space between axes to 0 -
    fig.subplots_adjust(hspace=0)
    for axes in axs:
        for ax in axes:
            highlight_all_mis_greyscale(ax)

    axs[0, 0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args_1208)
    axs[0, 0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args_1209)
    axs[0, 0].set_ylabel('{} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"), color=plot_colours[0])
    axs[0, 0].invert_yaxis()
    axs[0, 0].legend()

    filter_diff = resampled_data[resampled_data.age_ka.between(2400, 3400)]
    axs[0, 1].plot(filter_diff.age_ka, filter_diff.difference_d18O, marker="+", color="tab:grey", label="Difference",
                   alpha=0.7)
    axs[0, 1].set(ylabel="{} ({})".format(r'$\Delta \delta^{18}$O (1208 - 1209)', u"\u2030"))
    args = {"marker": None, "color": plot_colours[1], "label": "10-ka filtered data"}
    axs[0, 1].plot(filter_diff.age_ka, filter_diff.filtered_difference, **args)
    axs[0, 1].fill_between(filter_diff.age_ka, filter_diff.filtered_difference, alpha=0.1)
    axs[0, 1].set_ylabel("{} ({})".format(r'$\Delta \delta^{18}$O', u"\u2030"), color=plot_colours[1])


    axs[1, 0].plot(productivity_1208.age_ka, productivity_1208.Mn_excess, **args_1208)
    axs[1, 0].set_ylabel(r'Mn$_{excess}$', color=plot_colours[2])

    axs[1, 1].plot(productivity_1208.age_ka, (productivity_1208.C_37/productivity_1208.CaCO3_conc), **args_1208)
    axs[1, 1].set_ylabel(r'C$_{37}$/[CaCO$_3$]', color=plot_colours[3])

    axs[2, 0].plot(productivity_1208.age_ka, productivity_1208.CaCO3_conc, **args_1208)
    axs[2, 0].set_ylabel(r'[CaCO$_3$]', color=plot_colours[4])

    axs[2, 1].plot(productivity_1208.age_ka, (productivity_1208.Opal_conc/productivity_1208.CaCO3_conc), **args_1208)
    axs[2, 1].set_ylabel(r'[Opal]/[CaCO$_3$]', color=plot_colours[5])

    axs[3, 0].plot(productivity_1208.age_ka, productivity_1208.Opal_conc, **args_1208)
    axs[3, 0].set_ylabel(r'[Opal]', color=plot_colours[6])

    axs[3, 1].plot(productivity_1208.age_ka, (productivity_1208.Ba_excess/productivity_1208.Opal_conc), **args_1208)
    axs[3, 1].set_ylabel(r'Ba$_{excess}$/[Opal]', color=plot_colours[7])

    tick_dirs_ncols(axs, n_plots, age_min, age_max, False, 2)

    plt.show()


if __name__ == "__main__":
    jordan_data_present()