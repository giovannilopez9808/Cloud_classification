from Modules.transform_data import transform_data_model
from Modules.functions import get_data_between_hours
from Modules.params import (get_params,
                            get_threshold)
from Modules.data_model import SIMA_model
from pandas import DataFrame
from os.path import join


def get_subparams(station: str,
                  params: dict) -> dict:
    year = params["test"][station]["date"]
    year = year.split("-")[0]
    subparams = params.copy()
    subparams.pop("test")
    subparams.update({
        "date": params["test"][station]["date"],
        "timezone": params["timezone"],
        "station": station,
        "year": year,
    })
    return subparams


def get_station_location(SIMA: SIMA_model,
                         station: str,
                         subparams: dict) -> dict:
    info = SIMA.get_station_info(subparams,
                                 station)
    subparams.update({
        "longitude": info["Longitude"],
        "latitude": info["Latitude"],
    })
    return subparams


params = get_params()
params.update({
    "file graphics": "Reconstruction.png",
    "comparison operation": "ratio",
    "clear sky model": "RS",
    "top vectors": 30,
    "timezone": -6.25,
})
params["threshold"] = get_threshold(params)
for station in params["test"]:
    subparams = get_subparams(station,
                              params)
    SIMA_data = SIMA_model(subparams)
    subparams = get_station_location(SIMA_data,
                                     station,
                                     subparams)
    data = SIMA_data.get_data(subparams["station"],
                              subparams["pollutant"],
                              subparams["date"])
    data = DataFrame(data)
    data = get_data_between_hours(data,
                                  subparams)
    transform_data = transform_data_model(subparams)
    comparison = transform_data.run(data)
