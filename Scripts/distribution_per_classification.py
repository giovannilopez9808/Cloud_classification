from Modules.dataset_model import dataset_model
from matplotlib.ticker import PercentFormatter
from Modules.params import get_params
from numpy import ones_like, linspace
import matplotlib.pyplot as plt
from pandas import DataFrame
from sys import argv

params = get_params()
params.update({
    "comparison operation": argv[1],
    "clear sky model": argv[2],
    "hour initial": 10,
    "hour final": 18,
})
fig, all_axs = plt.subplots(3, 4,
                            sharex=True,
                            sharey=True,
                            figsize=(12, 8))
all_axs = all_axs.T
for station, axs in zip(params["stations"],
                        all_axs):
    params["station"] = station
    dataset = dataset_model(params)
    for index, ax in zip(params["classification"],
                         axs):
        color = params["classification"][index]["color"]
        index_vector = dataset.train[1] == index
        vector = dataset.train[0][index_vector]
        vector = vector.flatten()
        vector = vector[vector > 0]
        vector = vector[vector < 1]
        weights = ones_like(vector)*100 / len(vector)
        ax.hist(vector,
                bins=30,
                color=color,
                weights=weights)
        ax.set_xlim(0, 1)
        ax.set_xticks(linspace(0, 1, 6))
        ax.set_ylim(0, 30)
        ax.grid(ls="--",
                color="#000000",
                alpha=0.6)
        ax.yaxis.set_major_formatter(PercentFormatter())
        if index == 0:
            ax.set_title(station)
        if station == params["stations"][0]:
            classification = params["classification"][index]["label"]
            ax.set_ylabel(classification)
plt.tight_layout(pad=1)
plt.savefig("test.png")
