from pandas import read_csv, to_datetime, DataFrame, to_timedelta, concat
from Modules.functions import yymmdd2yyyy_mm_dd, hourly_mean, ls, yyyy_mm_dd2yymmdd
from Modules.data_model import SIMA_model, SMARTS_model
from Modules.params import get_params
import matplotlib.pyplot as plt
from os.path import join
from tqdm import tqdm


def get_data_between_hours(data: DataFrame, params: dict) -> DataFrame:
    data = data[data.index.hour >= params["hour initial"]]
    data = data[data.index.hour <= params["hour final"]]
    return data


def comparison_operation(measurement: DataFrame, model: DataFrame, operation: str) -> DataFrame:
    if "diff" == operation:
        comparison = model["Data"]-measurement["SIMA"]
    if "ratio" == operation:
        comparison = model["Data"]/measurement["SIMA"]
    comparison = comparison.reset_index()
    return comparison


params = get_params()
params.update({
    "classification file": "Classification.csv",
    "file results": "ratio.csv",
    "operation comparison": "ratio",
    "station": "Noroeste",
    "pollutant": "SR",
    "hour initial": 7,
    "hour final": 16,
})
filename = join(params["path SMARTS data"],
                params["station"],
                params["classification file"])
classification = read_csv(filename,
                          index_col=0,
                          parse_dates=True)
results = DataFrame()
SIMA = SIMA_model()
SMARTS = SMARTS_model()
year = ""
bar = tqdm(classification.index)
for date in bar:
    date = date.date()
    bar.set_postfix(date=date)
    if year != date.year:
        year = date.year
        file = f"{year}.csv"
        file = join(params["path data"],
                    params["SIMA folder"],
                    file)
        SIMA.read(file)
        SIMA.get_station_data(params["station"],
                              params["pollutant"])
    file = yyyy_mm_dd2yymmdd(date)
    file = f"{file}.txt"
    file = join(params["path SMARTS data"],
                params["station"],
                params["SMARTS DM"],
                file)
    SMARTS_daily = SMARTS.read(file)
    SMARTS_daily = hourly_mean(SMARTS_daily)
    SIMA_daily = SIMA.get_data_date(date)
    SIMA_daily.index = SIMA_daily.index-to_timedelta("00:30:00")
    SIMA_daily = get_data_between_hours(SIMA_daily,
                                        params)
    SIMA_daily.columns = ["SIMA"]
    SMARTS_daily.index = SIMA_daily.index
    comparison = comparison_operation(SIMA_daily,
                                      SMARTS_daily,
                                      params["operation comparison"])
    results = concat([results, comparison[0]],
                     axis=1,
                     ignore_index=True)
filename = join(params["path results"],
                params["file results"])
results.columns = classification.index.date
results.to_csv(filename,
               index=False)
