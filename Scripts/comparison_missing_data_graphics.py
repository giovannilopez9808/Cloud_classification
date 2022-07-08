from Modules.data_model import (SIMA_model,
                                clear_sky_data,
                                full_data_model)
from Modules.functions import get_hourly_mean
from Modules.params import get_params
import matplotlib.pyplot as plt

params = get_params()
params.update({
    "clear sky model": "GHI",
    # "station": "Sureste2",
    # "date": "2021-07-22",
    "station": "Noroeste",
    "date": "2021-06-02",
    # "station": "Noroeste",
    # "date": "2021-10-26",
    # "station": "Noroeste",
    # "date": "2021-04-09",
    "pollutant": "SR",
    "year": 2021,
})
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
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4),
                               sharex=True,
                               sharey=True)
ax1.plot(data,
         # label="SIMA",
         color="#d00000",
         ls="--",
         marker="o")
ax1.plot(clear_sky,
         # label="RS model",
         color="#03071e",
         ls="--",
         marker="o")
ax2.plot(clear_sky,
         label="GHI model",
         color="#03071e",
         ls="--",
         marker="o")
ax2.plot(full_data,
         label="SIMA",
         color="#d00000",
         ls="--",
         marker="o")
ax2.plot(full_data[:10],
         label="Restoration",
         color="#8ac926",
         ls="--",
         marker="o")
ax1.set_xticks(data.index,
               data.index.hour)
ax1.set_xlim(data.index[6],
             data.index[20])
ax1.set_ylim(0, 1400)
ax1.grid(ls="--",
         color="#000000",
         alpha=0.6)
ax2.grid(ls="--",
         color="#000000",
         alpha=0.6)
fig.legend(frameon=False,
           ncol=3,
           loc="upper center")
ax1.set_title(params["date"])
ax2.set_title(params["date"])
ax1.set_ylabel("Solar Irradiance (W/m$^2$)")
ax2.set_ylabel("Solar Irradiance (W/m$^2$)")
ax1.set_xlabel("Local time (h)")
ax2.set_xlabel("Local time (h)")
plt.tight_layout()
plt.savefig(params["date"])
