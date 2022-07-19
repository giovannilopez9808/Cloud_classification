from Modules.transform_data import transform_data_model
from Modules.functions import get_data_between_hours
from Modules.clear_sky import clear_sky_model
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
    "timezone": -6.25,
    "datasets": {
        "Sureste2": {
            "date": "2015-02-01",
        },
        "Noreste": {
            "date": "2012-08-10",
        },
        "Noroeste": {
            "date": "2016-03-19",
        },
        "Suroeste": {
            "date": "2017-10-08",
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
    GHI_params = subparams.copy()
    GHI_params["clear sky model"] = "GHI"
    GHI = clear_sky_model()
    GHI = GHI.run(GHI_params)
    if subparams["clear sky model"] == "RS":
        RS = clear_sky_model()
        RS = RS.run(subparams)
    ax.plot(GHI,
            color="#80b918")
    ax.plot(RS,
            color="#bf0603")
    ax.plot(transform_data.clear_data,
            color="#f72585",
            marker=".")
    ax.plot(transform_data.full_data,
            color="#480ca8",
            ls="--")
    date = subparams["date"]
    fig.text(0.005, 0.37,
             "Solar irradiance (W/m$^2$)",
             horizontalalignment='left',
             rotation='vertical',
             fontsize=13)
    fig.text(0.46, 0.01,
             "Local time (h)",
             fontsize=13)
    ax.set_title(f"{station} {date}")
    ax.set_xticks(data.index)
    ax.set_xticklabels(data.index.hour)
    ax.set_xlim(data.index[5],
                data.index[21])
    ax.grid(ls="--",
            color="#000000",
            alpha=0.6)
ax.set_ylim(0, 1400)
plt.tight_layout(pad=2.1)
plt.savefig("test.png",
            dpi=400)
