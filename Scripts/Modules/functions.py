from sklearn.metrics.pairwise import cosine_similarity
from pandas import (Timestamp,
                    DataFrame,
                    to_datetime,
                    concat)
from numpy import (divide,
                   zeros_like,
                   array,
                   empty,
                   nan,
                   isnan)
from os import listdir, makedirs
from typing import Type


def datetime_format(date: Timestamp,
                    hour: int) -> str:
    """
    Obtiene la fecha con hora en formato Y-M-D H:m

    Input:
    --------------------
    date -> fecha con formato Timestamp o datetime
    hour -> numeor entrero de la hora

    Output:?
    --------------------
    fecha con formato Y-M-D H:m
    """
    date = str(date)
    hour = fill_number(hour,
                       2)
    datetime = f"{date} {hour}:00"
    return datetime


def get_data_between_hours(data: DataFrame,
                           params: dict) -> DataFrame:
    data = data[data.index.hour >= params["hour initial"]]
    data = data[data.index.hour <= params["hour final"]]
    data = DataFrame(data)
    return data


def get_hourly_mean(data: DataFrame) -> DataFrame:
    """
    Obtiene el promerio horario de  un dataframe

    Inputs:
    --------------------
    data -> dataframe con los dato, el indice debe tener formato Timestamp

    Outputs:
    --------------------
    Dataframe con el promedio por hora, el indice tiene formato Timestamp
    """
    # Obtiene la fecha de los datos
    date = data.index[0].date()
    # Obtiene las horas
    hours = data.index.hour
    # Realiza el promedio por hora
    data = data.groupby(hours).mean()
    # Obtiene las horas totales
    hours = list(set(hours))
    # Indice
    index = [datetime_format(date, hour)
             for hour in hours]
    # To Timestamp
    data.index = to_datetime(index)
    data = DataFrame(data)
    return data


def mkdir(path: str) -> None:
    """
    Generalizacion del mkdir

    Inputs:
    --------------------
    path -> carpeta a crear
    """
    makedirs(path,
             exist_ok=True)


def ls(path: str) -> list:
    """
    Generalizacion del ls

    Inputs:
    --------------------
    path -> direccion a leer los archivos
    """
    files = sorted(listdir(path))
    return files


def fill_number(number: int,
                zfill: int) -> str:
    """
    Convierte un numero a string a n caracteres, los caracteres faltantes
    seran 0

    Inputs:
    --------------------
    number -> numero a convertir
    zfill -> numero de caracteres a rellenar

    Output:
    --------------------
    numero con tipo string
    """
    return str(number).zfill(zfill)


def get_labels(params: dict) -> tuple:
    keys = list(params["classification"].keys())
    label = [params["classification"][key]["label"]
             for key in keys]
    return keys, label


def get_colors(params: dict) -> list:
    colors = [params["classification"][key]["color"]
              for key in params["classification"]]
    return colors


def comparison_operation(measurement: DataFrame,
                         model: DataFrame,
                         operation: str,
                         fillnan: bool = True) -> DataFrame:
    model = DataFrame(model)
    index = model.index
    station = model.columns
    model = model.to_numpy()
    model = model.flatten()
    measurement = measurement.to_numpy()
    measurement = measurement.flatten()
    if "diff" == operation:
        comparison = model-measurement
        comparison[model < 1e-3] = 0
    if "ratio" == operation:
        comparison = divide(measurement,
                            model,
                            out=zeros_like(model),
                            where=model != 0)
    if fillnan:
        comparison[isnan(measurement)] = nan
    comparison = DataFrame(comparison,
                           index=index,
                           columns=station)
    return comparison


def threshold_filter(data: DataFrame,
                     params: dict) -> DataFrame:
    operation = params["comparison operation"]
    threshold = params["threshold"]
    if operation == "ratio":
        data[data > threshold] = nan
        return data
    if operation == "diff":
        data[data < threshold] = nan
        return data


def clean_data(data: DataFrame,
               clear_sky: DataFrame,
               comparison: DataFrame) -> DataFrame:
    comparison = DataFrame(comparison)
    index = list(data.index)
    header = comparison.columns
    data = data.to_numpy()
    comparison = comparison.to_numpy()
    comparison = comparison.flatten()
    data[isnan(comparison)] = nan
    data[clear_sky == 0] = 0
    data = DataFrame(data,
                     index=index,
                     columns=header)
    return data

# Apartado de cosine similitud


def get_cosine_similarity(data: DataFrame,
                          clean_data: Type,
                          params: dict) -> DataFrame:
    dates = clean_data.get_dates()
    station = params["station"]
    header = [f"{station} {date}"
              for date in dates]
    clean_data.get_station_data(station)
    all_data = clean_data.station_data
    all_data = all_data.fillna(0)
    all_data = all_data.to_numpy()
    all_data = all_data.reshape(-1, 24)
    data = data.fillna(0)
    data = data.to_numpy()
    data = data.reshape(1, -1)
    cosine = cosine_similarity(data,
                               all_data)
    cosine = cosine.flatten()
    cosine = DataFrame(cosine,
                       index=header)
    return cosine


def nan_vector(vector: DataFrame) -> array:
    header = vector.columns
    index = vector.index
    vector = empty(vector.size)
    vector[:] = nan
    vector = DataFrame(vector,
                       index=index,
                       columns=header)
    return vector


def sort(data: DataFrame) -> DataFrame:
    data = data.sort_values(ascending=False)
    return data


def get_best_similarity_dates(similarity: DataFrame,
                              params: dict,
                              header: str) -> list:
    similarity_vector = similarity[header]
    similarity_vector = sort(similarity_vector)
    similarity_vector = similarity_vector.iloc[1:params["top vectors"]]
    similarity_vector = similarity_vector.index
    return similarity_vector


def get_similarity_vectors(clean_data: Type,
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


if "__main__" == __name__:
    pass
