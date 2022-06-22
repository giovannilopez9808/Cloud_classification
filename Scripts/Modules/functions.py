from pandas import Timestamp
from os import listdir


def ls(path: str) -> list:
    files = sorted(listdir(path))
    return files


def fill_number(number: int, zfill: int) -> str:
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
