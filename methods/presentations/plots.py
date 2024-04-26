import matplotlib.pyplot as plt

from objects.core_data.isotopes import iso_1208, iso_1209
from objects.core_data.psu import psu_1208, psu_1209
from objects.core_data.lr04 import iso_probstack
import objects.arguments.args_Presentations as args



def isotope_plot(ax: plt.axis) -> plt.axis:
    ax.plot(iso_1208.age_ka, iso_1208.d18O_unadj, **args.args_1208)
    ax.plot(iso_1209.age_ka, iso_1209.d18O_unadj, **args.args_1209)
    ax.set(ylabel='Cibicidoides {} ({}, VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    ax.invert_yaxis()
    return ax


def psu_bwt_plot(ax: plt.axis) -> plt.axis:
    ax.plot(psu_1208.age_ka, psu_1208.temp, **args.args_1208)
    ax.fill_between(psu_1208.age_ka, psu_1208.temp_min1, psu_1208.temp_plus1, **args.fill_1208)
    ax.plot(psu_1209.age_ka, psu_1209.temp, **args.args_1209)
    ax.fill_between(psu_1209.age_ka, psu_1209.temp_min1, psu_1209.temp_plus1, **args.fill_1209)
    ax.set(ylabel='BWT Estimate ({})'.format(u'\N{DEGREE SIGN}C'))
    return ax


def psu_d18sw_plot(ax: plt.axis) -> plt.axis:
    ax.plot(psu_1208.age_ka, psu_1208.d18O_sw, **args.args_1208)
    ax.fill_between(psu_1208.age_ka, psu_1208.d18O_min1, psu_1208.d18O_plus1, **args.fill_1208)
    ax.plot(psu_1209.age_ka, psu_1209.d18O_sw, **args.args_1209)
    ax.fill_between(psu_1209.age_ka, psu_1209.d18O_min1, psu_1209.d18O_plus1, **args.fill_1209)
    ax.set(ylabel='Derived {} ({} VPDB)'.format(r'$\delta^{18}$O$_{sw}$', u"\u2030"))
    ax.invert_yaxis()
    return ax


def probStack_plot(ax: plt.axis, colour=args.colours[2]) -> plt.axis:
    ax.plot(iso_probstack.age_ka, iso_probstack.d18O_unadj, c=colour)
    ax.invert_yaxis()
    ax.set(ylabel='Probabilistic {} stack ({}, VPDB)'.format(r'$\delta^{18}$O', u"\u2030"))
    return ax
