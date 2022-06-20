from pandas import read_csv, DataFrame, to_datetime, to_timedelta
from .functions import fill_number, yymmdd2yyyy_mm_dd


class SIMA_model:
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
        station = station.upper()
        self.select_data = DataFrame(self.data[(station, pollutant)])
        self.select_data = self.select_data*1000

    def get_data_date(self, date: str) -> DataFrame:
        date = to_datetime(date)
        data = self.select_data[self.select_data.index.date == date.date()]
        return data


class SMARTS_model:
    def __init__(self) -> None:
        pass

    def read(self, filename: str) -> DataFrame:
        data = read_csv(filename,
                        header=None,
                        sep=" ")
        data[0] = data[0].apply(self.format_time)
        data.columns = ["Date", "Data"]
        date = filename.split("/")[-1]
        date = date.split(".")[0]
        data = self.fill_year(data,
                              date)
        return data

    def format_time(self, hour: float) -> str:
        minutes = round(hour % 1*60)
        minutes = fill_number(minutes, 2)
        hour = int(hour)
        hour = fill_number(hour, 2)
        time = f"{hour}:{minutes}"
        return time

    def fill_year(self,
                  data: DataFrame,
                  date: int) -> DataFrame:
        date = yymmdd2yyyy_mm_dd(date)
        data["Date"] = data["Date"].apply(
            lambda time: f"{date} {time}")
        data.index = to_datetime(data["Date"])
        data = data.drop(columns=["Date"])
        data.index = data.index-to_timedelta("00:30:00")
        return data
