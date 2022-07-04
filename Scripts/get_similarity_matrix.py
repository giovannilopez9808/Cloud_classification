from Modules.data_model import (comparison_data,
                                SIMA_model)
from Modules.functions import get_data_between_hours
from Modules.params import get_params
from pandas import DataFrame, concat
from numpy import nan, array, dot
from numpy.linalg import norm
from os.path import join
from tqdm import tqdm


def get_vector(data: DataFrame,
               station: str,
               date: str) -> array:
    vector = data[station][date]
    vector = vector.to_numpy()
    return vector


def cosine_similarity(vector_i: array,
                      vector_j: array) -> float:
    norm_i = norm(vector_i)
    norm_j = norm(vector_j)
    denominator = norm_i*norm_j
    numerator = dot(vector_i,
                    vector_j)
    if denominator < 1e-6:
        return 0
    return numerator/denominator


params = get_params()
params.update({
    "comparison operation": "diff",
    "file results": "similarity",
    "clear sky model": "GHI",
    # "threshold": 0.8,
    "threshold": 10000,
    "pollutant": "SR",
    "year": 2021,
})
SIMA = SIMA_model(params)
data = DataFrame()
for station in params["stations"]:
    SIMA.get_station_data(station,
                          params["pollutant"])
    data = concat([data,
                   SIMA.station_data],
                  axis=1)
dates = SIMA.get_dates()
del SIMA
data.columns = params["stations"]
data = get_data_between_hours(data,
                              params)
comparison = comparison_data(params)
headers = [f"{station} {date}"
           for station in data.columns
           for date in dates]
stations_data = DataFrame(columns=headers,
                          index=headers)
print("-"*30)
print("Transformando datos")
bar = tqdm(headers)
# Transform data
for station_date in bar:
    bar.set_postfix(station_date=station_date)
    station, date = station_date.split()
    # Get daily data per station
    vector_data = get_vector(data,
                             station,
                             date)
    # Get daily ratio vector per station
    vector_comparison = get_vector(comparison.data,
                                   station,
                                   date)
    # Check atypical
    vector_comparison = vector_comparison > params["threshold"]
    # Transform to missing data
    vector_data[vector_comparison] = nan
    data[station][date] = vector_data
data = data.fillna(0)
print("-"*30)
print("Calculando similaridad")
bar = tqdm(headers)
for station_date_i, station_date in enumerate(bar):
    bar.set_postfix(station_date=station_date)
    station_i, date_i = station_date.split()
    vector_i = get_vector(data,
                          station_i,
                          date_i)
    for station_date_j in headers[station_date_i+1:]:
        station_j, date_j = station_date_j.split()
        vector_j = get_vector(data,
                              station_j,
                              date_j)
        cosine = cosine_similarity(vector_i,
                                   vector_j)
        stations_data.loc[station_date, station_date_j] = cosine
        stations_data.loc[station_date_j, station_date] = cosine
filename = "{}_{}.csv".format(params["file results"],
                              params["comparison operation"])
filename = join(params["path results"],
                params["clear sky model"],
                filename)
print(f"Guardando archivo {filename}")
stations_data.to_csv(filename)
