from Modules.clear_sky import clear_sky_model
from Modules.data_model import SIMA_model
from Modules.params import get_params
from pandas import concat, DataFrame
from os.path import join
from tqdm import tqdm


params = get_params()
params.update({
    "pollutant": "SR",
    "year": "2021",
    "timezone": -5,
    "hour initial": 6,
    "hour final": 21,
})


SIMA = SIMA_model()
model = clear_sky_model()
filename = f"{params['year']}.csv"
filename = join(params["path data"],
                params["SIMA folder"],
                filename)
SIMA.read(filename)
dates = SIMA.get_dates()
results = DataFrame(columns=params["stations"])
bar = tqdm(dates)
for date in bar:
    bar.set_postfix(date=date)
    params["date"] = date
    results_per_day = DataFrame()
    for station in params["stations"]:
        dataset = SIMA.get_station_info(params,
                                        station)
        params["latitude"] = dataset["Latitude"]
        params["longitude"] = dataset["Longitude"]
        clear_sky = model.run(params)
        clear_sky.columns = [station]
        results_per_day = concat([results_per_day,
                                  clear_sky],
                                 axis=1)
    results = concat([results,
                      results_per_day])
filename = join(params["path results"],
                params["clear sky file"])
results.index.name = "Date"
results.to_csv(filename)
