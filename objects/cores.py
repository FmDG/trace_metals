from pandas import read_csv


class Core:

    def __init__(self, site: str, method: str, location: str = "cores", sort: str = "age_ka", drop: str = None):
        self.site = site
        self.method = method
        self.data = self.get_data(location, sort, drop)

    def get_data(self, location: str, sort: str, drop: str = None):
        loc = "data/{}/{}.csv".format(location, "{}_{}".format(self.site, self.method))
        if drop is None:
            return read_csv(loc).sort_values(by=sort)
        else:
            return read_csv(loc).sort_values(by=sort).dropna(subset=drop)

