import matplotlib.pyplot as plt

from objects.core_data.ceara_isotopes import iso_925, iso_927, iso_929

colours = ['#dd5129', '#0f7ba2', '#43b284', '#fab255']


def ceara_rise():
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(14, 8), sharex="all")
    fig.subplots_adjust(hspace=0)

    ax.plot(iso_925.age_ka, iso_925.d18O_corr, marker="+", c=colours[0], label="ODP 925")
    ax.plot(iso_927.age_ka, iso_927.d18O_corr, marker="+", c=colours[1], label="ODP 927")
    ax.plot(iso_929.age_ka, iso_929.d18O_corr, marker="+", c=colours[2], label="ODP 929")

    ax.set(ylabel='Corrected {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"), ylim=[2, 5])
    ax.invert_yaxis()
    ax.axvspan(xmin=3195, xmax=3215, alpha=0.1, facecolor='r')  # KM5c
    ax.axvspan(xmin=2452, xmax=2477, alpha=0.1, facecolor='r')  # MIS 97
    ax.axvspan(xmin=3119, xmax=3150, alpha=0.1, facecolor='b')  # KM2
    ax.axvspan(xmin=2510, xmax=2540, alpha=0.1, facecolor='b')  # MIS 100

    min_age, max_age = 2000, 3300

    ax.legend(shadow=False, frameon=False)
    ax.set(xlabel="Age (ka)", xlim=[min_age, max_age])

    plt.show()


if __name__ == "__main__":
    ceara_rise()
