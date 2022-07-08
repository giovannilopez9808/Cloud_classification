from Modules.transform_data import transform_data_model
from Modules.functions import get_data_between_hours
from Modules.params import (get_params,
                            get_threshold)
from Modules.data_model import SIMA_model
from pandas import DataFrame

params = get_params()
params.update({
    "comparison operation": "ratio",
    "clear sky model": "RS",
    "longitude": -100.22,
    "latitude": 25.75,
    "timezone": -5,
    "top vectors": 30,
    "station": "Sureste2",
    "date": "2021-07-22",
    "pollutant": "SR",
    "year": 2021,
})
params["threshold"] = get_threshold(params)
SIMA_data = SIMA_model(params)
data = SIMA_data.get_data(params["station"],
                          params["pollutant"],
                          params["date"])
data = DataFrame(data)
data = get_data_between_hours(data,
                              params)

transform_data = transform_data_model(params)
comparison = transform_data.run(data)
print(comparison)
