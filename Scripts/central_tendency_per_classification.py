from Modules.data_model import comparison_data, classification_data
from Modules.functions import get_labels
from Modules.params import get_params
from pandas import DataFrame, concat
from os.path import join

params = get_params()
params.update({
    "file results": "Central_tendency",
    "comparison operation": "diff",
    "clear sky model": "RS",
})
cloud_types, names = get_labels(params)
classification = classification_data(params)
comparison = comparison_data(params)
daily = comparison.get_daily_mean()
data = dict()
for cloud_type in cloud_types:
    data[cloud_type] = []
    for station in daily.columns:
        classification.get_station_data(station)
        values = classification.get_data_from_type(cloud_type)
        dates = values.index
        values = daily[station][dates]
        data[cloud_type] += list(values)
    data[cloud_type] = DataFrame(data[cloud_type])
results = DataFrame()
for cloud_type, name in zip(cloud_types, names):
    tendency = data[cloud_type].describe()
    tendency.columns = [name]
    results = concat([results,
                      tendency],
                     axis=1)
results.index.name = "Central tendency"
filename = "{}_{}.csv".format(params["file results"],
                              params["comparison operation"])
filename = join(params["path results"],
                params["clear sky model"],
                filename)
results.to_csv(filename)
