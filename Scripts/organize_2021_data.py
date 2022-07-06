from pandas import (
    read_csv,
    to_datetime,
    concat,
    DataFrame,
)
from os import listdir as ls
from tqdm import tqdm

stations = {
    "Dates": "Fechas",
    "SE": "SURESTE",
    "NE": "NORESTE",
    "CE": "CENTRO",
    "NO": "NOROESTE",
    "SO": "SUROESTE",
    "NO2": "NOROESTE2",
    "NTE": "NORTE",
    "NE2": "NORESTE2",
    "SE2": "SURESTE2",
    "SO2": "SUROESTE2",
    "SE3": "SURESTE3",
    "SUR": "SUR",
    "NTE2": "NORTE2",
    "NE3": "NORESTE3",
}


def date_format(date: str) -> str:
    """
    Format date to dd/mm/yyyy hh:mm P.M to yyyy-mm-dd hh:mm
    """
    # Get date and hour
    date, hour = date.split()[:2]
    # List date
    date = date.split("/")
    # Reverse date
    date.reverse()
    # Join date
    date = "-".join(date)
    # Join date and hour
    date = " ".join([
        date,
        hour,
    ])
    return date


def data_format(data: DataFrame) -> DataFrame:
    """
    Apply date format to dataframe and set as a index
    """
    # Apply format date
    data["date"] = data["date"].apply(date_format)
    # Set as index
    data.index = to_datetime(data["date"])
    # Delete useless column
    data = data.drop(columns="date")
    data.index.name = "Date"
    return data


def get_parameter_name(file: str) -> str:
    """
    Get parameter from filename
    """
    parameter = file.split(".")[0]
    parameter = parameter.upper()
    return parameter


if __name__ == "__main__":
    # Get all files
    files = sorted(ls())
    # Selecrt only csv files
    files = [file
             for file in files
             if ".csv" in file]
    # Initialize files
    results = DataFrame()
    for file in tqdm(files):
        # Get parameter
        parameter = get_parameter_name(file)
        # Read data
        data = read_csv(file)
        # Format data
        data = data_format(data)
        # Rename columns
        data.columns = [(stations[column], parameter)
                        for column in data.columns]
        # Save data
        results = concat(
            [results, data],
            axis=1,
        )
    # Get all parameters
    parameters = [[column[1]
                   for column in results.columns]]
    # Set row with all parameters
    parameters = DataFrame(parameters,
                           columns=results.columns)
    # concat results
    results = concat([parameters,
                      results])
    # Set row with all stations
    stations = [[column[0]
                 for column in results.columns]]
    stations = DataFrame(stations,
                         columns=results.columns)
    # concat all stations
    results = concat([stations,
                      results])
    # Columns
    columns = list(results.columns)
    # Sort columns with stations
    columns.sort(key=lambda values: values[0])
    # Sort all the data
    results = results[columns]
    results.to_csv("../2021.csv",
                   header=None)
