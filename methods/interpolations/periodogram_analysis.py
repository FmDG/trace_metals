import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig

from methods.interpolations.generate_interpolations import resample_both
from objects.args_Nature import args_diff


def freq_to_period(x):
    return 1 / x


def period_to_freq(x):
    return 1 / x


def difference_periodogram():
    # --------------- RESAMPLE THE 1208 and 1209 DATA ---------------
    age_min, age_max = 2300, 3700
    interpolated_frame = resample_both(5.0, age_min, age_max).dropna()
    start_period = 5
    end_period = 200
    w = np.linspace(1 / end_period, 1 / start_period, 1000)
    # --------------- MAKE PERIODOGRAM ---------------
    pgram = sig.lombscargle(interpolated_frame.age_ka, interpolated_frame.d18O_difference, w, normalize=True,
                            precenter=True)

    fig, axs = plt.subplots(2, 1, constrained_layout=True)
    axs[0].plot(interpolated_frame.age_ka, interpolated_frame.d18O_difference, **args_diff)
    axs[0].set_xlabel('Age (ka)')

    axs[0].legend()
    axs[0].invert_yaxis()
    axs[0].set(ylabel='Cibicidoides {} ({} VPDB)'.format(r'$\delta^{18}$O', u"\u2030"), xlabel="Age (ka)")

    axs[1].plot(w, pgram)
    axs[1].set(ylabel="Normalised Amplitude", xlim=(1 / end_period, 1 / start_period))

    plt.show()


if __name__ == "__main__":
    difference_periodogram()
