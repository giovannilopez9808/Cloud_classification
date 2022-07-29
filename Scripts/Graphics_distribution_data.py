from Modules.params import get_params
import matplotlib.pyplot as plt
from pandas import read_csv
from matplotlib import cm
from os.path import join


def minior_tick(values: list) -> list:
    ticks = [value-0.5
             for value in values]
    return ticks


params = get_params()
params.update({
    "file distribution": "Distribution.csv",
    "file graphics": "Distribution_stations.png",
})
filename = join(params["path results"],
                params["file distribution"])
data = read_csv(filename,
                index_col=0)
data = data.fillna(0)
data = data.T
fig, ax = plt.subplots(figsize=(12, 10))
cmap = cm.get_cmap("inferno",
                   12)
colormap = ax.matshow(data,
                      cmap=cmap,
                      aspect="auto")
bar = fig.colorbar(colormap,
                   ticks=range(13))
ax.set_xticks(range(29),
              data.columns,
              rotation=90)
ax.set_xticks(minior_tick(range(29)),
              minor=True)
ax.set_yticks(range(16),
              data.index)
ax.set_yticks(minior_tick(range(16)),
              minor=True)
ax.grid(ls="--",
        which="minor")
plt.tight_layout()
filename = join(params["path graphics"],
                params["file graphics"])
plt.savefig(filename,
            dpi=400)
