from Modules.transform_data import transform_data_model
from Modules.functions import get_data_between_hours
from Modules.clear_sky import clear_sky_model
from pandas import (to_timedelta,
                    to_datetime,
                    DataFrame)
from Modules.data_model import SIMA_model
from Modules.params import get_params
import matplotlib.pyplot as plt
from os.path import join
from numpy import isnan


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


def get_index(clear_data: DataFrame,
              full_data: DataFrame) -> DataFrame:
    data = DataFrame(index=clear_data.index,
                     columns=["data"])
    index = clear_data[isnan(clear_data["H0"])]
    index = index.index
    new_index = set()
    for hour in index:
        date = to_datetime(hour)
        for update in range(-1, 2):
            hour_u = date + to_timedelta(update,
                                         unit="H")
            new_index.add(hour_u)
    new_index = sorted(list(new_index))
    data.loc[new_index] = full_data.loc[new_index]
    return data


params = get_params()
params.update({
    "file graphics": "Reconstruction.png",
    "comparison operation": "ratio",
    "clear sky model": "RS",
    "top vectors": 10,
    "timezone": -6.25,
})
fig, axs = plt.subplots(2, 2,
                        # sharex=True,
                        sharey=True,
                        figsize=(12, 6))
axs = axs.flatten()
for station, ax in zip(params["test"],
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
    reconstruction = get_index(transform_data.clear_data,
                               transform_data.full_data)
    GHI_params = subparams.copy()
    GHI_params["clear sky model"] = "GHI"
    GHI = clear_sky_model()
    GHI = GHI.run(GHI_params)
    if subparams["clear sky model"] == "RS":
        RS = clear_sky_model()
        RS = RS.run(subparams)
    ax.plot(GHI,
            label="modelo GHI$_0$",
            color="#6a040f")
    ax.plot(RS,
            label="modelo RS",
            color="#007f5f")
    ax.plot(transform_data.clear_data,
            label="SIMA",
            color="#b5179e")
    ax.plot(reconstruction,
            color="#6a994e",
            label="Reconstrucción",
            ls="--")
    date = subparams["date"]
    fig.text(0.005, 0.37,
             "Irradiancia solar (W/m$^2$)",
             horizontalalignment='left',
             rotation='vertical',
             fontsize=13)
    fig.text(0.46, 0.01,
             "Hora local",
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
handles, labels = ax.get_legend_handles_labels()
fig.legend(handles,
           labels,
           ncol=4,
           frameon=False,
           loc='upper center')
plt.tight_layout(pad=2.2)
filename = join(params["path graphics"],
                params["file graphics"])
plt.savefig(filename,
            dpi=400)
