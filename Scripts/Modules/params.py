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
            "Decicion tree",
        ],
        # Neural models
        "neural models": [
            "perceptron",
            "CNN",
            "LSTM",
            "RNN",
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
                "batch_size": 5,
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
                "batch_size": 6,
                "epochs": 150,
                "verbose": 1,
            },
            "Noroeste": {
                "validation_split": 0.1,
                "batch_size": 5,
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
                "batch_size": 5,
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
                "batch_size": 5,
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
                "batch_size": 5,
                "epochs": 200,
                "verbose": 1,
            },
        },
        "RNN": {
            "Noreste": {
                "validation_split": 0.1,
                "batch_size": 5,
                "epochs": 200,
                "verbose": 1,
            },
            "Noroeste": {
                "validation_split": 0.1,
                "batch_size": 5,
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
                "batch_size": 5,
                "epochs": 200,
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
