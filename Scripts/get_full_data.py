from Modules.functions import (get_data_between_hours,
                               get_hourly_mean)
from pandas import read_csv, DataFrame, concat
from Modules.data_model import SIMA_model
from Modules.params import get_params
from os.path import join
from tqdm import tqdm


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
    similarity_vector = similarity_vector.iloc[:params["top vectors"]]
    similarity_vector = similarity_vector.index
    return similarity_vector


def get_similarity_vectors(SIMA: SIMA_model,
                           similarity_dates: list,
                           params: dict) -> DataFrame:
    data = DataFrame()
    for station_date in similarity_dates:
        station, date = station_date.split()
        station_data = SIMA.get_data(station,
                                     params["pollutant"],
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
        if value < 0:
            value = similarity_data.loc[sim_index]
            value = float(value)
            data.loc[data_index] = value
    return data


params = get_params()
params.update({
    "similarity file": "similarity",
    "file results": "full_data",
    "clear sky model": "GHI",
    "operation": "diff",
    "pollutant": "SR",
    "year": 2021,
    "top vectors": 20,
})
SIMA = SIMA_model()
filename = f"{params['year']}.csv"
filename = join(params["path data"],
                params["SIMA folder"],
                filename)
SIMA.read(filename)
SIMA.data = SIMA.data.fillna(-1)
dates = SIMA.get_dates()
filename = "{}_{}.csv".format(params["similarity file"],
                              params["operation"])
filename = join(params["path results"],
                params["clear sky model"],
                filename)
similarity = read_csv(filename,
                      index_col=0)
full_data = DataFrame()
bar_stations = tqdm(params["stations"])
for station in bar_stations:
    bar_stations.set_postfix(station=station)
    results_per_station = DataFrame()
    SIMA.get_station_data(station,
                          params["pollutant"])
    bar_dates = tqdm(dates)
    for date in bar_dates:
        bar_dates.set_postfix(date=date)
        similarity_dates = get_best_similarity_dates(similarity,
                                                     params,
                                                     station,
                                                     date)
        similarity_vector = get_similarity_vectors(SIMA,
                                                   similarity_dates,
                                                   params)
        vector = SIMA.get_date_data(date)
        vector = get_data_between_hours(vector,
                                        params)
        vector = fill_data(vector,
                           similarity_vector)
        results_per_station = concat([results_per_station,
                                      vector])
    results_per_station.columns = [station]
    full_data = concat([full_data,
                        results_per_station],
                       axis=1)
full_data.index.name = "Date"
filename = "{}_{}.csv".format(params["file results"],
                              params["operation"])
filename = join(params["path results"],
                params["clear sky model"],
                filename)
full_data.to_csv(filename)
