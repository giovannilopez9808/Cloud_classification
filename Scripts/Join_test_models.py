from matplotlib.colors import LinearSegmentedColormap
from Modules.params import get_params
import matplotlib.pyplot as plt
from pandas import (DataFrame,
                    read_csv,
                    concat)
from numpy import arange
from os.path import join


def iscorrect(value: int,
              data: int) -> int:
    if data == value:
        return 0
    return 1


params = get_params()
params.update({
    "file results": "Test_models.csv",
    "file graphics": "Test_models.png",
    "colors": {
        "correct": (82/255, 182/255, 154/255),
        "incorrect": (230/255, 57/255, 70/255),
    },
    "labels": [
        0,
        2,
        0,
        1,
    ],
})
results = DataFrame()
for folder in [params["Classical model path"],
               params["Neural model path"]]:
    filename = join(params["path results"],
                    folder,
                    params["file results"])
    data = read_csv(filename,
                    index_col=0)
    results = concat([results,
                      data])
table = DataFrame(results,
                  dtype=int)
headers = table.columns
headers = [station.replace(" ",
                           "\n")
           for station in headers]
colors = [params["colors"][label]
          for label in params["colors"]]
for header, value in zip(table.columns,
                         params["labels"]):
    results[header] = results[header].apply(lambda data: iscorrect(data,
                                                                   value))
cmap = LinearSegmentedColormap.from_list("custom",
                                         colors,
                                         N=2)
fig, ax = plt.subplots()
ax.imshow(results.to_numpy(),
          origin="lower",
          vmin=0,
          vmax=1,
          interpolation="nearest",
          aspect='auto',
          cmap=cmap)
ax.set_yticks(range(len(results)),
              results.index)
ax.set_xticks(range(results.columns.size),
              headers)
ax.set_xticks(arange(-.5, 4, 1),
              minor=True)
ax.set_yticks(arange(-.5, 10, 1),
              minor=True)
ax.xaxis.tick_top()
ax.grid(ls="--",
        which='minor',
        color="#000000")
plt.tight_layout()
filename = join(params["path graphics"],
                params["file graphics"])
plt.savefig(filename)
