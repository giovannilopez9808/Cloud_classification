"""
python get_full_data (operation) (sky model)
"""
from Modules.functions import (get_data_between_hours,
                               get_hourly_mean)
from pandas import read_csv, DataFrame, concat
from Modules.data_model import (classification_data,
                                clean_data_model)
from numpy import isnan, array, empty, nan
from Modules.params import get_params
from os.path import join
from tqdm import tqdm
from sys import argv


def nan_vector(vector: DataFrame) -> array:
    header = vector.name
    index = vector.index
    vector = empty(vector.size)
    vector[:] = nan
    vector = DataFrame(vector,
                       index=index,
                       columns=[header])
    return vector


def sort(data: DataFrame) -> DataFrame:
    data = data.sort_values(ascending=False)
    return data


def get_best_similarity_dates(data: DataFrame,
                              params: dict,
                              station: str,
                              date: str) -> list:
    header = f"{station} {date}"
    similarity_vector = similarity[header]
    similarity_vector = sort(similarity_vector)
    similarity_vector = similarity_vector.iloc[1:params["top vectors"]]
    similarity_vector = similarity_vector.index
    return similarity_vector


def get_similarity_vectors(clean_data: clean_data_model,
                           similarity_dates: list,
                           params: dict) -> DataFrame:
    data = DataFrame()
    for station_date in similarity_dates:
        station, date = station_date.split()
        station_data = clean_data.get_data(station,
                                           date)
        data = concat([data,
                       station_data])
    data = get_hourly_mean(data)
    data = get_data_between_hours(data,
                                  params)
    return data


def fill_data(data: DataFrame,
              similarity_data: DataFrame) -> DataFrame:
    for data_index, sim_index in zip(data.index,
                                     similarity_data.index):
        value = data.loc[data_index]
        value = float(value)
        if isnan(value):
            value = similarity_data.loc[sim_index]
            value = float(value)
            data.loc[data_index] = value
    data = DataFrame(data)
    return data


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
            similarity_dates = get_best_similarity_dates(similarity,
                                                         params,
                                                         station,
                                                         date)
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
