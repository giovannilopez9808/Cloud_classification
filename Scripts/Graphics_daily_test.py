from Modules.data_model import clean_data_model
from Modules.params import get_params
import matplotlib.pyplot as plt
from os.path import join

params = get_params()
params.update({
    "file graphics": "test_daily.png",
    "comparison operation": "ratio",
    "clear sky model": "RS",
    "top vectors": 10,
    "timezone": -5,
    "test": {
        "Noreste": {"date": "2021-10-23"},
        "Sureste2": {"date": "2020-07-25"},
        "Suroeste": {"date": "2019-12-15"},
        "Noroeste": {"date": "2019-04-06"},
    }
})

clean_data = clean_data_model(params)
fig, axs = plt.subplots(2, 2,
                        figsize=(18, 8),
                        sharex=True,
                        sharey=True)
axs = axs.flatten()
for station, ax in zip(params["test"],
                       axs):
    date = params["test"][station]["date"]
    clean_data.get_station_data(station)
    clean = clean_data.get_date_data(date)
    ax.plot(clean.index.hour,
            clean,
            ls="--",
            marker="o",
            color="#7209b7")
    ax.set_title(f"{station} {date}")
    ax.set_xlim(clean.index.hour[6],
                clean.index.hour[20])
    ax.set_ylim(0, 1000)
    ax.grid(ls="--",
            color="#000000",
            alpha=0.6)
fig.text(0, 0.42,
         "Irradiancia solar (W/m$^2$)",
         rotation=90,
         fontsize=14)
fig.text(0.47, 0.01,
         "Tiempo local (h)",
         fontsize=14)
plt.tight_layout(pad=2.2)
filename = join(params["path graphics"],
                params["file graphics"])
plt.savefig(filename,
            dpi=400)
