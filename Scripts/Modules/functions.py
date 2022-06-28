from pandas import (Timestamp,
                    DataFrame,
                    to_datetime)
from os import listdir, makedirs


def datetime_format(date: Timestamp,
                    hour: int) -> str:
    """
    Obtiene la fecha con hora en formato Y-M-D H:m

    Input:
    --------------------
    date -> fecha con formato Timestamp o datetime
    hour -> numeor entrero de la hora

    Output:
    --------------------
    fecha con formato Y-M-D H:m
    """
    date = str(date)
    hour = fill_number(hour,
                       2)
    datetime = f"{date} {hour}:00"
    return datetime


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


if "__main__" == __name__:
    pass
