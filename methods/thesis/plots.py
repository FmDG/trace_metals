import matplotlib.pyplot as plt

from objects.core_data.psu import psu_1208, psu_1209
from objects.arguments.args_Nature import args_1209, args_1208, fill_1208, fill_1209


def bwt_plot_1209(ax: plt.axis, colour: str = "k") -> plt.axis:
    ax.plot(psu_1209.age_ka, psu_1209.temp, marker="+", color=colour)
    ax.fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, alpha=0.1, facecolor=colour)
    ax.set_ylabel('BWT Estimate ({})'.format(u'\N{DEGREE SIGN}C'), color=colour)
    ax.tick_params(axis='y', labelcolor=colour)
    return ax


def d18o_sw_plot_1209(ax: plt.axis, colour: str = "k") -> plt.axis:
    ax.plot(psu_1209.age_ka, psu_1209.d18O_sw, marker="+", color=colour)
    ax.fill_between(psu_1209.age_ka, psu_1209.d18O_min1, psu_1209.d18O_plus1, alpha=0.1, facecolor=colour)
    ax.set_ylabel('Derived {} ({} VPDB)'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"), color=colour)
    ax.tick_params(axis='y', labelcolor=colour)
    return ax