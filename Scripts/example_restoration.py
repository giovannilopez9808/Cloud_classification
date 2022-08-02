from Modules.data_model import (SIMA_model,
                                clear_sky_data,
                                full_data_model)
from Modules.functions import get_hourly_mean
from Modules.params import get_params
import matplotlib.pyplot as plt
from os.path import join

params = get_params()
params.update({
    "file graphics": "example_restoration.png",
    "clear sky model": "GHI",
    "datasets": {
        1: {
            "station": "Noroeste",
            "date": "2021-06-02",
        },
        2: {
            "station": "Noroeste",
            "date": "2021-10-26",
        },
    },
    "pollutant": "SR",
    "year": 2021,
})
fig, axs = plt.subplots(2, 2,
                        figsize=(16, 8),
                        sharex=True,
                        sharey=True)
for index, ax in zip(params["datasets"],
                     axs):
    ax1, ax2 = ax
    dataset = params["datasets"][index]
    params["station"] = dataset["station"]
    params["date"] = dataset["date"]
    data = SIMA_model(params)
    data = data.get_data(params["station"],
                         "SR",
                         params["date"])
    clear_sky = clear_sky_data(params)
    clear_sky = clear_sky.get_data(params["station"],
                                   params["date"])
    clear_sky = get_hourly_mean(clear_sky)
    full_data = full_data_model(params)
    full_data = full_data.get_data(params["station"],
                                   params["date"])
    ax1.plot(data.index.hour,
             data,
             color="#d00000",
             ls="--",
             marker="o")
    ax1.plot(clear_sky.index.hour,
             clear_sky,
             color="#03071e",
             ls="--",
             marker="o")
    ax2.plot(clear_sky.index.hour,
             clear_sky,
             label="modelo GHI",
             color="#03071e",
             ls="--",
             marker="o")
    ax2.plot(full_data.index.hour,
             full_data,
             label="Mediciones",
             color="#d00000",
             ls="--",
             marker="o")
    ax2.plot(full_data.index.hour[:10],
             full_data[:10],
             label="Mediciones restauradas",
             color="#8ac926",
             ls="--",
             marker="o")
    ax1.set_xlim(data.index.hour[6],
                 data.index.hour[20])
    ax1.set_ylim(0, 1600)
    ax1.grid(ls="--",
             color="#000000",
             alpha=0.6)
    ax2.grid(ls="--",
             color="#000000",
             alpha=0.6)
    fig.text(0, 0.42,
             "Irradiancia solar (W/m$^2$)",
             rotation=90,
             fontsize=14)
    fig.text(0.47, 0,
             "Hora local (h)",
             fontsize=14)
lines_labels = [ax.get_legend_handles_labels()
                for ax in fig.axes]
lines, labels = [sum(lol, [])
                 for lol in zip(*lines_labels)]
lines_true = []
labels_true = []
for line, label in zip(lines,
                       labels):
    if not label in labels_true:
        labels_true += [label]
        lines_true += [line]
fig.legend(lines_true,
           labels_true,
           loc="upper center",
           ncol=3,
           frameon=False)
plt.tight_layout(pad=2.2)
filename = join(params["path graphics"],
                params["file graphics"])
plt.savefig(filename,
            dpi=400)
