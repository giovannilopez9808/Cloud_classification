from pandas import (Timestamp,
                    DataFrame,
                    to_datetime)
from os import listdir, makedirs


def datetime_format(date: Timestamp,
                    hour: int) -> str:
    date = str(date)
    hour = fill_number(hour,
                       2)
    datetime = f"{date} {hour}:00"
    return datetime


def hourly_mean(data: DataFrame) -> DataFrame:
    date = data.index[0].date()
    hours = data.index.hour
    data = data.groupby(hours).mean()
    hours = list(set(hours))
    index = [datetime_format(date, hour)
             for hour in hours]
    data.index = to_datetime(index)
    return data


def mkdir(path: str) -> None:
    makedirs(path,
             exist_ok=True)


def ls(path: str) -> list:
    files = sorted(listdir(path))
    return files


def fill_number(number: int,
                zfill: int) -> str:
    return str(number).zfill(zfill)


def yymmdd2yyyy_mm_dd(date: int) -> str:
    date = str(date)
    date = [date[i:i+2]
            for i in range(0,
                           len(date),
                           2)]
    date[0] = f"20{date[0]}"
    date = "-".join(date)
    return date


def yyyy_mm_dd2yymmdd(date: Timestamp) -> str:
    year = str(date.year)
    month = fill_number(date.month, 2)
    day = fill_number(date.day, 2)
    year = year[2:]
    date = [year,
            month,
            day]
    date = "".join(date)
    return date


if "__main__" == __name__:
    pass
