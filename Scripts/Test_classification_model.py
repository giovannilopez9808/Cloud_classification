from Modules.transform_data import transform_data_model
from Modules.classic_models import classification_model
from Modules.functions import get_data_between_hours
from Modules.dataset_model import dataset_model
from Modules.params import (get_params,
                            get_threshold)
from Modules.data_model import SIMA_model
from pandas import DataFrame
from os.path import join
from tqdm import tqdm


def get_subparams(params: dict) -> dict:
    station = params["station"]
    year = params["test"][station]["date"]
    year = year.split("-")[0]
    subparams = params.copy()
    subparams.pop("test")
    subparams.update({
        "date": params["test"][station]["date"],
        "timezone": params["timezone"],
        "station": station,
        "year": year,
    })
    return subparams


def get_station_location(SIMA: SIMA_model,
                         station: str,
                         subparams: dict) -> dict:
    info = SIMA.get_station_info(subparams,
                                 station)
    subparams.update({
        "longitude": info["Longitude"],
        "latitude": info["Latitude"],
    })
    return subparams


def get_test_header(params: dict) -> list:
    headers = list()
    for station in params["test"]:
        date = params["test"][station]["date"]
        header = f"{station} {date}"
        headers += [header]
    return headers


params = get_params()
params.update({
    "file results": "Test_models.csv",
    "comparison operation": "ratio",
    "clear sky model": "RS",
    "top vectors": 30,
    "timezone": -6.25,
})
params["threshold"] = get_threshold(params)
headers = get_test_header(params)
model = classification_model()
results = DataFrame(index=params["classical models"],
                    columns=headers)
for station in params["test"]:
    print("-"*40)
    print(f"Analizando {station}")
    params["station"] = station
    subparams = get_subparams(params)
    dataset = dataset_model(subparams)
    dataset.split_data()
    SIMA_data = SIMA_model(subparams)
    subparams = get_station_location(SIMA_data,
                                     station,
                                     subparams)
    data = SIMA_data.get_data(subparams["station"],
                              subparams["pollutant"],
                              subparams["date"])
    data = DataFrame(data)
    data = get_data_between_hours(data,
                                  subparams)
    transform_data = transform_data_model(subparams)
    comparison = transform_data.run(data)
    comparison = comparison.to_numpy()
    comparison = comparison.flatten()
    results_per_station = list()
    bar = tqdm(params["classical models"])
    for model_name in bar:
        bar.set_postfix(model=model_name)
        subparams["classification model"] = model_name
        model.define_model(subparams)
        model.run(dataset.train)
        result = model.predict([[comparison], 0])
        results_per_station += [result[0]]
    header = f"{station} {subparams['date']}"
    results[header] = results_per_station
filename = join(params["path results"],
                params["file results"])
results.to_csv(filename)
