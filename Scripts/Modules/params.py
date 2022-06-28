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
                "label": "Nublado",
                "color": "#00171f"
            },
            1: {
                "label": "Medio nublado",
                "color": "#003459"
            },
            2: {
                "label": "Despejado",
                "color": "#007ea7"
            },
        }
    }
    return params


if __name__ == "__main__":
    pass
