from Modules.data_model import clean_data_model
from sklearn.metrics import pairwise_distances
from Modules.params import get_params
from pandas import DataFrame
from os.path import join

params = get_params()
params.update({
    "file results": "similarity.csv",
})
clean_data = clean_data_model(params)
dates = clean_data.get_dates()
headers = [f"{station} {date}"
           for station in params["stations"]
           for date in dates]
print("-"*30)
print("Calculando similitud")
clean_data.data = clean_data.data.fillna(0)
vectors = clean_data.data.to_numpy()
vectors = vectors.T
vectors = vectors.reshape(-1, 24)
cosine = 1-pairwise_distances(vectors,
                              metric="cosine")
cosine = DataFrame(cosine,
                   index=headers,
                   columns=headers)
filename = join(params["path results"],
                params["file results"])
cosine.to_csv(filename)
