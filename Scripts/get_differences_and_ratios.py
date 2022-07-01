from Modules.data_model import (SIMA_model,
                                clear_sky_data,
                                classification_data)
from Modules.functions import (get_hourly_mean,
                               get_data_between_hours)
from Modules.params import get_params
from pandas import DataFrame, concat
from os.path import join
from numpy import inf
from tqdm import tqdm


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
    # "operation comparison": "ratio",
    "operation comparison": "diff",
    "pollutant": "SR",
    "year": 2021,
})
results = DataFrame(columns=params["stations"])
clear_sky = clear_sky_data(params)
SIMA = SIMA_model()
filename = f"{params['year']}.csv"
filename = join(params["path data"],
                params["SIMA folder"],
                filename)
SIMA.read(filename)
dates = clear_sky.get_dates()
bar_dates = tqdm(dates,
                 bar_format="{bar}|{postfix}")
for date in bar_dates:
    bar_dates.set_postfix(date=date)
    SIMA_daily = SIMA.get_data_date(date)
    clear_sky_daily = clear_sky.get_date_date(date)
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
                                          params["operation comparison"])
        results_per_day = concat([results_per_day,
                                  comparison],
                                 axis=1)
    results = concat([results,
                      results_per_day])
filename = f"{params['operation comparison']}.csv"
filename = join(params['path results'],
                filename)
results.index.name = "Date"
results.to_csv(filename)
