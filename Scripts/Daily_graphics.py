from Modules.data_model import (SIMA_model,
                                clear_sky_data)
from Modules.functions import (get_hourly_mean,
                               mkdir)
from Modules.params import get_params
import matplotlib.pyplot as plt
from pandas import DataFrame
from os.path import join
from tqdm import tqdm


def plot(SIMA: DataFrame,
         Clear_sky: DataFrame,
         params: dict) -> None:
    date = Clear_sky.index[0].date()
    plt.subplots(figsize=(8, 4))
    plt.title(date)
    plt.plot(Clear_sky,
             label=params["dataset"]["title"],
             color="#003049",
             ls="--",
             marker="o")
    plt.plot(SIMA,
             label="SIMA",
             color="#d62828",
             marker="o")
    plt.xlabel("Local time (h)")
    plt.ylabel("Solar Irradiance (W/m$^2$)")
    plt.xticks(Clear_sky.index,
               Clear_sky.index.hour)
    plt.yticks(params["dataset"]["yticks"])
    plt.xlim(Clear_sky.index[6],
             Clear_sky.index[20])
    plt.ylim(params["dataset"]["ylim"][0],
             params["dataset"]["ylim"][1])
    plt.legend(ncol=2,
               frameon=False,
               loc="upper center")
    plt.grid(ls="--",
             color="#000000",
             alpha=0.6)
    plt.tight_layout()
    filename = f"{date}.png"
    filename = join(params["path station graphics"],
                    filename)
    plt.savefig(filename)
    # plt.show()
    plt.clf()
    plt.close("all")


params = get_params()
params.update({
    "path daily graphics": "Daily",
    "clear sky model": "RS",
    "pollutant": "SR",
    "year": 2021,
    "datasets": {
        "RS": {
            "title": "RS model",
            "ylim": [0, 1400],
            "yticks": range(0, 1600, 200),
        },
        "GHI": {
            "title": "GHI$_0$",
            "ylim": [0, 1600],
            "yticks": range(0, 1800, 200),
        }
    },
})
params["dataset"] = params["datasets"][params["clear sky model"]]
SIMA = SIMA_model(params)
clear_sky = clear_sky_data(params)
dates = clear_sky.get_dates()
stations_bar = tqdm(params["stations"])
for station in stations_bar:
    dates_bar = tqdm(dates)
    stations_bar.set_postfix(station=station)
    clear_sky.get_station_data(station)
    SIMA.get_station_data(station,
                          params["pollutant"])
    params["path station graphics"] = join(params["path graphics"],
                                           params["clear sky model"],
                                           params["path daily graphics"],
                                           station)
    mkdir(params["path station graphics"])
    for date in dates_bar:
        if date.year == 2021:
            dates_bar.set_postfix(date=date)
            SIMA_daily = SIMA.get_date_data(date)
            clear_sky_daily = clear_sky.get_date_data(date)
            clear_sky_daily = get_hourly_mean(clear_sky_daily)
            plot(SIMA_daily,
                 clear_sky_daily,
                 params)
