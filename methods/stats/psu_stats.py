from methods.simple_figures.core_tops import temp_from_mgca
from objects.misc.mis_boundaries import mis_boundaries
from objects.core_data.psu import psu_1209, psu_1208

from scipy.stats import kstest, ttest_ind
import matplotlib.pyplot as plt

psu_1208['glacial'] = False
psu_1209['glacial'] = False
for _, row in mis_boundaries.iterrows():
    lower_age = row["age_start"]
    upper_age = row['age_end']
    if row["glacial"] == "glacial":
        psu_1208.loc[(psu_1208.age_ka >= lower_age) & (psu_1208.age_ka < upper_age), 'glacial'] = True
        psu_1209.loc[(psu_1209.age_ka >= lower_age) & (psu_1209.age_ka < upper_age), 'glacial'] = True


psu_1208['pliocene'] = False
psu_1209['pliocene'] = False
psu_1208.loc[psu_1208.age_ka > 2700, 'pliocene'] = True
psu_1209.loc[psu_1209.age_ka > 2700, 'pliocene'] = True

def bwt_stats():

    pleistocene_glacial_1208 = psu_1208.loc[(psu_1208.pliocene == False) & psu_1208.glacial].temp.values
    pleistocene_glacial_1209 = psu_1209.loc[(psu_1209.pliocene == False) & psu_1209.glacial].temp.values
    pleistocene_interglacial_1208 = psu_1208.loc[
        (psu_1208.pliocene == False) & (psu_1208.glacial == False)].temp.values
    pleistocene_interglacial_1209 = psu_1209.loc[
        (psu_1209.pliocene == False) & (psu_1209.glacial == False)].temp.values

    pliocene_1208 = psu_1208.loc[(psu_1208.age_ka < 3000) & (psu_1208.age_ka > 2700)].temp.values
    pliocene_1209 = psu_1209.loc[(psu_1209.age_ka < 3000) & (psu_1209.age_ka > 2700)].dropna(subset='temp').temp.values



    print('Welch T-test')
    print("Is the BWT during Pleistocene glacials significantly different at 1208 compared to 1209?")
    print(f'No, p value = {ttest_ind(pleistocene_glacial_1208, pleistocene_glacial_1209, equal_var=False).pvalue:.4g}')
    print(f'Pleistocene Glacial 1208 Mean: {pleistocene_glacial_1208.mean():.4f}, Pleistocene Glacial 1209 Mean: {pleistocene_glacial_1209.mean():.4f}')
    print(f'Difference in Pleistocene Glacial Means: {(pleistocene_glacial_1208.mean() - pleistocene_glacial_1209.mean()):.4f}')
    print("Is the BWT during Pleistocene interglacials significantly different at 1208 compared to 1209?")
    print(f'Yes, p value = {ttest_ind(pleistocene_interglacial_1208, pleistocene_interglacial_1209, equal_var=False).pvalue:.4g}')
    print(f'Pleistocene Interglacial 1208 Mean: {pleistocene_interglacial_1208.mean():.4f}, Pleistocene Interglacial 1209 Mean: {pleistocene_interglacial_1209.mean():.4f}')
    print(f'Difference in Pleistocene Interglacial Means: {(pleistocene_interglacial_1208.mean() - pleistocene_interglacial_1209.mean()):.4f}')

    print("Is the BWT at 1209 during Pleistocene significantly different during glacials and interglacials?")
    print(f'No, p value = {ttest_ind(pleistocene_glacial_1209, pleistocene_interglacial_1209, equal_var=False).pvalue:.4g}')
    print(f'Pleistocene Glacial 1209 Mean: {pleistocene_glacial_1209.mean():.4f}, Pleistocene Interglacial 1209 Mean: {pleistocene_interglacial_1209.mean():.4f}')
    print(f'Difference in 1209 Pleistocene Means: {(pleistocene_glacial_1209.mean() - pleistocene_interglacial_1209.mean()):.4f}')
    print("Is the BWT at 1208 during Pleistocene significantly different during glacials and interglacials?")
    print(f'Yes, p value = {ttest_ind(pleistocene_glacial_1208, pleistocene_interglacial_1208, equal_var=False).pvalue:.4g}')
    print(f'Pleistocene Glacial 1208 Mean: {pleistocene_glacial_1208.mean():.4f}, Pleistocene Interglacial 1208 Mean: {pleistocene_interglacial_1208.mean():.4f}')
    print(f'Difference in Pleistocene 1208 Means: {(pleistocene_glacial_1208.mean() - pleistocene_interglacial_1208.mean()):.4f}')


    print("Is the BWT at 1208 during Late Pliocene different to 1209?")
    print(f'Yes, p value = {ttest_ind(pliocene_1208, pliocene_1209, equal_var=False).pvalue:.4g}')
    print(f'Late Pliocene 1208 Mean: {pliocene_1208.mean():.4f}, Late Pliocene 1209 Mean: {pliocene_1209.mean():.4f}')
    print(f'Difference in Pliocene Means: {(pliocene_1208.mean() - pliocene_1209.mean()):.4f}')


    print("Is the BWT at 1208 during Late Pliocene different to Pleistocene?")
    print(f'Yes, p value = {ttest_ind(pliocene_1208, pleistocene_glacial_1208, equal_var=False).pvalue:.4g}')
    print(f'Late Pliocene 1208 Mean: {pliocene_1208.mean():.4f}, Pleistocene Glacial 1208 Mean: {pleistocene_glacial_1208.mean():.4f}')
    print(f'Difference in Means: {(pliocene_1208.mean() - pleistocene_glacial_1208.mean()):.4f}')

    print("Is the BWT at 1209 during Late Pliocene different to Pleistocene?")
    print(f'Yes, p value = {ttest_ind(pliocene_1209, pleistocene_glacial_1209, equal_var=False).pvalue:.4g}')
    print(f'Late Pliocene 1209 Mean: {pliocene_1209.mean():.4f}, Pleistocene Glacial 1209 Mean: {pleistocene_glacial_1209.mean():.4f}')
    print(f'Difference in Means: {(pliocene_1209.mean() - pleistocene_glacial_1209.mean()):.4f}')



    fig, axs = plt.subplots(
            ncols = 2,
            sharex = 'all',
            sharey = 'all',
            figsize = (10, 5)
    )

    axs[0].hist(pleistocene_glacial_1208, alpha=0.2, label='1208 Pleistocene Glacials')
    axs[0].axvline(pleistocene_glacial_1208.mean(), ls='--', color='tab:blue', label='1208 Mean')
    axs[0].hist(pleistocene_glacial_1209, alpha=0.2, label='1209 Pleistocene Glacials')
    axs[0].axvline(pleistocene_glacial_1209.mean(), ls='--', color='tab:orange', label='1209 Mean')

    axs[1].hist(pleistocene_interglacial_1208, alpha=0.2, label='1208 Pleistocene Interglacials')
    axs[1].axvline(pleistocene_interglacial_1208.mean(), ls='--', color='tab:blue', label='1208 Mean')
    axs[1].hist(pleistocene_interglacial_1209, alpha=0.2, label='1209 Pleistocene Interglacials')
    axs[1].axvline(pleistocene_interglacial_1209.mean(), ls='--', color='tab:orange', label='1209 Mean')

    for ax in axs:
        ax.legend(ncols=2)
        ax.set(xlabel=r'BWT')

    fig, ax = plt.subplots()

    ax.hist(pliocene_1208, alpha=0.2, label='1208 Pliocene')
    ax.axvline(pliocene_1208.mean(), ls='--', color='tab:blue', label='1208 Mean')
    ax.hist(pliocene_1209, alpha=0.2, label='1209 Pliocene')
    ax.axvline(pliocene_1209.mean(), ls='--', color='tab:orange', label='1209 Mean')

    ax.legend()

    plt.show()


def seawater_stats():

    pleistocene_glacial_1208 = psu_1208.loc[(psu_1208.pliocene == False) & psu_1208.glacial].d18O_sw.values
    pleistocene_glacial_1209 = psu_1209.loc[(psu_1209.pliocene == False) & psu_1209.glacial].d18O_sw.values
    pleistocene_interglacial_1208 = psu_1208.loc[
        (psu_1208.pliocene == False) & (psu_1208.glacial == False)].d18O_sw.values
    pleistocene_interglacial_1209 = psu_1209.loc[
        (psu_1209.pliocene == False) & (psu_1209.glacial == False)].d18O_sw.values

    pliocene_1208 = psu_1208.loc[(psu_1208.age_ka < 3000) & (psu_1208.age_ka > 2700)].d18O_sw.values
    pliocene_1209 = psu_1209.loc[(psu_1209.age_ka < 3000) & (psu_1209.age_ka > 2700)].dropna(subset='d18O_sw').d18O_sw.values



    print('Welch T-test')
    print("Is the d18O_sw during Pleistocene glacials significantly different at 1208 compared to 1209?")
    print(f'No, p value = {ttest_ind(pleistocene_glacial_1208, pleistocene_glacial_1209, equal_var=False).pvalue:.4g}')
    print(f'Pleistocene Glacial 1208 Mean: {pleistocene_glacial_1208.mean():.4f}, Pleistocene Glacial 1209 Mean: {pleistocene_glacial_1209.mean():.4f}')
    print(f'Difference in Pleistocene Glacial Means: {(pleistocene_glacial_1208.mean() - pleistocene_glacial_1209.mean()):.4f}')
    print("Is the d18O_sw during Pleistocene interglacials significantly different at 1208 compared to 1209?")
    print(f'Yes, p value = {ttest_ind(pleistocene_interglacial_1208, pleistocene_interglacial_1209, equal_var=False).pvalue:.4g}')
    print(f'Pleistocene Interglacial 1208 Mean: {pleistocene_interglacial_1208.mean():.4f}, Pleistocene Interglacial 1209 Mean: {pleistocene_interglacial_1209.mean():.4f}')
    print(f'Difference in Pleistocene Interglacial Means: {(pleistocene_interglacial_1208.mean() - pleistocene_interglacial_1209.mean()):.4f}')

    print("Is the d18O_sw at 1208 during Late Pliocene different to 1209?")
    print(f'Yes, p value = {ttest_ind(pliocene_1208, pliocene_1209, equal_var=False).pvalue:.4g}')
    print(f'Late Pliocene 1208 Mean: {pliocene_1208.mean():.4f}, Late Pliocene 1209 Mean: {pliocene_1209.mean():.4f}')
    print(f'Difference in Pliocene Means: {(pliocene_1208.mean() - pliocene_1209.mean()):.4f}')


    fig, axs = plt.subplots(
            ncols = 2,
            sharex = 'all',
            sharey = 'all',
            figsize = (10, 5)
    )

    axs[0].hist(pleistocene_glacial_1208, alpha=0.2, label='1208 Pleistocene Glacials')
    axs[0].axvline(pleistocene_glacial_1208.mean(), ls='--', color='tab:blue', label='1208 Mean')
    axs[0].hist(pleistocene_glacial_1209, alpha=0.2, label='1209 Pleistocene Glacials')
    axs[0].axvline(pleistocene_glacial_1209.mean(), ls='--', color='tab:orange', label='1209 Mean')

    axs[1].hist(pleistocene_interglacial_1208, alpha=0.2, label='1208 Pleistocene Interglacials')
    axs[1].axvline(pleistocene_interglacial_1208.mean(), ls='--', color='tab:blue', label='1208 Mean')
    axs[1].hist(pleistocene_interglacial_1209, alpha=0.2, label='1209 Pleistocene Interglacials')
    axs[1].axvline(pleistocene_interglacial_1209.mean(), ls='--', color='tab:orange', label='1209 Mean')

    for ax in axs:
        ax.legend(ncols=2)
        ax.set(xlabel=r'd18O_sw')

    fig, ax = plt.subplots()

    ax.hist(pliocene_1208, alpha=0.2, label='1208 Pliocene')
    ax.axvline(pliocene_1208.mean(), ls='--', color='tab:blue', label='1208 Mean')
    ax.hist(pliocene_1209, alpha=0.2, label='1209 Pliocene')
    ax.axvline(pliocene_1209.mean(), ls='--', color='tab:orange', label='1209 Mean')

    ax.legend()

    plt.show()

if __name__ == "__main__":
    seawater_stats()