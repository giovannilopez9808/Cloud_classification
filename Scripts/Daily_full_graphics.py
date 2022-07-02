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
         GHI: DataFrame,
         RS: DataFrame,
         params: dict) -> None:
    date = SIMA.index[0].date()
    plt.subplots(figsize=(8, 4))
    plt.title(date)
    plt.plot(GHI,
             label="GHI$_0$",
             color="#003049",
             ls="--",
             marker="o")
    plt.plot(RS,
             label="RS",
             color="#e85d04",
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
    "file data": "data_full.csv",
    "clear sky models": ["GHI",
                         "RS"],
    "null threshold": 14,
    "pollutant": "SR",
    "year": 2021,
})
filename = join(params["path results"],
                params["clear sky model"],
                params["file data"])
data = read_csv(filename,
                index_col=0,
                parse_dates=True)
params["clear sky model"] = params["cler sky models"][0]
GHI = clear_sky_data(params)
params["clear sky model"] = params["cler sky models"][1]
RS = clear_sky_data(params)
dates = GHI.get_dates()
stations_bar = tqdm(params["stations"])
for station in stations_bar:
    dates_bar = tqdm(dates)
    stations_bar.set_postfix(station=station)
    GHI.get_station_data(station)
    RS.get_station_data(station)
    station_data = data[station]
    params["path station graphics"] = join(params["path graphics"],
                                           params["clear sky model"],
                                           params["path daily graphics"],
                                           station)
    mkdir(params["path station graphics"])
    for date in dates_bar:
        dates_bar.set_postfix(date=date)
        datetime = to_datetime(date)
        datetime = datetime.date()
        index = station_data.index.date == datetime
        SIMA_daily = station_data[index]
        GHI_daily = GHI.get_date_date(date)
        GHI_daily = get_hourly_mean(GHI_daily)
        RS_daily = GHI.get_date_date(date)
        RS_daily = get_hourly_mean(RS_daily)
        plot(SIMA_daily,
             GHI_daily,
             RS_daily,
             params)
