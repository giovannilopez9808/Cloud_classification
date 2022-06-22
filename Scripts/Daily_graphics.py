from pandas import read_csv, to_datetime, DataFrame, to_timedelta
from Modules.data_model import SIMA_model, SMARTS_model
from Modules.functions import yymmdd2yyyy_mm_dd
from Modules.params import get_params
import matplotlib.pyplot as plt
from os.path import join
from tqdm import tqdm


def plot(SMARTS: DataFrame, SIMA: DataFrame, params: dict) -> None:
    date = SIMA.index[0].date()
    plt.subplots(figsize=(8, 4))
    plt.title(date)
    hours = SIMA[7:17].index+to_timedelta("00:15:00")
    SMARTS.index = hours
    SIMA.index = SIMA.index-to_timedelta("00:30:00")
    plt.plot(hours,
             SMARTS,
             label="SMARTS model",
             color="#003049",
             ls="--",
             marker="o")
    plt.plot(SIMA,
             label="SIMA",
             color="#d62828",
             marker="o")
    plt.xlabel("Local time (h)")
    plt.ylabel("Irradiance solar (W/m$^2$)")
    plt.xticks(SIMA.index,
               SIMA.index.hour)
    plt.yticks(range(0, 1400, 200))
    plt.xlim(SIMA.index[7],
             SIMA.index[18])
    plt.ylim(0, 1200)
    plt.legend(ncol=2,
               frameon=False,
               loc="upper center")
    plt.grid(ls="--",
             color="#000000",
             alpha=0.6)
    plt.tight_layout()
    filename = f"{date}.png"
    filename = join(params["path graphics"],
                    filename)
    plt.savefig(filename)
    plt.close()


def hourly_mean(data: DataFrame) -> DataFrame:
    hours = data.index.hour
    data = data.groupby(hours).mean()
    return data


params = get_params()
params.update({
    "path SIMA data": "../Data/SIMA",
    "path station data": "SMARTS/Data/",
    "path graphics": "../Graphics/Daily",
    "path SMARTS": "Results_DM",
    "station": "Noroeste",
    "pollutant": "SR",
    "file data": "datos.txt",
    "null threshold": 14,
})


SIMA = SIMA_model()
SMARTS = SMARTS_model()
filename = join(params["path station data"],
                params["station"],
                params["file data"])
data = read_csv(filename)
data["Fecha"] = data["Date"].apply(yymmdd2yyyy_mm_dd)

year = ""
bar = tqdm(data.index)
for index in bar:
    if year != data["year"][index]:
        year = data["year"][index]
        filename = f"{year}.csv"
        filename = join(params["path SIMA data"],
                        filename)
        SIMA.read(filename)
        SIMA.get_station_data(params["station"],
                              params["pollutant"])
    date = data["Fecha"][index]
    bar.set_postfix(date=date)
    SIMA_daily = SIMA.get_data_date(date)
    n_null = int(SIMA_daily.isnull().sum())
    if n_null < params["null threshold"]:
        filename = f"{data['Date'][index]}.txt"
        filename = join(params["path station data"],
                        params["station"],
                        params["path SMARTS"],
                        filename)
        SMARTS_daily = SMARTS.read(filename)
        SMARTS_daily = hourly_mean(SMARTS_daily)
        plot(SMARTS_daily,
             SIMA_daily,
             params)
