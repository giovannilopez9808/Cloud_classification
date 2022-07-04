from Modules.functions import get_labels, get_colors
from Modules.data_model import comparison_data
from pandas import read_csv, DataFrame, concat
from Modules.params import get_params
import matplotlib.pyplot as plt
from os.path import join


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
