from Modules.functions import get_labels, get_colors
from pandas import read_csv, DataFrame, concat
from matplotlib.container import BarContainer
from Modules.params import get_params
import matplotlib.pyplot as plt
from os.path import join


def get_frecuency(data: DataFrame) -> DataFrame:
    columns = data.columns
    frecuency = DataFrame()
    for column in columns:
        freq = data[column].value_counts()
        frecuency = concat([frecuency,
                            freq],
                           axis=1)
    frecuency = frecuency.T
    frecuency = frecuency.sum()
    return frecuency


def autolabel(rects: BarContainer) -> None:
    for rect in rects:
        height = rect.get_height()
        height_str = "{:.2f}%".format(height)
        plt.annotate(height_str,
                     xy=(rect.get_x() + rect.get_width() / 2,
                         height),
                     xytext=(0, 1),
                     textcoords="offset points",
                     ha='center',
                     va='bottom',)


params = get_params()
params.update({
    "graphics file": "distribution.png"
})
filename = join(params["path results"],
                params["classification file"])
classification = read_csv(filename,
                          index_col=0,
                          parse_dates=True)
frecuency = get_frecuency(classification)
frecuency = 100*frecuency / frecuency.sum()
keys, label = get_labels(params)
colors = get_colors(params)
plt.subplots(figsize=(8, 4))
bar = plt.bar(frecuency.index,
              frecuency,
              color=colors)
autolabel(bar)
plt.xticks(keys,
           label)
plt.xlabel("Condiciones de cielo")
plt.yticks(range(0,
                 60,
                 5))
plt.ylabel("Distribución")
plt.grid(ls="--",
         color="#000000",
         alpha=0.6,
         axis="y")
plt.tight_layout()
filename = join(params["path graphics"],
                params["graphics file"])
plt.savefig(filename,
            dpi=400)
