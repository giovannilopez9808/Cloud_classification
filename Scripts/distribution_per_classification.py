from Modules.data_model import comparison_data, classification_data
from Modules.functions import get_colors
from Modules.params import get_params
import matplotlib.pyplot as plt
from numpy import linspace
from os.path import join

params = get_params()
params.update({
    "comparison": "ratio",
    "x label": "Ratio",
    "y label": "Frecuency",
    "bins": 700,
    "x limit": [0, 1],
    "y limit": [0, 40],
})
cloud_types = list(params["classification"].keys())
classification = classification_data(params)
comparison = comparison_data(params)
comparison.read(params["comparison"])
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
ax1.set_xlim(params["x limit"][0],
             params["x limit"][1])
ax1.set_xticks(linspace(0, 1, 11))
ax1.set_ylim(params["y limit"][0],
             params["y limit"][1])
ax2.set_ylabel(params["y label"])
ax3.set_xlabel(params["x label"])
for i, ax in enumerate([ax1, ax2, ax3]):
    title = params["classification"][i]["label"]
    ax.set_title(title)
    ax.hist(data[i],
            bins=params["bins"],
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
