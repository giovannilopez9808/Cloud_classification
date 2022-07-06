from Modules.clear_sky import clear_sky_model
from Modules.functions import (get_best_similarity_dates,
                               get_similarity_vectors,
                               get_data_between_hours,
                               get_cosine_similarity,
                               comparison_operation,
                               threshold_filter,
                               get_hourly_mean,
                               fill_data,
                               clean_data)
from Modules.params import (get_threshold,
                            get_params)
from Modules.data_model import (clean_data_model,
                                SIMA_model)
import matplotlib.pyplot as plt
from pandas import DataFrame

params = get_params()
params.update({
    "comparison operation": "ratio",
    "clear sky model": "GHI",
    "longitude": -100.22,
    "latitude": 25.75,
    "timezone": -5,
    "top vectors": 30,
    "station": "Noroeste",
    "date": "2021-05-13",
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
comparison = threshold_filter(comparison,
                              params)
# Clean data
data = clean_data(data,
                  clear_sky,
                  comparison)
plt.plot(data)
# Cosine similarity
clean_data = clean_data_model(params)
cosine = get_cosine_similarity(data,
                               SIMA_data,
                               params)
# Full data
similarity_dates = get_best_similarity_dates(cosine,
                                             params,
                                             0)
similarity_vectors = get_similarity_vectors(clean_data,
                                            similarity_dates,
                                            params)
full_data = fill_data(data,
                      similarity_vectors)
plt.plot(full_data)
plt.show()
