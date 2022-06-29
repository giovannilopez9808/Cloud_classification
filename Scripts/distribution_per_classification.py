from Modules.data_model import comparison_data, classification_data
from Modules.functions import get_colors
from Modules.params import get_params
import matplotlib.pyplot as plt
from numpy import linspace
from os.path import join

params = get_params()
params.update({
    "comparison": "diff",
    "graphics params": {
        "ratio": {
            "x label": "Ratio",
            "y label": "Frecuency",
            "bins": 700,
            "x ticks": linspace(0, 1, 11),
            "x limit": [0, 1],
            "y limit": [0, 40],
        },
        "diff": {
            "x label": "Difference",
            "y label": "Frecuency",
            "bins": 75,
            "x ticks": linspace(0, 1000, 11),
            "x limit": [0, 1000],
            "y limit": [0, 30],
        }
    }
})
cloud_types = list(params["classification"].keys())
classification = classification_data(params)
comparison = comparison_data(params)
comparison.read(params["comparison"])
dataset = params["graphics params"][params["comparison"]]
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
fig, (ax1, ax2, ax3) = plt.subplots(3, 1,
                                    sharex=True,
                                    sharey=True,
                                    figsize=(12, 8))
colors = get_colors(params)
ax1.set_xlim(dataset["x limit"][0],
             dataset["x limit"][1])
ax1.set_xticks(dataset["x ticks"])
ax1.set_ylim(dataset["y limit"][0],
             dataset["y limit"][1])
ax2.set_ylabel(dataset["y label"])
ax3.set_xlabel(dataset["x label"])
for i, ax in enumerate([ax1, ax2, ax3]):
    title = params["classification"][i]["label"]
    ax.set_title(title)
    ax.hist(data[i],
            bins=dataset["bins"],
            color=colors[i])
    ax.grid(ls="--",
            color="#000000",
            alpha=0.6)
plt.tight_layout()
filename = f"{params['comparison']}.png"
filename = join(params["path graphics"],
                filename)
plt.savefig(filename,
            dpi=400)
