from .data_model import (classification_data,
                         full_comparison_data)
from numpy import isnan, array, mean
from pandas import DataFrame


class dataset_model:
    def __init__(self,
                 params: dict) -> None:
        self.params = params
        self._read()

    def _read(self) -> DataFrame:
        classification = classification_data(self.params)
        comparison = full_comparison_data(self.params)
        dataset = self.params["datasets"]
        self.train = self._create_dataset(classification,
                                          comparison,
                                          dataset,
                                          "train")
        self.validation = self._create_dataset(classification,
                                               comparison,
                                               dataset,
                                               "validation")
        self.test = self._create_dataset(classification,
                                         comparison,
                                         dataset,
                                         "test")

    def _create_dataset(self,
                        classification: classification_data,
                        comparison: full_comparison_data,
                        dataset: dict,
                        data_name: str) -> DataFrame:
        print("-"*40)
        print(f"Creando dataset {data_name}")
        stations = dataset[data_name]
        data = list()
        target = list()
        dates = classification.get_dates()
        for station in stations:
            classification.get_station_data(station)
            comparison.get_station_data(station)
            for date in dates:
                daily_value = classification.get_date_data(date)
                daily_value = self._get_vector(daily_value)
                if not isnan(daily_value):
                    daily_vector = comparison.get_date_data(date)
                    daily_vector = self._get_vector(daily_vector)
                    data.append(daily_vector)
                    target += list(daily_value)
        data = array(data)
        target = array(target)
        return [data, target]

    def apply_mean(self) -> array:
        self.train[0] = self._mean(self.train[0])
        self.validation[0] = self._mean(self.validation[0])
        self.test[0] = self._mean(self.test[0])

    def _mean(self,
              data: array) -> array:
        mean_value = mean(data,
                          axis=1)
        mean_value = mean_value.reshape(-1, 1)
        return mean_value

    def _get_vector(self,
                    data: DataFrame) -> array:
        vector = data.to_numpy()
        vector = vector.flatten()
        return vector
