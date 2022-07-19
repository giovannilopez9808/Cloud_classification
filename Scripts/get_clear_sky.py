"""
python get_clear_sky (clear sky model) 
"""
from Modules.clear_sky import clear_sky_model
from Modules.data_model import SIMA_model
from Modules.params import get_params
from pandas import concat, DataFrame
from os.path import join
from tqdm import tqdm
from sys import argv

params = get_params()
params.update({
    "clear sky model": argv[1],
    "timezone": -5,
})

results = DataFrame(columns=params["stations"])
for year in params["years"]:
    print(f"Analizando año {year}")
    params["year"] = year
    SIMA = SIMA_model(params)
    model = clear_sky_model()
    dates = SIMA.get_dates()
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
                params["clear sky model"],
                params["clear sky file"])
results.index.name = "Date"
results.to_csv(filename)
