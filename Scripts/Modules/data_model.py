from pandas import read_csv, DataFrame, to_datetime


class data_model:
    def __init__(self) -> None:
        pass

    def read(self, filename: str) -> DataFrame:
        self.data = read_csv(filename,
                             header=[0, 1],
                             skiprows=[2],
                             index_col=0,
                             parse_dates=True,
                             low_memory=False)

    def get_station_data(self, station: str, pollutant: str) -> DataFrame:
        self.select_data = DataFrame(self.data[(station, pollutant)])

    def get_data_date(self, date: str) -> DataFrame:
        date = to_datetime(date)
        data = self.select_data[self.select_data.index.date == date.date()]
        return data