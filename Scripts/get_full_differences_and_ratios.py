"""
python get_full_differences_and_ratios.py (operation) (model)

operation -> diff | ratio
model -> GHI | RS
"""
from Modules.data_model import (full_data_model,
                                clear_sky_data)
from Modules.functions import (get_hourly_mean,
                               get_data_between_hours,
                               comparison_operation)
from Modules.params import get_params
from pandas import DataFrame, concat
from os.path import join
from tqdm import tqdm
from sys import argv


params = get_params()
params.update({
    "comparison operation": argv[1],
    "clear sky model": argv[2],
    "file results": "full",
})
results = DataFrame(columns=params["stations"])
clear_sky = clear_sky_data(params)
full_data = full_data_model(params)
dates = clear_sky.get_dates()
bar_dates = tqdm(dates)
for date in bar_dates:
    bar_dates.set_postfix(date=date)
    full_data_daily = full_data.get_date_data(date)
    clear_sky_daily = clear_sky.get_date_data(date)
    results_per_day = DataFrame()
    for station in params["stations"]:
        clear_sky_station = clear_sky_daily[station]
        clear_sky_station = get_hourly_mean(clear_sky_station)
        clear_sky_station = get_data_between_hours(clear_sky_station,
                                                   params)
        full_data_station = full_data_daily[station]
        full_data_station = get_data_between_hours(full_data_station,
                                                   params)
        comparison = comparison_operation(full_data_station,
                                          clear_sky_station,
                                          params["comparison operation"],
                                          fillnan=False)
        results_per_day = concat([results_per_day,
                                  comparison],
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
