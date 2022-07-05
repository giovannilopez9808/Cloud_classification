"""

"""
from Modules.data_model import (full_data_model,
                                clear_sky_data)
from Modules.functions import (get_hourly_mean,
                               mkdir)
from pandas import (to_datetime,
                    DataFrame)
from Modules.params import get_params
import matplotlib.pyplot as plt
from os.path import join
from tqdm import tqdm


def plot(SIMA: DataFrame,
         clear_sky: DataFrame,
         params: dict) -> None:
    date = SIMA.index[0].date()
    plt.subplots(figsize=(8, 4))
    plt.title(date)
    plt.plot(clear_sky,
             label="RS model",
             color="#003049",
             ls="--",
             marker="o")
    plt.plot(SIMA,
             label="SIMA",
             color="#d62828",
             marker="o")
    plt.xlabel("Local time (h)")
    plt.ylabel("Solar Irradiance (W/m$^2$)")
    plt.xticks(SIMA.index,
               SIMA.index.hour)
    plt.yticks(range(0, 1800, 200))
    plt.xlim(SIMA.index[0],
             SIMA.index[-1])
    plt.ylim(0, 1600)
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
    plt.close()


params = get_params()
params.update({
    "path daily graphics": "Daily_full",
    "comparison operation": "diff",
    "clear sky model": "RS",
})
full_data = full_data_model(params)
clear_sky = clear_sky_data(params)
dates = clear_sky.get_dates()
stations_bar = tqdm(params["stations"])
for station in stations_bar:
    dates_bar = tqdm(dates)
    stations_bar.set_postfix(station=station)
    clear_sky.get_station_data(station)
    full_data.get_station_data(station)
    params["path station graphics"] = join(params["path graphics"],
                                           params["clear sky model"],
                                           params["path daily graphics"],
                                           station)
    mkdir(params["path station graphics"])
    for date in dates_bar:
        dates_bar.set_postfix(date=date)
        datetime = to_datetime(date)
        datetime = datetime.date()
        full_data_daily = full_data.get_date_data(date)
        full_data_daily = get_hourly_mean(full_data_daily)
        clear_sky_daily = clear_sky.get_date_data(date)
        clear_sky_daily = get_hourly_mean(clear_sky_daily)
        plot(full_data_daily,
             clear_sky_daily,
             params)
