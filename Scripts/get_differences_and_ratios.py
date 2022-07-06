"""
python get_differences_and_ratios.py (operation) (sky model)
"""
from Modules.data_model import (clear_sky_data,
                                SIMA_model)
from Modules.functions import (get_hourly_mean,
                               get_data_between_hours,
                               comparison_operation,
                               threshold_filter)
from Modules.params import get_params, get_threshold
from pandas import DataFrame, concat
from os.path import join
from tqdm import tqdm
from sys import argv


params = get_params()
params.update({
    "comparison operation": argv[1],
    "clear sky model": argv[2],
    "pollutant": "SR",
    "year": 2021,
})
params["threshold"] = get_threshold(params)
results = DataFrame(columns=params["stations"])
clear_sky = clear_sky_data(params)
SIMA = SIMA_model(params)
dates = clear_sky.get_dates()
bar_dates = tqdm(dates)
for date in bar_dates:
    bar_dates.set_postfix(date=date)
    SIMA_daily = SIMA.get_date_data(date)
    clear_sky_daily = clear_sky.get_date_data(date)
    results_per_day = DataFrame()
    for station in params["stations"]:
        clear_sky_station = clear_sky_daily[station]
        clear_sky_station = get_hourly_mean(clear_sky_station)
        clear_sky_station = get_data_between_hours(clear_sky_station,
                                                   params)
        SIMA_station = SIMA_daily[(station.upper(),
                                   params["pollutant"])]
        SIMA_station = get_data_between_hours(SIMA_station,
                                              params)
        comparison = comparison_operation(SIMA_station,
                                          clear_sky_station,
                                          params["comparison operation"])
        comparison = threshold_filter(comparison,
                                      params)
        results_per_day = concat([results_per_day,
                                  comparison],
                                 axis=1)
    results = concat([results,
                      results_per_day])
filename = f"{params['comparison operation']}.csv"
filename = join(params['path results'],
                params["clear sky model"],
                filename)
results.index.name = "Date"
results.to_csv(filename)
