def get_params() -> dict:
    """
    Parametros generales de los programas
    """
    params = {
        # Ruta de las graficas
        "path graphics": "../Graphics",
        # Ruta de los resultados
        "path results": "../Results",
        # Ruta de los datos
        "path data": "../Data",
        # Carpeta de los datos del SIMA
        "SIMA folder": "SIMA",
        # Informacion de las estaciones
        "stations info": "Stations_information.csv",
        # Archivo con los resultados del modelo de Clear_sky
        "clear sky file": "Clear_sky.csv",
        # Archivo con las clasificaciones
        "classification file": "Classification.csv",
        # Classical models results
        "Classical model path": "Classical_model",
        # Neural models results
        "Neural model path": "Neural_model",
        # Clear sky models
        "clear sky models": [
            "RS",
            "GHI",
        ],
        # Comparison operations
        "comparison operations": [
            "ratio",
            "diff",
        ],
        # Classical models
        "classical models": [
            "SVM",
            "KNN",
            "Random forest",
            "Gaussian naive",
            "Decision tree",
        ],
        # Neural models
        "neural models": [
            "perceptron",
            "CNN",
            "LSTM",
            "RNN",
            "Bi LSTM",
            "Attention CNN",
            "Voting",
        ],
        # Estaciones a utilizar
        "stations": [
            "Sureste2",
            "Noreste",
            "Noroeste",
            "Suroeste",
        ],
        "classification": {
            0: {
                "label": "Cloudly",
                "color": "#00171f"
            },
            1: {
                "label": "Partly cloudly",
                "color": "#003459"
            },
            2: {
                "label": "Clear sky",
                "color": "#007ea7"
            },
        },
        "pollutant": "SR",
        "hour initial": 0,
        "hour final": 24,
        "years": [
            "2019",
            "2020",
            "2021",
        ],
    }
    return params


def get_classification_params(params: dict) -> dict:
    class_params = {
        "SVM": {
            "kernel": "linear",
        },
        "KNN": {
            "n_neighbors": 3,
        },
        "Random forest": {
            "criterion": "gini",
            "n_estimators": 1000,
        },
        "Gaussian naive": {
        },
        "Decision tree": {
            "criterion": "gini",
        },
    }
    label = "classification model"
    dataset = params[label]
    return class_params[dataset]


def get_neural_params(params: dict) -> dict:
    label = "neural model"
    neural_params = {
        "perceptron": {
            "Noreste": {
                "validation_split": 0.1,
                "batch_size": 8,
                "epochs": 200,
                "verbose": 1,
            },
            "Noroeste": {
                "validation_split": 0.1,
                "batch_size": 10,
                "epochs": 100,
                "verbose": 1,
            },
            "Sureste2": {
                "validation_split": 0.1,
                "batch_size": 5,
                "epochs": 200,
                "verbose": 1,
            },
            "Suroeste": {
                "validation_split": 0.1,
                "batch_size": 5,
                "epochs": 200,
                "verbose": 1,
            },
        },
        "CNN": {
            "Noreste": {
                "validation_split": 0.1,
                "batch_size": 3,
                "epochs": 200,
                "verbose": 1,
            },
            "Noroeste": {
                "validation_split": 0.1,
                "batch_size": 4,
                "epochs": 200,
                "verbose": 1,
            },
            "Sureste2": {
                "validation_split": 0.1,
                "batch_size": 4,
                "epochs": 200,
                "verbose": 1,
            },
            "Suroeste": {
                "validation_split": 0.1,
                "batch_size": 4,
                "epochs": 200,
                "verbose": 1,
            },
        },
        "LSTM": {
            "Noreste": {
                "validation_split": 0.1,
                "batch_size": 5,
                "epochs": 200,
                "verbose": 1,
            },
            "Noroeste": {
                "validation_split": 0.1,
                "batch_size": 4,
                "epochs": 200,
                "verbose": 1,
            },
            "Sureste2": {
                "validation_split": 0.1,
                "batch_size": 4,
                "epochs": 200,
                "verbose": 1,
            },
            "Suroeste": {
                "validation_split": 0.1,
                "batch_size": 3,
                "epochs": 200,
                "verbose": 1,
            },
        },
        "RNN": {
            "Noreste": {
                "validation_split": 0.1,
                "batch_size": 3,
                "epochs": 100,
                "verbose": 1,
            },
            "Noroeste": {
                "validation_split": 0.1,
                "batch_size": 6,
                "epochs": 200,
                "verbose": 1,
            },
            "Sureste2": {
                "validation_split": 0.1,
                "batch_size": 5,
                "epochs": 200,
                "verbose": 1,
            },
            "Suroeste": {
                "validation_split": 0.1,
                "batch_size": 7,
                "epochs": 200,
                "verbose": 1,
            },
        },
        "Bi LSTM": {
            "Noreste": {
                "validation_split": 0.1,
                "batch_size": 3,
                "epochs": 100,
                "verbose": 1,
            },
            "Noroeste": {
                "validation_split": 0.1,
                "batch_size": 4,
                "epochs": 100,
                "verbose": 1,
            },
            "Sureste2": {
                "validation_split": 0.1,
                "batch_size": 6,
                "epochs": 100,
                "verbose": 1,
            },
            "Suroeste": {
                "validation_split": 0.1,
                "batch_size": 7,
                "epochs": 100,
                "verbose": 1,
            },
        },
        "Attention CNN": {
            "Noreste": {
                "validation_split": 0.1,
                "batch_size": 4,
                "epochs": 100,
                "verbose": 1,
            },
            "Noroeste": {
                "validation_split": 0.1,
                "batch_size": 3,
                "epochs": 100,
                "verbose": 1,
            },
            "Sureste2": {
                "validation_split": 0.1,
                "batch_size": 4,
                "epochs": 200,
                "verbose": 1,
            },
            "Suroeste": {
                "validation_split": 0.1,
                "batch_size": 7,
                "epochs": 100,
                "verbose": 1,
            },
        },

    }
    model = params[label]
    station = params["station"]
    dataset = dict()
    dataset["run"] = neural_params[model][station]
    dataset.update({
        "compile": {
            "optimizer": "adam",
            "loss": "sparse_categorical_crossentropy",
            "metrics": ["accuracy"],
        },
    })
    return dataset


def get_voting_models(params: dict) -> list:
    voting_models = {
        "Noroeste": {
            "ratio": {
                "RS": [
                    "Bi LSTM",
                    "Attention CNN",
                    "CNN",
                ],
                "GHI": [
                    "CNN",
                    "Bi LSTM",
                    "Attention CNN",
                ],
            },
            "diff": {
                "RS": [
                    "CNN",
                    "Bi LSTM",
                    "LSTM",
                ],
                "GHI": [
                    "CNN",
                    "RNN",
                    "Bi LSTM"
                ]
            },
        },
        "Noreste": {
            "ratio": {
                "RS": [
                    "perceptron",
                    "CNN",
                    "Bi LSTM",
                ],
                "GHI": [
                    "Bi LSTM",
                    "CNN",
                    "RNN",
                ],
            },
            "diff": {
                "RS": [
                    "LSTM",
                    "CNN",
                    "Bi LSTM",
                ],
                "GHI": [
                    "CNN",
                    "LSTM",
                    "Bi LSTM"
                ]
            },
        },
        "Sureste2": {
            "ratio": {
                "RS": [
                    "CNN",
                    "Bi LSTM",
                    "LSTM",
                ],
                "GHI": [
                    "CNN",
                    "Attention CNN",
                    "Bi LSTM",
                ],
            },
            "diff": {
                "RS": [
                    "CNN",
                    "Bi LSTM",
                    "LSTM",
                ],
                "GHI": [
                    "CNN",
                    "RNN",
                    "Bi LSTM"
                ]
            },
        },
        "Suroeste": {
            "ratio": {
                "RS": [
                    "RNN",
                    "Bi LSTM",
                    "CNN",
                ],
                "GHI": [
                    "CNN",
                    "RNN",
                    "Attention CNN",
                ],
            },
            "diff": {
                "RS": [
                    "CNN",
                    "Bi LSTM",
                    "LSTM",
                ],
                "GHI": [
                    "CNN",
                    "LSTM",
                    "RNN"
                ]
            },
        },
    }
    operation = params["comparison operation"]
    sky_model = params["clear sky model"]
    station = params["station"]
    models = voting_models[station][operation][sky_model]
    return models


def get_threshold(params: dict) -> dict:
    model = params["clear sky model"]
    operation = params["comparison operation"]
    threshold = {
        "RS": {
            "ratio": 10,
            "diff": -1000,
        },
        "GHI": {
            "ratio": 0.8,
            "diff": 0,
        },
    }
    return threshold[model][operation]


if __name__ == "__main__":
    pass
