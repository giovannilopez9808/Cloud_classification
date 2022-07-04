from Modules.data_model import (classification_data,
                                full_data_model,
                                clear_sky_data)
from Modules.functions import (get_hourly_mean,
                               get_data_between_hours)
from Modules.params import get_params
from pandas import DataFrame, concat
from os.path import join
from numpy import inf
from tqdm import tqdm
from sys import exit


def comparison_operation(measurement: DataFrame,
                         model: DataFrame,
                         operation: str) -> DataFrame:
    index = model.index
    station = model.name
    model = model.to_numpy()
    measurement = measurement.to_numpy()
    if "diff" == operation:
        comparison = model-measurement
    if "ratio" == operation:
        comparison = measurement/model
        comparison[comparison == inf] = 0
    comparison = DataFrame(comparison,
                           index=index,
                           columns=[station])
    return comparison


params = get_params()
params.update({
    "comparison operation": "diff",
    "clear sky model": "RS",
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
        fill_data_station = get_data_between_hours(full_data_station,
                                                   params)
        comparison = comparison_operation(full_data_station,
                                          clear_sky_station,
                                          params["comparison operation"])

        results_per_day = concat([results_per_day,
                                  comparison],
                                 axis=1)
        print(results_per_day)
        exit(0)
    results = concat([results,
                      results_per_day])
filename = "{}_{}.csv".format(params["file results"],
                              params["comparison operation"])
filename = join(params['path results'],
                params["clear sky model"],
                filename)
results.index.name = "Date"
results.to_csv(filename)
