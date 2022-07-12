from sklearn.model_selection import train_test_split
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
        comparison.get_data_between_hours()
        self.train = self._create_dataset(classification,
                                          comparison)
        self.test =[1,1]
    def _create_dataset(self,
                        classification: classification_data,
                        comparison: full_comparison_data) -> DataFrame:
        station = self.params["station"]
        data = list()
        target = list()
        dates = classification.get_dates()
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

    def _get_vector(self,
                    data: DataFrame) -> array:
        vector = data.to_numpy()
        vector = vector.flatten()
        return vector

    def split_data(self) -> tuple:
        x_train, x_test, y_train, y_test = train_test_split(self.train[0],
                                                            self.train[1],
                                                            test_size=0.3,
                                                            random_state=42)
        self.train[0] = x_train
        self.train[1] = y_train
        self.test[0] = x_test
        self.test[1] = y_test
