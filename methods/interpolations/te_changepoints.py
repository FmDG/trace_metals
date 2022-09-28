import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Define some colours
colours = ['#1b9e77', '#d95f02', '#7570b3']


def age_split(dataseries, split_point, value="MgCa"):
    # Split the dataframe into two parts
    before = dataseries[dataseries.age_ka > split_point]
    after = dataseries[dataseries.age_ka < split_point]
    # Return the means
    return after[value].mean(), after[value].std(), before[value].mean(), before[value].std()


def te_changepoints(age_limit=False):
    # Load the data
    te_1209 = pd.read_csv("data/cores/1209_te.csv")

    # Split ages
    split_ages = [2500, 2600, 2700, 2800]

    # Age limit
    if age_limit:
        te_1209 = te_1209[te_1209.age_ka < 2900]

    # Plot up the data
    fig, axs = plt.subplots(nrows=2, ncols=2, sharex='all', sharey='all')
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0, wspace=0)

    fig.suptitle('Site 1209 Data')

    i, j = 0, 0

    for x in range(len(split_ages)):
        split_age = split_ages[x]
        # Return the means and standard deviations
        after_mean, after_error, before_mean, before_error = age_split(te_1209, split_age)

        axs[i, j].plot(te_1209.age_ka, te_1209.MgCa, marker='+', color=colours[0])
        axs[i, j].plot([te_1209.age_ka.min(), split_age], [after_mean, after_mean],
                       label=f'Post-{split_age} kyr = {after_mean:.2} ± {after_error:.1}', color=colours[1])
        axs[i, j].fill_between([te_1209.age_ka.min(), split_age], [after_mean - after_error, after_mean - after_error],
                               [after_mean + after_error, after_mean + after_error], alpha=0.1, color=colours[1])
        axs[i, j].plot([split_age, te_1209.age_ka.max()], [before_mean, before_mean],
                       label=f'Pre-{split_age} kyr = {before_mean:.2} ± {before_error:.1}', color=colours[2])
        axs[i, j].fill_between([split_age, te_1209.age_ka.max()],
                               [before_mean - before_error, before_mean - before_error],
                               [before_mean + before_error, before_mean + before_error], alpha=0.1, color=colours[2])

        axs[i, j].axvline(split_age, color='r', ls='--')
        axs[i, j].legend()

        i += 1
        if i > 1:
            i = 0
            j += 1

    for ax in axs.flat:
        ax.set(xlabel='Age (ka)', ylabel='Mg/Ca (mmol/mol)')
        ax.label_outer()

    plt.show()


def best_changepoint(age_limit=True, start=2500, stop=2850, step=10):
    # Load the data
    te_1209 = pd.read_csv("data/cores/1208_te.csv")

    # Split ages
    split_ages = np.arange(start=start, stop=stop, step=step)
    diff_means = []
    tot_errors = []
    diff_ages = []

    # Age limit
    if age_limit:
        te_1209 = te_1209[te_1209.age_ka < 2900]

    for x in split_ages:
        # Return the means and standard deviations
        after_mean, after_error, before_mean, before_error = age_split(te_1209, x)

        # append various lists
        diff_means.append(abs(before_mean - after_mean))
        tot_errors.append(after_error + before_error)
        diff_ages.append(x)

    differences_frame = pd.DataFrame(list(zip(diff_ages, diff_means, tot_errors)),
                                     columns=['diff_age', 'Difference', "St. dev."])

    fig, ax = plt.subplots(figsize=(10, 10))
    differences_frame.plot(x="diff_age", y=["Difference", "St. dev."], kind="bar", ax=ax)
    ax.set(xlabel="Age (ka)", ylabel='Difference in 1209 {} before/after ({})'.format('Mg/Ca', "mmol/mol"))
    plt.show()


def display_changepoint(age_limit=True):
    # Load the data
    te_1209 = pd.read_csv("data/cores/1209_te.csv")
    te_1208 = pd.read_csv("data/cores/1208_te.csv")

    # Age limit
    if age_limit:
        te_1209 = te_1209[te_1209.age_ka < 2900]
        te_1208 = te_1208[te_1208.age_ka < 2900]

    # Define split age
    split_age = 2700
    # Calculate means
    after_mean, after_error, before_mean, before_error = age_split(te_1209, split_age)
    after_mean_08, after_error_08, before_mean_08, before_error_08 = age_split(te_1208, split_age)

    # Plot up the data
    fig, axs = plt.subplots(nrows=2, sharex='all', sharey='all', figsize=(10, 8))
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0, wspace=0)

    # Plot up results
    axs[0].plot(te_1209.age_ka, te_1209.MgCa, marker='+', color=colours[0])
    axs[0].plot([te_1209.age_ka.min(), split_age], [after_mean, after_mean],
                label=f'Post-{split_age} kyr = {after_mean:.3} ± {after_error:.2}', color=colours[1])
    axs[0].fill_between([te_1209.age_ka.min(), split_age], [after_mean - after_error, after_mean - after_error],
                        [after_mean + after_error, after_mean + after_error], alpha=0.1, color=colours[1])
    axs[0].plot([split_age, te_1209.age_ka.max()], [before_mean, before_mean],
                label=f'Pre-{split_age} kyr = {before_mean:.3} ± {before_error:.2}', color=colours[2])
    axs[0].fill_between([split_age, te_1209.age_ka.max()],
                        [before_mean - before_error, before_mean - before_error],
                        [before_mean + before_error, before_mean + before_error], alpha=0.1, color=colours[2])

    axs[0].axvline(split_age, color='r', ls='--')
    axs[0].legend()
    axs[0].set(xlabel='Age (ka)', ylabel='1209 Mg/Ca (mmol/mol)')

    axs[1].plot(te_1208.age_ka, te_1208.MgCa, marker='+', color=colours[0])
    axs[1].plot([te_1208.age_ka.min(), split_age], [after_mean_08, after_mean_08],
                label=f'Post-{split_age} kyr = {after_mean_08:.3} ± {after_error_08:.2}', color=colours[1])
    axs[1].fill_between([te_1208.age_ka.min(), split_age],
                        [after_mean_08 - after_error_08, after_mean_08 - after_error_08],
                        [after_mean_08 + after_error_08, after_mean_08 + after_error_08], alpha=0.1, color=colours[1])
    axs[1].plot([split_age, te_1208.age_ka.max()], [before_mean_08, before_mean_08],
                label=f'Pre-{split_age} kyr = {before_mean_08:.3} ± {before_error_08:.2}', color=colours[2])
    axs[1].fill_between([split_age, te_1208.age_ka.max()],
                        [before_mean_08 - before_error_08, before_mean_08 - before_error_08],
                        [before_mean_08 + before_error_08, before_mean_08 + before_error_08], alpha=0.1,
                        color=colours[2])

    axs[1].axvline(split_age, color='r', ls='--')
    axs[1].legend()
    axs[1].set(xlabel='Age (ka)', ylabel='1208 Mg/Ca (mmol/mol)')

    plt.show()


if __name__ == "__main__":
    os.chdir("../..")
    display_changepoint()
