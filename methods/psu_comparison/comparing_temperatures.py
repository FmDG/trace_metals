from objects.core_data.psu import psu_1208, psu_mPWP_1209
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from methods.interpolations.binning_records import binning_multiple_series
from methods.interpolations.generate_interpolations import linear_relations

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

    fig, ax = plt.subplots(
        figsize=(8, 8)
    )

    pre_iNHG = temp_comparator[temp_comparator.age_ka > 2700]
    post_iNHG = temp_comparator[temp_comparator.age_ka < 2700.1]

    ax.scatter(post_iNHG.temp_mean_1209, post_iNHG.temp_mean_1208, label="post 2.7 Ma", marker="o", s=20)
    ax.scatter(pre_iNHG.temp_mean_1209, pre_iNHG.temp_mean_1208, label="pre 2.7 Ma", marker="^", s=20)
    ax.set(xlabel=r'BWT 1209 ($\degree$C)', ylabel=r'BWT 1208 ($\degree$C)')
    ax.axis("equal")
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))

    ax = linear_relations(ax, temp_comparator, "temp_mean_1208", "temp_mean_1209", True)
    ax.legend()

    if save_fig:
        plt.savefig("figures/psu_plots/BWT_crossplot.png", dpi=300)
    else:
        plt.show()


if __name__ == "__main__":
    compare_psu()