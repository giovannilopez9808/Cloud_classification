"""
python get_differences_and_ratios.py (operation) (sky model)
"""
from Modules.data_model import (comparison_data,
                                SIMA_model,
                                clear_sky_data)
from Modules.functions import (get_data_between_hours,
                               threshold_filter,
                               get_hourly_mean,
                               clean_data)
from Modules.params import (get_threshold,
                            get_params)
from pandas import DataFrame, concat
from os.path import join
from tqdm import tqdm

params = get_params()
params.update({
    "comparison operation": "ratio",
    "file results": "clean_data",
    "clear sky model": "GHI",
    "pollutant": "SR",
})
params["threshold"] = get_threshold(params)
results = DataFrame(columns=params["stations"])
comparison = comparison_data(params)
clear_sky = clear_sky_data(params)
dates = comparison.get_dates()
bar_dates = tqdm(dates)
year = 0
for date in bar_dates:
    if year != date.year:
        year = date.year
        params["year"] = year
        SIMA = SIMA_model(params)
    bar_dates.set_postfix(date=date)
    SIMA_daily = SIMA.get_date_data(date)
    comparison_daily = comparison.get_date_data(date)
    clear_sky_daily = clear_sky.get_date_data(date)
    results_per_day = DataFrame()
    for station in params["stations"]:
        comparison_station = comparison_daily[station]
        comparison_station = get_data_between_hours(comparison_station,
                                                    params)
        clear_sky_station = clear_sky_daily[station]
        clear_sky_station = get_hourly_mean(clear_sky_station)
        clear_sky_station = get_data_between_hours(clear_sky_station,
                                                   params)
        SIMA_station = SIMA_daily[(station.upper(),
                                   params["pollutant"])]
        SIMA_station = get_data_between_hours(SIMA_station,
                                              params)
        data = clean_data(SIMA_station,
                          clear_sky_station,
                          comparison_station)
        results_per_day = concat([results_per_day,
                                  data],
                                 axis=1)
    results = concat([results,
                      results_per_day])
filename = "{}.csv".format(params["file results"])
filename = join(params['path results'],
                filename)
results.index.name = "Date"
results.to_csv(filename)
