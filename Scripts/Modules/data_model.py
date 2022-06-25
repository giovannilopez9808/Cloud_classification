from pandas import (read_csv,
                    DataFrame,
                    to_datetime,
                    to_timedelta)
from os.path import join


class SIMA_model:
    def __init__(self) -> None:
        pass

    def read(self,
             filename: str) -> DataFrame:
        self.data = read_csv(filename,
                             header=[0, 1],
                             skiprows=[2],
                             index_col=0,
                             parse_dates=True,
                             low_memory=False)

    def get_dates(self) -> list:
        dates = self.data.index.date
        dates = sorted(list(set(dates)))
        return dates

    def get_station_data(self,
                         station: str,
                         pollutant: str) -> DataFrame:
        station = station.upper()
        self.station_data = DataFrame(self.data[(station,
                                                 pollutant)])
        self.station_data = self.station_data*1000

    def get_data_date(self,
                      date: str) -> DataFrame:
        date = to_datetime(date)
        select_data = self.station_data.index.date == date.date()
        data = self.station_data[select_data]
        return data

    def get_station_info(self,
                         params: dict,
                         station: str) -> dict:
        filename = join(params["path data"],
                        params["stations info"])
        data = read_csv(filename,
                        index_col=2)
        data["Since"] = to_datetime(data["Since"],
                                    format="%d/%m/%Y")
        data = data.T
        return data[station]


class clear_sky_data:
    def __init__(self,
                 params: dict) -> None:
        self.params = params
        self._read()

    def _read(self) -> DataFrame:
        filename = join(self.params["path results"],
                        self.params["clear sky file"])
        self.data = read_csv(filename,
                             index_col=0,
                             parse_dates=True)
        self.data.index = self.data.index + to_timedelta("01:0:00")

    def get_dates(self) -> list:
        dates = sorted(list(set(self.data.index.date)))
        return dates

    def get_station_data(self,
                         station: str) -> DataFrame:
        self.station_data = DataFrame(self.data[station])

    def get_date_date(self,
                      date: str) -> DataFrame:
        date = to_datetime(date)
        select_data = self.station_data.index.date == date.date()
        data = self.station_data[select_data]
        return data


if __name__ == "__main__":
    pass
