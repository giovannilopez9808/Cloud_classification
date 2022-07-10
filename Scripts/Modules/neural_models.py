from keras.layers import (SimpleRNN,
                          Dropout,
                          Flatten,
                          Dense,
                          LSTM)
from sklearn.metrics import classification_report
from Modules.params import get_neural_params
from .dataset_model import dataset_model
from keras.models import Sequential
from numpy import argmax
from typing import Type


class neural_model:
    def __init__(self) -> None:
        pass

    def _get_input_dim(self,
                       params: dict) -> int:
        hour_i = params["hour initial"]
        hour_f = params["hour final"]
        if hour_i == 0 and hour_f == 24:
            input_dim = 24
        else:
            input_dim = hour_f-hour_i+1
        return input_dim

    def _get_dataset(self,
                     params: dict) -> Type:
        self.dataset = dataset_model(params)

    def build(self,
              params: dict) -> None:
        self.params = params
        input_dim = self._get_input_dim(params)
        self._get_dataset(params)
        if params["neural model"] == "perceptron":
            self.model = Perceptron_model(input_dim)
        if params["neural model"] == "RNN":
            self.model = RNN_model(input_dim)
        if params["neural model"] == "LSTM":
            self.model = LSTM_model(input_dim)

    def run(self) -> list:
        neural_params = get_neural_params(self.params)
        self.model.run(self.dataset,
                       neural_params)
        self.predict = self.model.predict(self.dataset)
        self._get_report()

    def _get_report(self) -> None:
        labels = self.dataset.test[1]
        print(classification_report(labels,
                                    self.predict))


class base_model:
    def __init__(self) -> None:
        self._build()

    def _build(self) -> None:
        self.model = Sequential()

    def _compile(self,
                 params: dict) -> None:
        self.model.compile(**params["compile"])

    def run(self,
            dataset: Type,
            params: dict) -> None:
        self._compile(params)
        self.model.fit(dataset.train[0],
                       dataset.train[1],
                       **params["run"])

    def predict(self,
                dataset: Type) -> list:
        results = self.model.predict(dataset.test[0])
        results = argmax(results,
                         axis=1)
        return results


class Perceptron_model(base_model):
    def __init__(self,
                 input_dim: int) -> None:
        super().__init__()
        self._build(input_dim)

    def _build(self,
               input_dim: int) -> None:
        self.model = Sequential([
            Flatten(input_shape=(input_dim, 1)),
            # dense layer 1
            Dense(256, activation='sigmoid'),
            # dense layer 2
            Dense(128, activation='sigmoid'),
            # output layer
            Dense(3, activation="sigmoid"),
        ])


class LSTM_model:
    def __init__(self,
                 input_dim: int) -> None:
        self._build(input_dim)

    def _build(self,
               input_dim: int) -> None:
        input_shape = (input_dim, 1)
        self.model = Sequential([
            LSTM(128,
                 input_shape=input_shape,
                 activation='relu',
                 return_sequences=True),
            Dropout(0.2),
            LSTM(128,
                 activation='relu'),
            Dropout(0.1),
            Dense(32,
                  activation='relu'),
            Dropout(0.2),
            Dense(3,
                  activation='softmax')
        ])

    def _compile(self,
                 params: dict) -> None:
        self.model.compile(**params["compile"])

    def run(self,
            dataset: Type,
            params: dict) -> None:
        self._compile(**params)
        self.model.fit(dataset.train[0],
                       dataset.train[1],
                       **params["run"])

    def predict(self,
                dataset: Type) -> list:
        results = self.model.predict(dataset.test[0])
        results = argmax(results,
                         axis=1)
        return results


class RNN_model:
    def __init__(self,
                 input_dim: int) -> None:
        self._build(input_dim)

    def _build(self,
               input_dim: int) -> None:
        input_shape = (input_dim, 1)
        self.model = Sequential([
            SimpleRNN(128,
                      input_shape=input_shape,
                      activation="linear"),
            Dense(3,
                  activation='softmax')
        ])

    def _compile(self,
                 params: dict) -> None:
        self.model.compile(**params["compile"])

    def run(self,
            dataset: Type,
            params: dict) -> None:
        self._compile(params)
        self.model.fit(dataset.train[0],
                       dataset.train[1],
                       **params["run"])

    def predict(self,
                dataset: Type) -> list:
        results = self.model.predict(dataset.test[0])
        results = argmax(results,
                         axis=1)
        return results
