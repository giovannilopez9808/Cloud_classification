from Modules.functions import get_hourly_mean
from Modules.clear_sky import clear_sky_model
from Modules.data_model import SIMA_model
from Modules.params import get_params
import matplotlib.pyplot as plt

params = get_params()
params.update({
    "latitude": 25.757,
    "longitude": -100.366,
    "timezone": -5,
    "pollutant": "SR",
    "year": 2021,
    "date": "2021-10-08",
})
data = SIMA_model(params)
data = data.get_data("Noroeste",
                     "SR",
                     params["date"])
clear_sky = clear_sky_model()
params["clear sky model"] = "RS"
rs = clear_sky.run(params)
rs = get_hourly_mean(rs)
params["clear sky model"] = "GHI"
ghi = clear_sky.run(params)
ghi = get_hourly_mean(ghi)
plt.subplots(figsize=(8, 4))
plt.plot(data,
         label="SIMA",
         color="#d00000",
         ls="--",
         marker="o")
plt.plot(rs,
         label="RS",
         color="#e85d04",
         ls="--",
         marker="o")
plt.plot(ghi,
         label="GHI$_0$",
         color="#03071e",
         ls="--",
         marker="o")
plt.xticks(data.index,
           data.index.hour)
plt.xlim(data.index[6],
         data.index[20])
plt.ylim(0, 1400)
plt.grid(ls="--",
         color="#000000",
         alpha=0.6)
plt.legend(frameon=False,
           ncol=3,
           loc="upper center")
plt.title(params["date"])
plt.ylabel("Solar Irradiance (W/m$^2$)")
plt.xlabel("Local time (h)")
plt.tight_layout()
plt.savefig(params["date"])
