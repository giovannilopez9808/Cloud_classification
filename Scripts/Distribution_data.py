from pandas import read_csv, DataFrame
from Modules.params import get_params
from os import listdir as ls
from os.path import join
from tqdm import tqdm

params = get_params()
params.update({
    "path data": "../Data/SIMA",
    "path results": "../Results",
    "file results": "Count.csv",
    "parameter": "SR",
    "Minimum data per day": 10,
    "Minimum data per month": 21,
})

results = dict()
# Get all files
files = sorted(ls(params["path data"]))
bar = tqdm(files)
for file in bar:
    bar.set_postfix(file=file)
    # Year from filename
    year = file.split(".")[0]
    results[year] = dict()
    # Filename with all route
    filename = join(params["path data"],
                    file)
    # Read data
    data = read_csv(filename,
                    header=[0, 1],
                    skiprows=[2],
                    index_col=0,
                    parse_dates=True,
                    low_memory=False)
    # Get columns
    columns = data.columns
    # Get columns with restriction
    columns = [(station, value)
               for station, value in columns
               if value == params["parameter"]]
    # Get data with restrictions
    data = data[columns]
    data = data[data.index.hour >= 8]
    data = data[data.index.hour <= 19]
    # Daily count
    data = data.resample("D").count()
    data = data >= params["Minimum data per day"]
    # Monthly count
    data = data.resample("MS").sum()
    data = data >= params["Minimum data per month"]
    data = data.sum()
    # Save data
    for station, value in data.index:
        montly = data.loc[(station, value)]
        results[year][station] = montly
# To DataFrame
results = DataFrame(results)
# Stations as header
results = results.T
# Save results
filename = join(params["path results"],
                params["file results"])
results.to_csv(filename)
