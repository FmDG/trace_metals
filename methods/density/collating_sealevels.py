import pandas as pd

from objects.core_data.trace_elements import te_1208, te_1209
from objects.core_data.isotopes import iso_1208, iso_1209
from objects.misc.sea_level import sea_level


def collate_sea_level_te(site: str = '1209') -> None:

    entries = []

    if site == '1209':
        mg_data, d18o_data = te_1209, iso_1209
    elif site == '1208':
        mg_data, d18o_data = te_1208, iso_1208
    else:
        raise ValueError("Site must be one of '1208' or '1209'")

    for _, value in mg_data.iterrows():
        sl_data = sea_level.iloc[(sea_level['age_ka'] - value.age_ka).abs().argsort()[:1]]
        iso_data = d18o_data.iloc[(d18o_data['age_ka'] - value.age_ka).abs().argsort()[:1]]
        entries.append(
            {'age_ka': value.age_ka, 'd18O': iso_data.d18O_unadj.values[0], 'mgca': value.MgCa, 'rsl': sl_data.SL_m.values[0]}
        )

    export_dataset = pd.DataFrame.from_records(entries)

    export_dataset.to_csv('data/{}_compiled_for_PSU_data.csv'.format(site))


if __name__ == "__main__":
    collate_sea_level_te('1208')