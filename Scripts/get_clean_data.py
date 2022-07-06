"""
python get_differences_and_ratios.py (operation) (sky model)
"""
from Modules.data_model import (comparison_data,
                                SIMA_model)
from Modules.functions import get_data_between_hours
from Modules.params import get_params
from pandas import DataFrame, concat
from numpy import isnan, nan
from os.path import join
from tqdm import tqdm
from sys import argv


def clean_data(data: DataFrame,
               comparison: DataFrame,
               params: dict) -> DataFrame:
    operation = params["comparison operation"]
    index = list(data.index)
    header = comparison.name
    data = data.to_numpy()
    comparison = comparison.to_numpy()
    if operation == "ratio":
        data[comparison == 0] = 0
    data[isnan(comparison)] = nan
    data = DataFrame(data,
                     index=index,
                     columns=[header])
    return data


params = get_params()
params.update({
    "comparison operation": argv[1],
    "file results": "clean_data",
    "clear sky model": argv[2],
    "pollutant": "SR",
    "year": 2021,
})
results = DataFrame(columns=params["stations"])
comparison = comparison_data(params)
SIMA = SIMA_model(params)
dates = comparison.get_dates()
bar_dates = tqdm(dates)
for date in bar_dates:
    bar_dates.set_postfix(date=date)
    SIMA_daily = SIMA.get_date_data(date)
    comparison_daily = comparison.get_date_data(date)
    results_per_day = DataFrame()
    for station in params["stations"]:
        comparison_station = comparison_daily[station]
        comparison_station = get_data_between_hours(comparison_station,
                                                    params)
        SIMA_station = SIMA_daily[(station.upper(),
                                   params["pollutant"])]
        SIMA_station = get_data_between_hours(SIMA_station,
                                              params)
        data = clean_data(SIMA_station,
                          comparison_station,
                          params)
        results_per_day = concat([results_per_day,
                                  data],
                                 axis=1)
    results = concat([results,
                      results_per_day])
filename = "{}_{}.csv".format(params["file results"],
                              params["comparison operation"])
filename = join(params['path results'],
                params["clear sky model"],
                filename)
results.index.name = "Date"
results.to_csv(filename)
