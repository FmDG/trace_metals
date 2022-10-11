
from methods.interpolations.generate_interpolations import generate_interpolation
from objects.core_data.isotopes import iso_1209, iso_1208


def glacial_delta(age_min: int = 2400, age_max: int = 2750):

    # We use a simple 1D interpolation, with a density of "freq"
    freq = 0.1

    subset_1208, _ = generate_interpolation(iso_1208, fs=freq, start=age_min, end=age_max, pchip=False)
    subset_1209, _ = generate_interpolation(iso_1209, fs=freq, start=age_min, end=age_max, pchip=False)

    threshold = 3.0
    subset_diff = subset_1208 - subset_1209

    # Determine the difference during glacial and interglacial periods
    diff_glacial = subset_diff[subset_1208 > threshold]
    diff_interglacial = subset_diff[subset_1208 <= threshold]

    return diff_glacial.mean(), diff_glacial.std(), diff_interglacial.mean(), diff_interglacial.std()


if __name__ == "__main__":
    g_mean, g_std, ig_mean, ig_std = glacial_delta()
    print(f"Glacial Dd18O = \t\t{g_mean:.6f} ± {g_std:.6f} \nInterglacial Dd18O = \t{ig_mean:.6f} ± {ig_std:.6f}")

