from objects.core_data.psu import psu_1208, psu_mPWP_1209
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import seaborn as sns
from methods.interpolations.binning_records import binning_multiple_series

def compare_psu(save_fig: bool = False) -> None:
    temp_comparator = binning_multiple_series(
        psu_1208, psu_mPWP_1209,
        names=["1208", "1209"],
        start=2000,
        end=3600,
        fs=2,
        value="temp"
    )
    temp_comparator = temp_comparator.dropna()

    fig, ax = plt.subplots(figsize=(8, 8))
    sns.scatterplot(data=temp_comparator, x="temp_mean_1209", y="temp_mean_1208", hue="age_ka", ax=ax, palette="Spectral", markers="^")
    ax.set(xlabel=r'BWT 1209 ($\degree$C)', ylabel=r'BWT 1208 ($\degree$C)', xlim=[-1.5, 3.5], ylim=[-1.5, 3.5])
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))

    plt.show()


if __name__ == "__main__":
    compare_psu()