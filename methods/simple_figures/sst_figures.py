from objects.core_data.alkenones import sst_846, sst_1208, sst_593, sst_594, sst_806, sst_882, sst_1012, sst_1417

import matplotlib.pyplot as plt

# sst_593 New Zealand
# sst_594  New Zealand
# sst_846  EEP, Near Mexico
# sst_1012  California
# sst_1208  NW Pacific
# sst_1417  Gulf of Alaska
# sst_882 Gulf of Okhotsk
# sst_806 WEP, Near New Guinea

if __name__ == "__main__":
    fig, ax = plt.subplots()

    ax.plot(sst_1417.age_ka, sst_1417.SST, label='1417 (Alaska)')
    ax.plot(sst_1208.age_ka, sst_1208.SST, label='1208')
    ax.plot(sst_882.age_ka, sst_882.SST, label='882 Okhotsk')

    ax.set(xlabel="Age (ka)", ylabel='SST', xlim=[2400, 3600])
    ax.legend()

    plt.show()