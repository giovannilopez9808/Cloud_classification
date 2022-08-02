from Modules.data_model import (clean_data_model,
                                clear_sky_data,
                                SIMA_model)
from Modules.functions import get_hourly_mean
from Modules.params import get_params
import matplotlib.pyplot as plt
from os.path import join

params = get_params()
params.update({
    "file graphics": "example_clean_data.png",
    "clear sky model": "GHI",
    "year": 2021,
    "dataset": {
        1: {
            "station": "Noroeste",
            "date": "2021-06-02",
        },
        2: {
            "station": "Noroeste",
            "date": "2021-10-26",
        },
    },
})
fig, axs = plt.subplots(2, 2,
                        figsize=(16, 8),
                        sharex=True,
                        sharey=True)
for index, ax in zip(params["dataset"],
                     axs):
    ax1, ax2 = ax
    dataset = params["dataset"][index]
    params["station"] = dataset["station"]
    params["date"] = dataset["date"]
    SIMA = SIMA_model(params)
    SIMA.get_station_data(params["station"],
                          params["pollutant"])
    SIMA_data = SIMA.get_date_data(params["date"])
    clear_sky = clear_sky_data(params)
    clear_sky.get_station_data(params["station"])
    clear_data = clear_sky.get_date_data(params["date"])
    clear_data = get_hourly_mean(clear_data)
    clean_data = clean_data_model(params)
    clean_data.get_station_data(params["station"])
    data = clean_data.get_date_data(params["date"])
    ax1.set_xlim(6, 20)
    ax1.set_ylim(0, 1600)
    ax1.plot(SIMA_data.index.hour,
             SIMA_data,
             color="#03071e",
             marker="o",
             ls="--",
             label="Mediciones")
    ax1.grid(ls="--",
             color="#000000",
             alpha=0.6)
    ax1.plot(clear_data.index.hour,
             clear_data,
             color="#9d0208",
             marker="o",
             ls="--",
             label="Modelo GHI")
    ax2.plot(data.index.hour,
             data,
             color="#e85d04",
             marker="o",
             ls="--",
             label="Mediciones limpias")
    ax2.plot(clear_data.index.hour,
             clear_data,
             marker="o",
             ls="--",
             color="#9d0208")
    ax2.grid(ls="--",
             color="#000000",
             alpha=0.6)
fig.text(0, 0.4,
         "Irradiancia solar (W/m$^2$)",
         rotation=90,
         fontsize=14)
fig.text(0.47, 0.01,
         "Hora locla (h)",
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
