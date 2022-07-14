from keras.layers import (GlobalAveragePooling1D,
                          SimpleRNN,
                          Dropout,
                          Flatten,
                          Conv1D,
                          Dense,
                          LSTM)
from Modules.params import get_neural_params
from keras.callbacks import ModelCheckpoint
from .dataset_model import dataset_model
from Modules.functions import (get_confusion_matrix,
                               get_report,
                               get_labels,
                               mkdir)
from keras.models import (Sequential,
                          load_model)
from pandas import DataFrame
from numpy import argmax
from os.path import join
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
        self.dataset.split_data()

    def build(self,
              params: dict) -> None:
        self.params = params
        input_dim = self._get_input_dim(params)
        self._get_dataset(params)
        if params["neural model"] == "perceptron":
            self.model = Perceptron_model(input_dim)
        if params["neural model"] == "CNN":
            self.model = CNN_model(input_dim)
        if params["neural model"] == "RNN":
            self.model = RNN_model(input_dim)
        if params["neural model"] == "LSTM":
            self.model = LSTM_model(input_dim)

    def run(self) -> list:
        self.params["neural params"] = get_neural_params(self.params)
        history = self.model.run(self.dataset,
                                 self.params)
        self._save_history(history)
        self._predict(self.params)

    def test(self) -> None:
        self._predict()
        self._save_confusion_matrix()

    def _predict(self) -> None:
        self.predict = self.model.predict(self.dataset,
                                          self.params)
        self._get_report()

    def _get_folder_save(self) -> str:
        folder = join(self.params["path results"],
                      self.params["Neural model path"],
                      self.params["neural model"],
                      self.params["station"])
        mkdir(folder)
        return folder

    def _get_report(self) -> None:
        operation = self.params["comparison operation"]
        sky_model = self.params["clear sky model"]
        _, class_label = get_labels(self.params)
        labels = self.dataset.test[1]
        report = get_report(labels,
                            self.predict,
                            sky_model,
                            operation,
                            class_label)
        filename = f"{operation}_{sky_model}_report.csv"
        folder = self._get_folder_save()
        filename = join(folder,
                        filename)
        file = open(filename,
                    "w")
        file.write(report)
        file.close()

    def _save_history(self,
                      history: DataFrame) -> None:
        folder = self._get_folder_save()
        operation = self.params["comparison operation"]
        clear_sky = self.params["clear sky model"]
        filename = f"{operation}_{clear_sky}_history.csv"
        filename = join(folder,
                        filename)
        history.to_csv(filename,
                       index=False)

    def _save_confusion_matrix(self,) -> None:
        _, class_label = get_labels(self.params)
        labels = self.dataset.test[1]
        matrix = get_confusion_matrix(labels,
                                      self.predict,
                                      class_label)
        folder = self._get_folder_save()
        operation = self.params["comparison operation"]
        clear_sky = self.params["clear sky model"]
        filename = f"{operation}_{clear_sky}_matrix.csv"
        filename = join(folder,
                        filename)
        matrix.to_csv(filename)


class base_model:
    def __init__(self,
                 input_dim: int) -> None:
        self._build(input_dim)

    def _build(self,
               input_dim: int) -> None:
        self.model = Sequential()

    def _get_filename_best_model(self,
                                 params: dict) -> str:
        filename = "best_model_{}_{}.h5".format(params["comparison operation"],
                                                params["clear sky model"])
        folder = join(params["path results"],
                      params["Neural model path"],
                      params["neural model"],
                      params["station"])
        self.filename = join(folder,
                             filename)

    def _get_callbacks(self,
                       params: dict) -> list:
        callbacks_list = [
            ModelCheckpoint(
                filepath=self.filename,
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1),
            # EarlyStopping(monitor='val_loss',
            # patience=20)
        ]
        return callbacks_list

    def _compile(self,
                 params: dict) -> None:
        neural_params = params["neural params"]
        self.model.compile(**neural_params["compile"])
        self._get_filename_best_model(params)

    def run(self,
            dataset: Type,
            params: dict) -> DataFrame:
        neural_params = params["neural params"]
        self._compile(params)
        callbacks = self._get_callbacks(params)
        history = self.model.fit(dataset.train[0],
                                 dataset.train[1],
                                 callbacks=callbacks,
                                 **neural_params["run"])
        history = history.history
        history = DataFrame(history)
        return history

    def predict(self,
                dataset: Type,
                params:dict) -> list:
        self._load_model(params)
        results = self.model.predict(dataset.test[0])
        results = argmax(results,
                         axis=1)
        return results

    def _load_model(self,
                    params:dict) -> None:
        self._get_filename_best_model(params)
        self.model = load_model(self.filename)


class Perceptron_model(base_model):
    def __init__(self,
                 input_dim: int) -> None:
        super().__init__(input_dim)
        self._build(input_dim)

    def _build(self,
               input_dim: int) -> None:
        self.model = Sequential([
            Flatten(input_shape=(input_dim, 1)),
            Dense(256, activation='sigmoid'),
            Dense(128, activation='sigmoid'),
            Dense(3, activation="sigmoid"),
        ])


class CNN_model(base_model):
    def __init__(self,
                 input_dim: int) -> None:
        super().__init__(input_dim)
        self._build(input_dim)

    def _build(self,
               input_dim: int) -> None:
        self.model = Sequential([
            Conv1D(100,
                   3,
                   activation="relu",
                   input_shape=(input_dim, 1)),
            Conv1D(200,
                   3,
                   activation="relu"),
            Conv1D(200,
                   3,
                   activation='relu'),
            GlobalAveragePooling1D(),
            Dropout(0.5),
            Dense(3,
                  activation="sigmoid"),
        ])


class RNN_model(base_model):
    def __init__(self,
                 input_dim: int) -> None:
        super().__init__(input_dim)
        self._build(input_dim)

    def _build(self,
               input_dim: int) -> None:
        input_shape = (input_dim, 1)
        self.model = Sequential([
            SimpleRNN(64,
                      input_shape=input_shape,
                      activation="relu"),
            Dense(3,
                  activation='sigmoid')
        ])


class LSTM_model(base_model):
    def __init__(self,
                 input_dim: int) -> None:
        super().__init__(input_dim)
        self._build(input_dim)

    def _build(self,
               input_dim: int) -> None:
        input_shape = (input_dim, 1)
        self.model = Sequential([
            LSTM(256,
                 input_shape=input_shape,
                 activation='tanh',
                 return_sequences=True),
            Dropout(0.1),
            LSTM(256,
                 activation='tanh'),
            # Dense(64,
            # activation='sigmoid'),
            Dense(3,
                  activation='sigmoid')
        ])
