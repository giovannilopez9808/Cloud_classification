from .data_model import classification_data, comparison_data
from pandas import DataFrame
from numpy import isnan


class dataset_model:
    def __init__(self,
                 params: dict) -> None:
        self.params = params
        self._read()

    def _read(self) -> DataFrame:
        classification = classification_data(self.params)
        comparison = comparison_data(self.params)
        comparison.read(self.params["comparison operation"])
        dataset = self.params["datasets"]
        self.train = self._create_dataset(classification,
                                          comparison,
                                          dataset["train"])
        self.validation = self._create_dataset(classification,
                                               comparison,
                                               dataset["validation"])
        self.test = self._create_dataset(classification,
                                         comparison,
                                         dataset["test"])

    def _create_dataset(self,
                        classification: classification_data,
                        comparison: comparison_data,
                        stations: list) -> DataFrame:
        data = list()
        target = list()
        dates = classification.get_dates()
        for station in stations:
            classification.get_station_data(station)
            comparison.get_station_data(station)
            for date in dates:
                daily_value = classification.get_date_date(date)
                daily_vector = comparison.get_data_date(date)
                daily_vector = daily_vector.fillna(100)
                daily_value = daily_value.to_numpy()
                daily_vector = daily_vector.to_numpy()
                if not isnan(daily_value):
                    data.append(list(daily_vector))
                    target += list(daily_value)
        return data, target
