from Modules.data_model import comparison_data
from Modules.params import get_params
import matplotlib.pyplot as plt

params = get_params()
params.update({
    "graphics file": "distribution.png",
    "comparison operation": "ratio",
    "clear sky model": "RS",
})
comparison = comparison_data(params)
daily = comparison.get_daily_mean()
plt.subplots(figsize=(10, 4))
for station in daily.columns:
    plt.scatter(daily.index,
                daily[station],
                label=station,
                marker=".")
plt.ylim(0, 1)
plt.legend(frameon=False,
           ncol=4)
plt.show()
