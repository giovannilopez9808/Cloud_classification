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
        "hour initial": 9,
        "hour final": 18,
        "datasets": {
            "train": ["Sureste2",
                      "Noroeste"],
            "validation": ["Suroeste"],
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
    }
    label = "classification model"
    dataset = params[label]
    return class_params[dataset]


if __name__ == "__main__":
    pass
