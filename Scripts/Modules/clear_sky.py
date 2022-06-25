from .extraterrestrial_solar import extraterrestial_solar_model
from pandas import DataFrame, to_datetime
from .functions import fill_number


class clear_sky_model:

    def __init__(self) -> None:
        self.model = extraterrestial_solar_model()

    def run(self, params: dict) -> DataFrame:
        results = DataFrame(columns=["H0"])
        hour_inital = params["hour initial"]
        hour_inital *= 60
        hour_final = params["hour final"]
        hour_final *= 60
        hours = range(hour_inital,
                      hour_final+1)
        for minutes in hours:
            datetime = self._get_datetime(params["date"],
                                          minutes)
            params["datetime"] = datetime
            H0 = self.model.get_H0(params)
            results.loc[datetime] = H0
        results.index = to_datetime(results.index)
        return results

    def _get_time(self, minutes: int) -> str:
        hour = self._get_hour(minutes)
        minute = self._get_minute(minutes)
        time = f"{hour}:{minute}"
        return time

    def _get_hour(self, minutes: int) -> str:
        hour = minutes//60
        hour = fill_number(hour,
                           2)
        return hour

    def _get_minute(self, minutes: int) -> str:
        minute = minutes % 60
        minute = fill_number(minute,
                             2)
        return minute

    def _get_datetime(self,
                      date: str,
                      minutes: int) -> str:
        time = self._get_time(minutes)
        datetime = f"{date} {time}"
        return datetime


if __name__ == "__main__":
    pass
