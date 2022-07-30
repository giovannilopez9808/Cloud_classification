from Modules.data_model import SIMA_model
from Modules.params import get_params
import matplotlib.pyplot as plt
from os.path import join

params = get_params()
params.update({
    "file graphics": "example_sky_conditions.png",
    "year": "2019",
    "datasets": {
        "Noroeste": {
            "date": "2019-06-05",
            "title": "Parcialmente nublado",
        },
        "Noreste": {
            "date": "2019-06-16",
            "title": "Nublado",
        },
        "Suroeste": {
            "date": "2019-08-10",
            "title": "Despejado",
        },
        "Sureste2": {
            "date": "2019-07-22",
            "title": "Nublado",
        },
    }
})
SIMA = SIMA_model(params)
fig, axs = plt.subplots(2, 2,
                        figsize=(12, 8),
                        sharex=True,
                        sharey=True)
axs = axs.flatten()
for station, ax in zip(params["datasets"],
                       axs):
    datasets = params["datasets"][station]
    date = datasets["date"]
    title = datasets["title"]
    SIMA.get_station_data(station,
                          params["pollutant"])
    data = SIMA.get_date_data(date)
    ax.plot(data.index.hour,
            data,
            ls="--",
            marker="o",
            color="#52b69a")
    ax.set_title(f"{station} {date}\n{title}")
    # ax.set_xticks(data.index,
    # data.index.hour)
    ax.set_xlim(data.index.hour[6],
                data.index.hour[20])
    ax.set_ylim(0, 1000)
    ax.grid(ls="--",
            color="#000000",
            alpha=0.5)
fig.text(0.01, 0.37,
         "Irradiancia solar (W/m$^2$)",
         fontsize=14,
         rotation=90)
fig.text(0.47, 0.01,
         "Hora local (h)",
         fontsize=14)
plt.tight_layout(pad=3)
filename = join(params["path graphics"],
                params["file graphics"])
plt.savefig(filename,
            dpi=400)
