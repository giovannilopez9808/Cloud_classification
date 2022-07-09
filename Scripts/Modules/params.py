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
        "datasets": {
            "train": ["Sureste2",
                      "Suroeste",
                      "Noroeste"],
            "validation": ["Noroeste"],
            "test": ["Noreste"],
        }
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
            "batch_size": 200,
            "epochs": 100,
        },
        "RNN": {
            "batch_size": 10,
            "epochs": 500,
        }
    }
    dataset = params[label]
    return neural_params[dataset]


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
