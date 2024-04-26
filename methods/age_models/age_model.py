import pandas as pd
import scipy.interpolate as interpol


def def_age_model(site: str = "1209"):
    """
    This function generates an age model from a linear interpolation of an existing age model and returns that function.
    :param site: Returns the age model for Site 1209 or 1208
    :return: function which is the age model, it works by returning y_new = f(x_new).
    """
    site_data = pd.read_csv("data/cores/{}_cibs.csv".format(site))
    # x is MCD and y is age_ka, the function then gives y_new = f(x_new)
    age_model = interpol.interp1d(x=site_data.mcd, y=site_data.age_ka, fill_value="extrapolate")
    return age_model


def bordiga_age_model():
    site_data = pd.read_csv("data/bordiga_age_model.csv")
    age_model = interpol.interp1d(x=site_data.mbsf, y=site_data.age_ka, fill_value="extrapolate")
    bordiga_data = pd.read_csv("data/comparisons/1209_core_tops_bordiga.csv")
    bordiga_data["age_ka"] = age_model(bordiga_data["mbsf"])
    bordiga_data.to_csv("data/comparisons/1209_core_tops_bordiga_new.csv")

if __name__ == "__main__":
    pass
