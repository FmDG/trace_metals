def clean(dataset, subset):
    return dataset.dropna(subset=[subset])


def sort(dataset):
    return dataset.sort_values(by="age_ka")


def clean_and_sort(dataset, subset):
    return sort(clean(dataset, subset))
