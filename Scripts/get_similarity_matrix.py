"""
python get_similarity_matrix (operation) (sky model)
"""
from Modules.data_model import (comparison_data,
                                clean_data_model)
from Modules.functions import get_data_between_hours
from Modules.params import get_params
from pandas import DataFrame, concat
from numpy import nan, array, dot
from numpy.linalg import norm
from os.path import join
from tqdm import tqdm
from sys import argv, exit


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
    "comparison operation": argv[1],
    "file results": "similarity",
    "clear sky model": argv[2],
})
clean_data = clean_data_model(params)
dates = clean_data.get_dates()
headers = [f"{station} {date}"
           for station in params["stations"]
           for date in dates]
stations_data = DataFrame(columns=headers,
                          index=headers)
data = clean_data.data
data = data.fillna(0)
print("-"*30)
print("Calculando similitud")
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
