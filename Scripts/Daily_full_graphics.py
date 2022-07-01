from Modules.data_model import (SIMA_model,
                                clear_sky_data)
from Modules.functions import (get_hourly_mean,
                               mkdir)
from pandas import (read_csv,
                    to_datetime,
                    DataFrame,
                    to_timedelta)
from Modules.params import get_params
import matplotlib.pyplot as plt
from os.path import join
from tqdm import tqdm


def plot(SIMA: DataFrame,
         Clear_sky: DataFrame,
         params: dict) -> None:
    date = SIMA.index[0].date()
    plt.subplots(figsize=(8, 4))
    plt.title(date)
    plt.plot(Clear_sky,
             label="GHI$_0$",
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
    "path graphics": "../Graphics/Daily_full",
    "file data": "data_full.csv",
    "null threshold": 14,
    "pollutant": "SR",
    "year": 2021,
})
filename = join(params["path results"],
                params["file data"])
data = read_csv(filename,
                index_col=0,
                parse_dates=True)
clear_sky = clear_sky_data(params)
dates = clear_sky.get_dates()
stations_bar = tqdm(params["stations"])
for station in stations_bar:
    dates_bar = tqdm(dates)
    stations_bar.set_postfix(station=station)
    clear_sky.get_station_data(station)
    station_data = data[station]
    params["path station graphics"] = join(params["path graphics"],
                                           station)
    mkdir(params["path station graphics"])
    for date in dates_bar:
        dates_bar.set_postfix(date=date)
        datetime = to_datetime(date)
        datetime = datetime.date()
        index = station_data.index.date == datetime
        SIMA_daily = station_data[index]
        clear_sky_daily = clear_sky.get_date_date(date)
        clear_sky_daily = get_hourly_mean(clear_sky_daily)
        plot(SIMA_daily,
             clear_sky_daily,
             params)
