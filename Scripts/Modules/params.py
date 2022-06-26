
def get_params() -> dict:
    params = {
        "path graphics": "../Graphics",
        "path results": "../Results",
        "path data": "../Data",
        "SIMA folder": "SIMA",
        "stations info": "Stations_information.csv",
        "clear sky file": "Clear_sky.csv",
        "classification file": "Classification.csv",
        "stations": ["Sureste2",
                     "Noreste",
                     "Noroeste",
                     "Suroeste",
                     ],
    }
    return params


if __name__ == "__main__":
    pass
