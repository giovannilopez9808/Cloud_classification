from Modules.transform_data import transform_data_model
from Modules.functions import get_data_between_hours
from Modules.params import (get_params,
                            get_threshold)
from Modules.data_model import SIMA_model
import matplotlib.pyplot as plt
from pandas import DataFrame


def get_subparams(station: str,
                  params: dict) -> dict:
    year = params["datasets"][station]["date"]
    year = year.split("-")[0]
    subparams = params.copy()
    subparams.pop("datasets")
    subparams.update({
        "date": params["datasets"][station]["date"],
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
    "comparison operation": "ratio",
    "clear sky model": "RS",
    "top vectors": 30,
    "pollutant": "SR",
    "timezone": -5,
    "datasets": {
        "Sureste2": {
            "date": "2021-07-22",
        },
        "Noreste": {
            "date": "2019-01-20",
        },
        "Noroeste": {
            "date": "2021-04-09",
        },
        "Suroeste": {
            "date": "2019-11-22",
        },
    },
})
params["threshold"] = get_threshold(params)
fig, axs = plt.subplots(2, 2,
                        # sharex=True,
                        sharey=True,
                        figsize=(12, 8))
axs = axs.flatten()
for station, ax in zip(params["datasets"],
                       axs):
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
    ax.plot(transform_data.clear_data,
            color="#f72585")
    ax.plot(transform_data.full_data,
            color="#480ca8",
            ls="--")
    date = subparams["date"]
    ax.set_title(f"{station} {date}")
    ax.set_xticks(data.index)
    ax.set_xticklabels(data.index.hour)
    ax.set_xlim(data.index[5],
                data.index[21])
    ax.grid(ls="--",
            color="#000000",
            alpha=0.6)
ax.set_ylim(0, 900)
plt.tight_layout()
plt.savefig("test.png",
            dpi=400)
