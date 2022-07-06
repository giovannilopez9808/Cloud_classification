"""
python get_full_data (operation) (sky model)
"""
from Modules.functions import (get_best_similarity_dates,
                               get_similarity_vectors,
                               get_data_between_hours,
                               get_hourly_mean,
                               nan_vector,
                               fill_data,
                               sort,)
from pandas import read_csv, DataFrame, concat
from Modules.data_model import (classification_data,
                                clean_data_model)
from numpy import isnan, array, empty, nan
from Modules.params import get_params
from os.path import join
from tqdm import tqdm
from sys import argv

params = get_params()
params.update({
    "similarity file": "similarity",
    "comparison operation": argv[1],
    "file results": "full_data",
    "clear sky model": argv[2],
    "top vectors": 30,
})
classification = classification_data(params)
clean_data = clean_data_model(params)
dates = clean_data.get_dates()
filename = "{}_{}.csv".format(params["similarity file"],
                              params["comparison operation"])
filename = join(params["path results"],
                params["clear sky model"],
                filename)
similarity = read_csv(filename,
                      index_col=0)
full_data = DataFrame()
bar_dates = tqdm(dates)
for date in bar_dates:
    bar_dates.set_postfix(date=date)
    results_date = DataFrame()
    clean_data_daily = clean_data.get_date_data(date)
    classification_daily = classification.get_date_data(date)
    for station in params["stations"]:
        clean_data_station = clean_data_daily[station]
        classification_station = classification_daily[station]
        classification_station = classification_station[0]
        clean_data_station = get_data_between_hours(clean_data_station,
                                                    params)
        if not isnan(classification_station):
            header = f"{station} {date}"
            similarity_dates = get_best_similarity_dates(similarity,
                                                         params,
                                                         header)
            similarity_vector = get_similarity_vectors(clean_data,
                                                       similarity_dates,
                                                       params)
            clean_data_station = fill_data(clean_data_station,
                                           similarity_vector)
        else:
            clean_data_station = nan_vector(clean_data_station)
        results_date = concat([results_date,
                               clean_data_station],
                              axis=1)
    full_data = concat([full_data,
                        results_date])
full_data.index.name = "Date"
filename = "{}_{}.csv".format(params["file results"],
                              params["comparison operation"])
filename = join(params["path results"],
                params["clear sky model"],
                filename)
full_data.to_csv(filename)
