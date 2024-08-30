import numpy as np
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt

from objects.core_data.isotopes import iso_1209, iso_1208, iso_607
from objects.core_data.psu import psu_1208, psu_1209, psu_607


def atlantic_isotope_stats():

    bwt_1208_pliocene = psu_1208.loc[psu_1208.age_ka > 2700].temp.values
    bwt_1209_pliocene = psu_1209.loc[psu_1209.age_ka > 2700].dropna(subset='temp').temp.values
    bwt_607_pliocene = psu_607.loc[psu_607.age_ka > 2700].temp.values

    bwt_1208_pleistocene = psu_1208.loc[psu_1208.age_ka < 2700].temp.values
    bwt_1209_pleistocene = psu_1209.loc[psu_1209.age_ka < 2700].temp.values
    bwt_607_pleistocene = psu_607.loc[psu_607.age_ka < 2700].temp.values

    bwt_all = np.concatenate([psu_1208.temp.values, psu_1209.dropna(subset='temp').temp.values])
    bwt_607 = psu_607.temp.values


    print('T test')
    print("Is the BWT during Pliocene at 607 significantly different to 1209?")
    print(f'Yes, p value = {ttest_ind(bwt_607_pliocene, bwt_1209_pliocene, equal_var=False).pvalue:.4g}')
    print(f'Pliocene 607 Mean: {bwt_607_pliocene.mean():.4f}, Pliocene 1209 Mean: {bwt_1209_pliocene.mean():.4f}')
    print(f'Difference in Pliocene Means: {(bwt_607_pliocene.mean() - bwt_1209_pliocene.mean()):.4f}')
    print("Is the BWT during Pliocene at 607 significantly different to 1208?")
    print(f'Yes, p value = {ttest_ind(bwt_607_pliocene, bwt_1208_pliocene, equal_var=False).pvalue:.4g}')
    print(f'Pliocene 607 Mean: {bwt_607_pliocene.mean():.4f}, Pliocene 1208 Mean: {bwt_1208_pliocene.mean():.4f}')
    print(f'Difference in Pliocene Means: {(bwt_607_pliocene.mean() - bwt_1208_pliocene.mean()):.4f}')

    print("Is the BWT during Pleistocene at 607 significantly different to 1209?")
    print(f'Yes, p value = {ttest_ind(bwt_607_pleistocene, bwt_1209_pleistocene, equal_var=False).pvalue:.4g}')
    print(f'Pleistocene 607 Mean: {bwt_607_pleistocene.mean():.4f}, Pleistocene 1209 Mean: {bwt_1209_pleistocene.mean():.4f}')
    print(f'Difference in Pleistocene Means: {(bwt_607_pleistocene.mean() - bwt_1209_pleistocene.mean()):.4f}')
    print("Is the BWT during Pleistocene at 607 significantly different to 1208?")
    print(f'Yes, p value = {ttest_ind(bwt_607_pleistocene, bwt_1208_pleistocene, equal_var=False).pvalue:.4g}')
    print(f'Pleistocene 607 Mean: {bwt_607_pleistocene.mean():.4f}, Pleistocene 1208 Mean: {bwt_1208_pleistocene.mean():.4f}')
    print(f'Difference in Pleistocene Means: {(bwt_607_pleistocene.mean() - bwt_1208_pleistocene.mean()):.4f}')


    print("Is the BWT at 607 significantly different to both 1208 and 1209?")
    print(f'Yes, p value = {ttest_ind(bwt_607, bwt_all, equal_var=False).pvalue:.4g}')
    print(f'607 Mean: {bwt_607.mean():.4f}, 1209/1208 Mean: {bwt_all.mean():.4f}')
    print(f'Difference in Means: {(bwt_607.mean() - bwt_all.mean()):.4f}')


    fig, axs = plt.subplots(
            nrows = 2,
            ncols = 2,
            sharex = 'all',
            sharey = 'all',
            figsize = (8, 8)
    )

    axs[0, 0].hist(bwt_607_pliocene, alpha=0.2, label='607')
    axs[0, 0].axvline(bwt_607_pliocene.mean(), ls='--', color='tab:blue', label='607 Mean')
    axs[0, 0].hist(bwt_1209_pliocene, alpha=0.2, label='1209')
    axs[0, 0].axvline(bwt_1209_pliocene.mean(), ls='--', color='tab:orange', label='1209 Mean')
    axs[0, 0].set(title='Pliocene')

    axs[1, 0].hist(bwt_607_pleistocene, alpha=0.2, label='607')
    axs[1, 0].axvline(bwt_607_pleistocene.mean(), ls='--', color='tab:blue', label='607 Mean')
    axs[1, 0].hist(bwt_1209_pleistocene, alpha=0.2, label='1208')
    axs[1, 0].axvline(bwt_1209_pleistocene.mean(), ls='--', color='tab:orange', label='1208 Mean')
    axs[1, 0].set(title='Pleistocene')

    axs[0, 1].hist(bwt_607_pliocene, alpha=0.2, label='607')
    axs[0, 1].axvline(bwt_607_pliocene.mean(), ls='--', color='tab:blue', label='607 Mean')
    axs[0, 1].hist(bwt_1208_pliocene, alpha=0.2, label='1209')
    axs[0, 1].axvline(bwt_1208_pliocene.mean(), ls='--', color='tab:orange', label='1209 Mean')
    axs[0, 1].set(title='Pliocene')

    axs[1, 1].hist(bwt_607_pleistocene, alpha=0.2, label='607')
    axs[1, 1].axvline(bwt_607_pleistocene.mean(), ls='--', color='tab:blue', label='607 Mean')
    axs[1, 1].hist(bwt_1208_pleistocene, alpha=0.2, label='1208')
    axs[1, 1].axvline(bwt_1208_pleistocene.mean(), ls='--', color='tab:orange', label='1208 Mean')
    axs[1, 1].set(title='Pliocene')

    for axes in axs:
        for ax in axes:
            ax.legend(ncols=2)
            ax.set(xlabel=r'BWT')

    plt.show()


if __name__ == "__main__":
    atlantic_isotope_stats()