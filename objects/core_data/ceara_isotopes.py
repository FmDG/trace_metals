import os

from objects.cores import Core


if not os.path.isdir("data/cores"):
    os.chdir('../..')

# Load the Oxygen Isotope datasets
iso_925 = Core("925", "d18O", "ceara_rise", sort="age_ka")
iso_926 = Core("926", "d18O", "ceara_rise", sort="age_ka")
iso_927 = Core("927", "d18O", "ceara_rise", sort="age_ka")
iso_928 = Core("928", "d18O", "ceara_rise", sort="age_ka")
iso_929 = Core("929", "d18O", "ceara_rise", sort="age_ka")

