from matplotlib.colors import ListedColormap
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
    "names": {
        "Attention CNN": "CNN con atención",
        "Bi LSTM": "Bi LSTM",
        "RNN": "RNN",
        "LSTM": "LSTM",
        "CNN": "CNN",
        "perceptron": "Perceptron",
        "Decision tree": "Arbol de decisión",
        "Gaussian naive": "Naive Gaussiano",
        "Randon forest": "Arboles aleatorios",
        "KNN": "KNN",
        "SVM": "SVM",
    }
})
filename = join(params["path results"],
                params["file distribution"])
data = read_csv(filename,
                index_col=0)
data = data+1
data.index = [params["names"][index]
              for index in data.index]
data = data.T
fig, ax = plt.subplots(figsize=(12, 10))
cmap = cm.get_cmap("inferno",
                   14)
cmap = cmap(range(14))
cmap[0] = [1, 1, 1, 1]
cmap = ListedColormap(cmap)
colormap = ax.imshow(data,
                     cmap=cmap,
                     vmin=-0.5,
                     vmax=13.5,
                     aspect="auto")
bar = fig.colorbar(colormap,
                   ticks=range(13))
color_ticks = ["Sin\ndatos"]
color_ticks += list(range(13))
bar.ax.set_yticks(range(14))
bar.ax.set_yticklabels(color_ticks)
bar.ax.set_ylabel("Meses",
                  labelpad=20,
                  fontsize=14,
                  rotation=-90)
ax.set_xticks(range(29),
              data.columns,
              rotation=90)
ax.set_ylabel("Estaciones",
              labelpad=10,
              fontsize=14)
ax.set_xticks(minior_tick(range(29)),
              minor=True)
ax.set_yticks(range(16),
              data.index)
ax.set_yticks(minior_tick(range(16)),
              minor=True)
ax.grid(ls="--",
        color="#9a8c98",
        which="minor")
plt.tight_layout()
filename = join(params["path graphics"],
                params["file graphics"])
plt.savefig(filename,
            dpi=400)
