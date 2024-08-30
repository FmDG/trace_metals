from methods.stats.overlaps import generate_differences
from objects.core_data.isotopes import iso_1208, iso_1209
from objects.misc.mis_boundaries import mis_boundaries
from methods.figures.highlight_mis import highlight_all_mis_greyscale

from scipy.stats import kstest, ttest_ind
import matplotlib.pyplot as plt


sample_data = generate_differences(2).dropna(subset='difference_d18O')
sample_data['glacial'] = False
iso_1208['glacial'] = False
iso_1209['glacial'] = False
for _, row in mis_boundaries.iterrows():
    lower_age = row["age_start"]
    upper_age = row['age_end']
    if row["glacial"] == "glacial":
        sample_data.loc[(sample_data.age_ka >= lower_age) & (sample_data.age_ka < upper_age), 'glacial'] = True
        iso_1208.loc[(iso_1208.age_ka >= lower_age) & (iso_1208.age_ka < upper_age), 'glacial'] = True
        iso_1209.loc[(iso_1209.age_ka >= lower_age) & (iso_1209.age_ka < upper_age), 'glacial'] = True

sample_data['pliocene'] = False
sample_data.loc[sample_data.age_ka > 2700, 'pliocene'] = True

iso_1208['pliocene'] = False
iso_1209['pliocene'] = False
iso_1208.loc[iso_1208.age_ka > 2700, 'pliocene'] = True
iso_1209.loc[iso_1209.age_ka > 2700, 'pliocene'] = True


def isotope_stats():
    sel_iso_1208 = iso_1208.loc[iso_1208.age_ka > iso_1209.age_ka.min()]

    pliocene_glacial_1208 = sel_iso_1208.loc[sel_iso_1208.pliocene & sel_iso_1208.glacial].d18O_unadj.values
    pliocene_glacial_1209 = iso_1209.loc[iso_1209.pliocene & iso_1209.glacial].d18O_unadj.values
    pliocene_interglacial_1208 = sel_iso_1208.loc[sel_iso_1208.pliocene & (sel_iso_1208.glacial == False)].d18O_unadj.values
    pliocene_interglacial_1209 = iso_1209.loc[iso_1209.pliocene & (iso_1209.glacial == False)].d18O_unadj.values
    pleistocene_glacial_1208 = sel_iso_1208.loc[(sel_iso_1208.pliocene == False) & sel_iso_1208.glacial].d18O_unadj.values
    pleistocene_glacial_1209 = iso_1209.loc[(iso_1209.pliocene == False) & iso_1209.glacial].d18O_unadj.values
    pleistocene_interglacial_1208 = sel_iso_1208.loc[
        (sel_iso_1208.pliocene == False) & (sel_iso_1208.glacial == False)].d18O_unadj.values
    pleistocene_interglacial_1209 = iso_1209.loc[
        (iso_1209.pliocene == False) & (iso_1209.glacial == False)].d18O_unadj.values

    pliocene_1208 = sel_iso_1208.loc[(sel_iso_1208.age_ka > 2700)].d18O_unadj.values
    pliocene_1209 = iso_1209.loc[(iso_1209.age_ka > 2700)].d18O_unadj.values

    print('KS test')
    print("Is the d18O during Pliocene glacials significantly different at 1208 compared to 1209?")
    print(f'Yes, p value = {kstest(pliocene_glacial_1208, pliocene_glacial_1209).pvalue:.4g}')
    print(f'Pliocene Glacial 1208 Mean: {pliocene_glacial_1208.mean():.4f}, Pliocene Glacial 1209 Mean: {pliocene_glacial_1209.mean():.4f}')
    print(f'Difference in Pliocene Glacial Means: {(pliocene_glacial_1208.mean() - pliocene_glacial_1209.mean()):.4f}')
    print("Is the d18O during Pliocene interglacials significantly different at 1208 compared to 1209?")
    print(f'Yes, p value = {kstest(pliocene_interglacial_1208, pliocene_interglacial_1209).pvalue:.4g}')
    print(f'Pliocene Interglacial 1208 Mean: {pliocene_interglacial_1208.mean():.4f}, Pliocene Interglacial 1209 Mean: {pliocene_interglacial_1209.mean():.4f}')
    print(f'Difference in Pliocene Interglacial Means: {(pliocene_interglacial_1208.mean() - pliocene_interglacial_1209.mean()):.4f}')
    print("Is the d18O during Pleistocene glacials significantly different at 1208 compared to 1209?")
    print(f'Yes, p value = {kstest(pleistocene_glacial_1208, pleistocene_glacial_1209).pvalue:.4g}')
    print(f'Yes, p value = {ttest_ind(pleistocene_glacial_1208, pleistocene_glacial_1209, equal_var=False).pvalue:.4g} (T-test)')
    print(f'Pleistocene Glacial 1208 Mean: {pleistocene_glacial_1208.mean():.4f}, Pleistocene Glacial 1209 Mean: {pleistocene_glacial_1209.mean():.4f}')
    print(f'Difference in Pleistocene Glacial Means: {(pleistocene_glacial_1208.mean() - pleistocene_glacial_1209.mean()):.4f}')
    print("Is the d18O during Pleistocene interglacials significantly different at 1208 compared to 1209?")
    print(f'Yes, p value = {kstest(pleistocene_interglacial_1208, pleistocene_interglacial_1209).pvalue:.4g}')
    print(f'Pleistocene Interglacial 1208 Mean: {pleistocene_interglacial_1208.mean():.4f}, Pleistocene Interglacial 1209 Mean: {pleistocene_interglacial_1209.mean():.4f}')
    print(f'Difference in Pleistocene Interglacial Means: {(pleistocene_interglacial_1208.mean() - pleistocene_interglacial_1209.mean()):.4f}')


    print("Is the d18O during the Pliocene significantly different at 1208 compared to 1209?")
    print(f'Yes, p value = {kstest(pliocene_1208, pliocene_1209).pvalue:.4g}')
    print(f'Pliocene 1208 Mean: {pliocene_1208.mean():.4f}, Pliocene 1209 Mean: {pliocene_1209.mean():.4f}')
    print(f'Difference in Pliocene Means: {(pliocene_1208.mean() - pliocene_1209.mean()):.4f}')


    fig, axs = plt.subplots(
            nrows = 2,
            ncols = 2,
            sharex = 'all',
            sharey = 'all',
            figsize = (8, 8)
    )

    axs[0, 0].hist(pliocene_glacial_1208, alpha=0.2, label='1208 Pliocene Glacials')
    axs[0, 0].axvline(pliocene_glacial_1208.mean(), ls='--', color='tab:blue', label='1208 Mean')
    axs[0, 0].hist(pliocene_glacial_1209, alpha=0.2, label='1209 Pliocene Glacials')
    axs[0, 0].axvline(pliocene_glacial_1209.mean(), ls='--', color='tab:orange', label='1209 Mean')

    axs[0, 1].hist(pliocene_interglacial_1208, alpha=0.2, label='1208 Pliocene Interglacials')
    axs[0, 1].axvline(pliocene_interglacial_1208.mean(), ls='--', color='tab:blue', label='1208 Mean')
    axs[0, 1].hist(pliocene_interglacial_1209, alpha=0.2, label='1209 Pliocene Interglacials')
    axs[0, 1].axvline(pliocene_interglacial_1209.mean(), ls='--', color='tab:orange', label='1209 Mean')

    axs[1, 0].hist(pleistocene_glacial_1208, alpha=0.2, label='1208 Pleistocene Glacials')
    axs[1, 0].axvline(pleistocene_glacial_1208.mean(), ls='--', color='tab:blue', label='1208 Mean')
    axs[1, 0].hist(pleistocene_glacial_1209, alpha=0.2, label='1209 Pleistocene Glacials')
    axs[1, 0].axvline(pleistocene_glacial_1209.mean(), ls='--', color='tab:orange', label='1209 Mean')

    axs[1, 1].hist(pleistocene_interglacial_1208, alpha=0.2, label='1208 Pleistocene Interglacials')
    axs[1, 1].axvline(pleistocene_interglacial_1208.mean(), ls='--', color='tab:blue', label='1208 Mean')
    axs[1, 1].hist(pleistocene_interglacial_1209, alpha=0.2, label='1209 Pleistocene Interglacials')
    axs[1, 1].axvline(pleistocene_interglacial_1209.mean(), ls='--', color='tab:orange', label='1209 Mean')

    for axes in axs:
        for ax in axes:
            ax.legend(ncols=2)
            ax.set(xlabel=r'$\delta^{18}$O')

    plt.show()


def same_isotope_stats():
    sel_iso_1208 = iso_1208.loc[iso_1208.age_ka > iso_1209.age_ka.min()]

    pliocene_glacial_1208 = sel_iso_1208.loc[sel_iso_1208.pliocene & sel_iso_1208.glacial].d18O_unadj.values
    pliocene_glacial_1209 = iso_1209.loc[iso_1209.pliocene & iso_1209.glacial].d18O_unadj.values
    pliocene_interglacial_1208 = sel_iso_1208.loc[sel_iso_1208.pliocene & (sel_iso_1208.glacial == False)].d18O_unadj.values
    pliocene_interglacial_1209 = iso_1209.loc[iso_1209.pliocene & (iso_1209.glacial == False)].d18O_unadj.values
    pleistocene_glacial_1208 = sel_iso_1208.loc[(sel_iso_1208.pliocene == False) & sel_iso_1208.glacial].d18O_unadj.values
    pleistocene_glacial_1209 = iso_1209.loc[(iso_1209.pliocene == False) & iso_1209.glacial].d18O_unadj.values
    pleistocene_interglacial_1208 = sel_iso_1208.loc[
        (sel_iso_1208.pliocene == False) & (sel_iso_1208.glacial == False)].d18O_unadj.values
    pleistocene_interglacial_1209 = iso_1209.loc[
        (iso_1209.pliocene == False) & (iso_1209.glacial == False)].d18O_unadj.values

    print('Welch T-test')
    print("Is the d18O at 1208 during Pliocene glacials significantly different to Pleistocene glacials?")
    print(f'Yes, p value = {ttest_ind(pliocene_glacial_1208, pleistocene_glacial_1208, equal_var=False).pvalue:.4g}')
    print(f'Pliocene Glacial 1208 Mean: {pliocene_glacial_1208.mean():.4f}, Pleistocene Glacial 1208 Mean: {pleistocene_glacial_1208.mean():.4f}')
    print(f'Difference in 1208 Glacial Means: {(pliocene_glacial_1208.mean() - pleistocene_glacial_1208.mean()):.4f}')
    print("Is the d18O at 1209 during Pliocene glacials significantly different to Pleistocene glacials?")
    print(f'Yes, p value = {ttest_ind(pliocene_glacial_1209, pleistocene_glacial_1209, equal_var=False).pvalue:.4g}')
    print(f'Pliocene Glacial 1209 Mean: {pliocene_glacial_1209.mean():.4f}, Pleistocene Glacial 1209 Mean: {pleistocene_glacial_1209.mean():.4f}')
    print(f'Difference in 1209 Glacial Means: {(pliocene_glacial_1209.mean() - pleistocene_glacial_1209.mean()):.4f}')
    print("Is the d18O at 1208 during Pliocene interglacials significantly to Pleistocene interglacials?")
    print(f'Yes, p value = {ttest_ind(pliocene_interglacial_1208, pleistocene_interglacial_1208, equal_var=False).pvalue:.4g}')
    print(f'Pliocene Interglacial 1208 Mean: {pliocene_interglacial_1208.mean():.4f}, Pleistocene interglacial 1208 Mean: {pleistocene_interglacial_1208.mean():.4f}')
    print(f'Difference in 1208 Interglacial Means: {(pliocene_interglacial_1208.mean() - pleistocene_interglacial_1208.mean()):.4f}')
    print("Is the d18O at 1209 during Pliocene interglacials significantly different to Pleistocene interglacials?")
    print(f'Yes, p value = {ttest_ind(pliocene_interglacial_1209, pleistocene_interglacial_1209, equal_var=False).pvalue:.4g}')
    print(f'Pliocene Interglacial 1209 Mean: {pliocene_interglacial_1209.mean():.4f}, Pleistocene Interglacial 1209 Mean: {pleistocene_interglacial_1209.mean():.4f}')
    print(f'Difference in 1209 Interglacial Means: {(pliocene_interglacial_1209.mean() - pleistocene_interglacial_1209.mean()):.4f}')

    fig, axs = plt.subplots(
            nrows = 2,
            ncols = 2,
            sharex = 'all',
            sharey = 'all',
            figsize = (8, 8)
    )

    axs[0, 0].hist(pliocene_glacial_1208, alpha=0.2, label='1208 Pliocene Glacials')
    axs[0, 0].axvline(pliocene_glacial_1208.mean(), ls='--', color='tab:blue', label='Pliocene Mean')
    axs[0, 0].hist(pleistocene_glacial_1208, alpha=0.2, label='1208 Pleistocene Glacials')
    axs[0, 0].axvline(pleistocene_glacial_1208.mean(), ls='--', color='tab:orange', label='Pleistocene Mean')

    axs[0, 1].hist(pliocene_glacial_1209, alpha=0.2, label='1209 Pliocene Glacials')
    axs[0, 1].axvline(pliocene_glacial_1209.mean(), ls='--', color='tab:blue', label='Pliocene Mean')
    axs[0, 1].hist(pleistocene_glacial_1209, alpha=0.2, label='1209 Pleistocene Glacials')
    axs[0, 1].axvline(pleistocene_glacial_1209.mean(), ls='--', color='tab:orange', label='Pleistocene Mean')

    axs[1, 0].hist(pliocene_interglacial_1208, alpha=0.2, label='1208 Pliocene Interglacials')
    axs[1, 0].axvline(pliocene_interglacial_1208.mean(), ls='--', color='tab:blue', label='Pliocene Mean')
    axs[1, 0].hist(pleistocene_interglacial_1208, alpha=0.2, label='1208 Pleistocene Interglacials')
    axs[1, 0].axvline(pleistocene_interglacial_1208.mean(), ls='--', color='tab:orange', label='Pleistocene Mean')

    axs[1, 1].hist(pliocene_interglacial_1209, alpha=0.2, label='1209 Pliocene Interglacials')
    axs[1, 1].axvline(pliocene_interglacial_1209.mean(), ls='--', color='tab:blue', label='Pliocene Mean')
    axs[1, 1].hist(pleistocene_interglacial_1209, alpha=0.2, label='1209 Pleistocene Interglacials')
    axs[1, 1].axvline(pleistocene_interglacial_1209.mean(), ls='--', color='tab:orange', label='Pleistocene Mean')

    for axes in axs:
        for ax in axes:
            ax.legend(ncols=2)
            ax.set(xlabel=r'$\delta^{18}$O')

    plt.show()


def isotope_overlaps():
    fig, ax = plt.subplots(
        figsize=(8, 8)
    )

    ax.scatter(
        sample_data.loc[sample_data.pliocene & sample_data.glacial].d18O_unadj_mean_1208,
        sample_data.loc[sample_data.pliocene & sample_data.glacial].d18O_unadj_mean_1209,
        label='Pliocene Glacials'
    )

    ax.scatter(
        sample_data.loc[sample_data.pliocene & (sample_data.glacial == False)].d18O_unadj_mean_1208,
        sample_data.loc[sample_data.pliocene & (sample_data.glacial == False)].d18O_unadj_mean_1209,
        label='Pliocene Interglacials'
    )

    ax.scatter(
        sample_data.loc[(sample_data.pliocene == False) & sample_data.glacial].d18O_unadj_mean_1208,
        sample_data.loc[(sample_data.pliocene == False) & sample_data.glacial].d18O_unadj_mean_1209,
        label='Pleistocene Glacials'
    )

    ax.scatter(
        sample_data.loc[(sample_data.pliocene == False) & (sample_data.glacial == False)].d18O_unadj_mean_1208,
        sample_data.loc[(sample_data.pliocene == False) & (sample_data.glacial == False)].d18O_unadj_mean_1209,
        label='Pleistocene Interglacials'
    )

    ax.plot([2.2, 3.8], [2.2, 3.8], ls='--')

    ax.set(xlim=[2.2, 3.8], ylim=[2.2, 3.8], ylabel='1209', xlabel='1208')
    ax.legend()

    fig, ax = plt.subplots(
        figsize=(8, 8)
    )

    ax.plot(iso_1209.age_ka, iso_1209.d18O_unadj, ls='--', color='k')

    ax.scatter(
        iso_1209.loc[iso_1209.pliocene & iso_1209.glacial].age_ka,
        iso_1209.loc[iso_1209.pliocene & iso_1209.glacial].d18O_unadj,
        label='Pliocene Glacials 1209'
    )

    ax.scatter(
        iso_1209.loc[iso_1209.pliocene & (iso_1209.glacial == False)].age_ka,
        iso_1209.loc[iso_1209.pliocene & (iso_1209.glacial == False)].d18O_unadj,
        label='Pliocene Interglacials 1209'
    )

    ax.scatter(
        iso_1209.loc[(iso_1209.pliocene == False) & iso_1209.glacial].age_ka,
        iso_1209.loc[(iso_1209.pliocene == False) & iso_1209.glacial].d18O_unadj,
        label='Pleistocene Glacials 1209'
    )

    ax.scatter(
        iso_1209.loc[(iso_1209.pliocene == False) & (iso_1209.glacial == False)].age_ka,
        iso_1209.loc[(iso_1209.pliocene == False) & (iso_1209.glacial == False)].d18O_unadj,
        label='Pleistocene Interglacials 1209'
    )

    ax.invert_yaxis()
    ax.set(xlabel='Age (ka)')
    ax.legend()

    fig, ax = plt.subplots(
        figsize=(8, 8)
    )

    ax.plot(iso_1208.age_ka, iso_1208.d18O_unadj, ls='--', color='k')

    ax.scatter(
        iso_1208.loc[iso_1208.pliocene & iso_1208.glacial].age_ka,
        iso_1208.loc[iso_1208.pliocene & iso_1208.glacial].d18O_unadj,
        label='Pliocene Glacials 1208'
    )

    ax.scatter(
        iso_1208.loc[iso_1208.pliocene & (iso_1208.glacial == False)].age_ka,
        iso_1208.loc[iso_1208.pliocene & (iso_1208.glacial == False)].d18O_unadj,
        label='Pliocene Interglacials 1208'
    )

    ax.scatter(
        iso_1208.loc[(iso_1208.pliocene == False) & iso_1208.glacial].age_ka,
        iso_1208.loc[(iso_1208.pliocene == False) & iso_1208.glacial].d18O_unadj,
        label='Pleistocene Glacials 1208'
    )

    ax.scatter(
        iso_1208.loc[(iso_1208.pliocene == False) & (iso_1208.glacial == False)].age_ka,
        iso_1208.loc[(iso_1208.pliocene == False) & (iso_1208.glacial == False)].d18O_unadj,
        label='Pleistocene Interglacials 1208'
    )

    ax.invert_yaxis()
    ax.set(xlabel='Age (ka)')
    ax.legend()


    plt.show()


def difference_stats():

    pliocene_glacial_difference = sample_data.loc[sample_data.pliocene & sample_data.glacial].difference_d18O.values
    pliocene_interglacial_difference = sample_data.loc[sample_data.pliocene & (sample_data.glacial == False)].difference_d18O.values
    pleistocene_glacial_difference = sample_data.loc[(sample_data.pliocene == False) & sample_data.glacial].difference_d18O.values
    pleistocene_interglacial_difference = sample_data.loc[(sample_data.pliocene == False) & (sample_data.glacial == False)].difference_d18O.values

    pliocene_difference = sample_data.loc[sample_data.pliocene].difference_d18O.values

    print('KS test')
    print(
        "Is the difference in d18O during glacials significantly different in the Pliocene compared to the Pleistocene?")
    print(f'No, p value = {ttest_ind(pliocene_glacial_difference, pleistocene_glacial_difference, equal_var=False).pvalue:.4f}')
    print(f'Pliocene Glacials: {pliocene_glacial_difference.mean():.4f}, Pleistocene Glacials: {pleistocene_glacial_difference.mean():.4f}')
    print(f'Difference: {pliocene_glacial_difference.mean() - pleistocene_glacial_difference.mean():.4f}')
    print(
        "Is the difference in d18O during interglacials significantly different in the Pliocene compared to the Pleistocene?")
    print(f'Yes, p value = {kstest(pliocene_interglacial_difference, pleistocene_interglacial_difference).pvalue:.4f}')
    print(f'Pliocene Interglacials: {pliocene_interglacial_difference.mean():.4f}, Pleistocene Interglacials: {pleistocene_interglacial_difference.mean():.4f}')
    print(f'Difference: {pliocene_interglacial_difference.mean() - pleistocene_interglacial_difference.mean():.4f}')
    print(
        "Is the difference in d18O in the Pliocene significantly different in glacials compared to interglacials?")
    print(f'No, p value = {kstest(pliocene_glacial_difference, pliocene_interglacial_difference).pvalue:.4f}')
    print(f'Pliocene Glacials: {pliocene_glacial_difference.mean():.4f}, Pliocene Interglacials: {pliocene_interglacial_difference.mean():.4f}')
    print(f'Difference: {pliocene_glacial_difference.mean() - pliocene_interglacial_difference.mean():.4f}')
    print(
        "Is the difference in d18O in the Pleistocene significantly different in glacials compared to interglacials?")
    print(f'Yes, p value = {kstest(pleistocene_glacial_difference, pleistocene_interglacial_difference).pvalue:.4f}')
    print(f'Pleistocene Glacials: {pleistocene_glacial_difference.mean():.4f}, Pleistocene Interglacials: {pleistocene_interglacial_difference.mean():.4f}')
    print(f'Difference: {pleistocene_glacial_difference.mean() - pleistocene_interglacial_difference.mean():.4f}')

    print(
        "Is the difference in d18O in the Pleistocene glacials significantly different to the Pliocene?")
    print(f'No, p value = {ttest_ind(pleistocene_glacial_difference, pliocene_difference, equal_var=False).pvalue:.4f}')
    print(f'Pleistocene Glacials: {pleistocene_glacial_difference.mean():.4f}, Pliocene: {pliocene_difference.mean():.4f}')
    print(f'Difference: {pleistocene_glacial_difference.mean() - pliocene_difference.mean():.4f}')

    print(
        "Is the difference in d18O in the Pleistocene interglacials significantly different to the Pliocene?")
    print(f'Yes, p value = {ttest_ind(pleistocene_interglacial_difference, pliocene_difference, equal_var=False).pvalue:.4f}')
    print(f'Pleistocene Glacials: {pleistocene_interglacial_difference.mean():.4f}, Pliocene: {pliocene_difference.mean():.4f}')
    print(f'Difference: {pleistocene_interglacial_difference.mean() - pliocene_difference.mean():.4f}')


    fig, axs = plt.subplots(
        ncols = 2,
        sharey='all',
        sharex='all',
        figsize=(10, 5)
    )

    axs[0].hist(pliocene_glacial_difference, alpha=0.2, label='Pliocene')
    axs[0].axvline(pliocene_glacial_difference.mean(), ls='--', label='Pliocene Mean', color='tab:blue')
    axs[0].hist(pleistocene_glacial_difference, alpha=0.2, label='Pleistocene')
    axs[0].axvline(pleistocene_glacial_difference.mean(), ls='--', label='Pleistocene Mean', color='tab:orange')
    axs[0].legend(ncols=2)
    axs[0].set(xlabel=r'$\Delta \delta^{18}$O', title='Glacials')

    axs[1].hist(pliocene_interglacial_difference, alpha=0.2, label='Pliocene')
    axs[1].axvline(pliocene_interglacial_difference.mean(), ls='--', label='Pliocene Mean', color='tab:blue')
    axs[1].hist(pleistocene_interglacial_difference, alpha=0.2, label='Pleistocene')
    axs[1].axvline(pleistocene_interglacial_difference.mean(), ls='--', label='Pleistocene Mean', color='tab:orange')
    axs[1].legend(ncols=2)
    axs[1].set(xlabel=r'$\Delta \delta^{18}$O', title='Interglacials')

    fig, axs = plt.subplots(
        ncols = 2,
        sharey='all',
        sharex='all',
        figsize=(10, 5)
    )

    axs[0].hist(pliocene_glacial_difference, alpha=0.2, label='Glacials')
    axs[0].axvline(pliocene_glacial_difference.mean(), ls='--', label='Glacial Mean', color='tab:blue')
    axs[0].hist(pliocene_interglacial_difference, alpha=0.2, label='Interglacials')
    axs[0].axvline(pliocene_interglacial_difference.mean(), ls='--', label='Interglacial Mean', color='tab:orange')
    axs[0].legend(ncols=2)
    axs[0].set(xlabel=r'$\Delta \delta^{18}$O', title='Pliocene')

    axs[1].hist(pleistocene_glacial_difference, alpha=0.2, label='Glacials')
    axs[1].axvline(pleistocene_glacial_difference.mean(), ls='--', label='Glacial Mean', color='tab:blue')
    axs[1].hist(pleistocene_interglacial_difference, alpha=0.2, label='Interglacials')
    axs[1].axvline(pleistocene_interglacial_difference.mean(), ls='--', label='Integlacial Mean', color='tab:orange')
    axs[1].legend(ncols=2)
    axs[1].set(xlabel=r'$\Delta \delta^{18}$O', title='Pleistocene')

    plt.show()


def visualise_differences():
    pliocene_glacial_difference = sample_data.loc[sample_data.pliocene & sample_data.glacial]
    pliocene_interglacial_difference = sample_data.loc[sample_data.pliocene & (sample_data.glacial == False)]
    pleistocene_glacial_difference = sample_data.loc[(sample_data.pliocene == False) & sample_data.glacial]
    pleistocene_interglacial_difference = sample_data.loc[(sample_data.pliocene == False) & (sample_data.glacial == False)]

    pliocene_glacial_1208 = iso_1208.loc[iso_1208.pliocene & iso_1208.glacial]
    pliocene_glacial_1209 = iso_1209.loc[iso_1209.pliocene & iso_1209.glacial]
    pliocene_interglacial_1208 = iso_1208.loc[iso_1208.pliocene & (iso_1208.glacial == False)]
    pliocene_interglacial_1209 = iso_1209.loc[iso_1209.pliocene & (iso_1209.glacial == False)]
    pleistocene_glacial_1208 = iso_1208.loc[(iso_1208.pliocene == False) & iso_1208.glacial]
    pleistocene_glacial_1209 = iso_1209.loc[(iso_1209.pliocene == False) & iso_1209.glacial]
    pleistocene_interglacial_1208 = iso_1208.loc[(iso_1208.pliocene == False) & (iso_1208.glacial == False)]
    pleistocene_interglacial_1209 = iso_1209.loc[(iso_1209.pliocene == False) & (iso_1209.glacial == False)]

    fig, axs = plt.subplots(
        nrows=2,
        sharex='all'
    )

    for ax in axs:
        highlight_all_mis_greyscale(ax)

    axs[0].plot(iso_1208.age_ka, iso_1208.d18O_unadj, lw=0.5)
    axs[0].plot(iso_1209.age_ka, iso_1209.d18O_unadj, lw=0.5)
    axs[0].scatter(pliocene_glacial_1208.age_ka, pliocene_glacial_1208.d18O_unadj,
               label='Pliocene Glacials 1208', marker="+")
    axs[0].scatter(pliocene_interglacial_1208.age_ka, pliocene_interglacial_1208.d18O_unadj,
               label='Pliocene Interglacials 1208', marker="+")
    axs[0].scatter(pleistocene_glacial_1208.age_ka, pleistocene_glacial_1208.d18O_unadj,
               label='Pleistocene Glacials 1208', marker="+")
    axs[0].scatter(pleistocene_interglacial_1208.age_ka, pleistocene_interglacial_1208.d18O_unadj,
               label='Pleistocene Interglacials 1208', marker="+")

    axs[1].plot(sample_data.age_ka, sample_data.difference_d18O, lw=0.5, color='k')
    axs[1].axhline(0, ls='--', color='r')

    axs[1].scatter(pliocene_glacial_difference.age_ka, pliocene_glacial_difference.difference_d18O,
               label='Pliocene Glacials', marker="+")
    axs[1].scatter(pliocene_interglacial_difference.age_ka, pliocene_interglacial_difference.difference_d18O,
               label='Pliocene Interglacials', marker="+")
    axs[1].scatter(pleistocene_glacial_difference.age_ka, pleistocene_glacial_difference.difference_d18O,
               label='Pleistocene Glacials', marker="+")
    axs[1].scatter(pleistocene_interglacial_difference.age_ka, pleistocene_interglacial_difference.difference_d18O,
               label='Pleistocene Interglacials', marker="+")

    axs[0].set(ylabel='{} ({}, VPDB)'.format(r'$\delta^{18}$O', u"\u2030"), xlim=[2370, 3580])
    axs[0].invert_yaxis()
    axs[0].legend()
    axs[1].set(xlabel='Age (ka)', ylabel='{} ({}, VPDB)'.format(r'$\Delta \delta^{18}$O', u"\u2030"), xlim=[2370, 3580])
    axs[1].invert_yaxis()
    axs[1].legend()

    plt.show()


if __name__ == "__main__":
    isotope_stats()
