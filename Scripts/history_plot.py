from Modules.params import get_params
import matplotlib.pyplot as plt
from pandas import read_csv
from os.path import join
from sys import argv

params = get_params()
params.update({
    "comparison operation": argv[1],
    "clear sky model": argv[2],
    "neural model": argv[3],
})
filename = "{}_{}.csv".format(params["comparison operation"],
                              params["clear sky model"])
filename = join(params["path results"],
                params["Neural model path"],
                params["neural model"],
                filename)
data = read_csv(filename)
plt.plot(data["accuracy"])
plt.plot(data["val_accuracy"])
plt.show()
