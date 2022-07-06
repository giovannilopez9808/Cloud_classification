from Modules.clear_sky import clear_sky_model
from Modules.functions import (comparison_operation,
                               threshold_filter,
                               get_hourly_mean,
                               clean_data)
from Modules.data_model import SIMA_model
from Modules.params import get_params
import matplotlib.pyplot as plt
from pandas import DataFrame

params = get_params()
params.update({
    "comparison operation": "ratio",
    "clear sky model": "RS",
    "longitude": -100.22,
    "latitude": 25.75,
    "timezone": -5,
    "station": "Noroeste",
    "date": "2021-05-13",
    "pollutant": "SR",
    "year": 2021,
})
data = SIMA_model(params)
data = data.get_data(params["station"],
                     params["pollutant"],
                     params["date"])
data = DataFrame(data)
plt.plot(data)
# Clear sky
clear_sky = clear_sky_model()
clear_sky = clear_sky.run(params)
clear_sky = get_hourly_mean(clear_sky)
plt.plot(clear_sky)
# Diff or ratio
comparison = comparison_operation(data,
                                  clear_sky,
                                  params["comparison operation"])
# Clean data
data = clean_data(data,
                  clear_sky,
                  comparison)
# Full data

plt.plot(data)
plt.show()
